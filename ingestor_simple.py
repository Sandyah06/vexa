"""Simple document ingestor (no LangChain dependencies)."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=str(Path(__file__).resolve().parents[0] / '.env'))

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME") or "vexa"
VECTOR_DIM = int(os.getenv("VECTOR_DIM", "768"))

from pinecone import Pinecone as PineconeClient
from embeddings import MockEmbeddings


def read_file(file_path):
    """Read text from various file types."""
    file_path = str(file_path)
    
    if file_path.lower().endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    elif file_path.lower().endswith('.md'):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    elif file_path.lower().endswith('.pdf'):
        try:
            from PyPDF2 import PdfReader
            text = ""
            with open(file_path, 'rb') as f:
                reader = PdfReader(f)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text()
            return text
        except Exception as e:
            print(f"⚠️  Failed to read PDF {file_path}: {e}")
            return ""
    
    return ""


def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into chunks."""
    if not text:
        return []
    
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end]
        
        if chunk.strip():
            chunks.append(chunk)
        
        start += chunk_size - overlap
    
    return chunks


def ingest_folder(folder_path: str) -> int:
    """Ingest all documents from a folder."""
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        raise ValueError(f"Folder not found: {folder_path}")
    
    print(f"📂 Scanning folder: {folder_path}")
    
    # Find all documents
    files = list(folder_path.rglob('*.txt')) + \
            list(folder_path.rglob('*.md')) + \
            list(folder_path.rglob('*.pdf'))
    
    print(f"✅ Found {len(files)} files")
    
    if not files:
        raise ValueError("No documents found in folder")
    
    # Read and chunk all files
    all_chunks = []
    for file_path in files:
        print(f"  📄 Reading: {file_path.name}")
        text = read_file(file_path)
        chunks = chunk_text(text, chunk_size=500, overlap=50)
        all_chunks.extend(chunks)
    
    print(f"✂️  Splitting into chunks...")
    print(f"📦 Created {len(all_chunks)} chunks")
    
    if not all_chunks:
        raise ValueError("No chunks created from documents")
    
    # Initialize embeddings and Pinecone
    embeddings = MockEmbeddings(dimension=VECTOR_DIM)
    pc = PineconeClient(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    index = pc.Index(INDEX_NAME)
    
    print(f"🔤 Generating embeddings...")
    
    # Create embeddings for all chunks
    chunk_embeddings = embeddings.embed_documents(all_chunks)
    
    print(f"⬆️  Upserting to Pinecone index '{INDEX_NAME}'...")
    
    # Upsert in batches
    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        batch_chunks = all_chunks[i:i+batch_size]
        batch_embeddings = chunk_embeddings[i:i+batch_size]
        
        # Prepare vectors for upsert
        vectors = []
        for j, (chunk, embedding) in enumerate(zip(batch_chunks, batch_embeddings)):
            vector_id = f"chunk_{i+j}"
            vectors.append({
                "id": vector_id,
                "values": embedding,
                "metadata": {"text": chunk}
            })
        
        # Upsert to Pinecone
        index.upsert(vectors=vectors)
        print(f"  ✅ Upserted batch {i//batch_size + 1}/{(len(all_chunks) + batch_size - 1)//batch_size}")
    
    total_ingested = len(all_chunks)
    print(f"✅ Successfully ingested {total_ingested} chunks into index '{INDEX_NAME}'")
    
    return total_ingested


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = input("Enter folder path to ingest: ").strip()
    
    if folder:
        try:
            count = ingest_folder(folder)
            print(f"\n✅ Ingestion complete: {count} chunks")
        except Exception as e:
            print(f"❌ Ingestion failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ No folder provided")
