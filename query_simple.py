"""Simple query using Ollama + Pinecone + Embeddings (no LangChain)."""
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=str(Path(__file__).resolve().parents[0] / '.env'))

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME") or "vexa"
VECTOR_DIM = int(os.getenv("VECTOR_DIM", "768"))
LLM_MODEL = os.getenv("LLM_MODEL") or "phi"

from pinecone import Pinecone as PineconeClient
import ollama
from embeddings import MockEmbeddings


def ask_question(query: str) -> str:
    """Ask a question using Ollama + Pinecone + Embeddings."""
    if not query:
        return ""
    
    print(f"❓ Query: {query}")
    print(f"🔍 Retrieving from Pinecone index '{INDEX_NAME}'...")
    
    try:
        # Initialize embeddings
        embeddings = MockEmbeddings(dimension=VECTOR_DIM)
        
        # Connect to Pinecone
        pc = PineconeClient(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
        index = pc.Index(INDEX_NAME)
        
        # Embed the query
        query_embedding = embeddings.embed_query(query)
        
        # Search for similar vectors
        results = index.query(
            vector=query_embedding,
            top_k=5,
            include_metadata=True
        )
        
        # Extract retrieved documents
        retrieved_docs = []
        for match in results.get("matches", []):
            text = match.get("metadata", {}).get("text", "")
            if text:
                retrieved_docs.append(text)
        
        if not retrieved_docs:
            return "I don't have information about that in the documents."
        
        # Create context
        context = "\n\n".join(retrieved_docs)
        
        # Print retrieval details to terminal only
        print(f"📚 Retrieved documents:")
        for i, doc in enumerate(retrieved_docs, 1):
            print(f"  {i}. {doc[:100]}...")
        
        # Prompt - extract exact text from story ONLY
        prompt = f"""You are answering questions by copying EXACT sentences from the story. NOTHING ELSE.

STORY TEXT:
{context}

QUESTION: {query}

RULES:
1. Copy EXACT sentences from the story above
2. If the answer is NOT in the story, respond ONLY with: "This is not mentioned in the story"
3. Do NOT rephrase, summarize, or add ANY words
4. Do NOT add explanations or instructions
5. Response should be ONLY the exact story text OR "This is not mentioned in the story"

ANSWER (exact story text only):"""
        
        # Generate answer with Ollama
        print(f"🧠 Using Ollama model: {LLM_MODEL}")
        print(f"⏳ Generating answer...")
        
        try:
            response = ollama.generate(
                model=LLM_MODEL,
                prompt=prompt,
                stream=False
            )
        except Exception as e:
            print(f"⚠️  Retrying Ollama connection...")
            import time
            time.sleep(2)
            response = ollama.generate(
                model=LLM_MODEL,
                prompt=prompt,
                stream=False
            )
        
        answer = response.get("response", "").strip()
        if not answer:
            return "This is not mentioned in the story"
        
        # Clean up preamble
        unwanted_starts = [
            "the answer is",
            "answer:",
            "based on the context,",
        ]
        
        answer_lower = answer.lower()
        for start in unwanted_starts:
            if answer_lower.startswith(start):
                answer = answer[len(start):].strip()
                break
        
        print(f"✅ Answer: {answer}")
        return answer
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}"


if __name__ == "__main__":
    query = input("Enter your question: ").strip()
    if query:
        answer = ask_question(query)
        print(f"\n📝 Answer:\n{answer}")
    else:
        print("❌ No query provided")