import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

from config import PINECONE_API_KEY, PINECONE_ENV, INDEX_NAME, VECTOR_DIM, LLM_MODEL

# Import ingestor and simple query (no LangChain dependencies)
from ingestor_simple import ingest_folder
from query_simple import ask_question

# Try to ensure Pinecone index exists at startup
try:
    from pinecone import Pinecone as PineconeClient
    pc = PineconeClient(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    indexes = pc.list_indexes().names()
    if INDEX_NAME not in indexes:
        print(f"📍 Creating Pinecone index '{INDEX_NAME}' with {VECTOR_DIM} dimensions...")
        pc.create_index(name=INDEX_NAME, dimension=VECTOR_DIM, metric="cosine")
    print(f"✅ Pinecone ready! Index: {INDEX_NAME}, Dimensions: {VECTOR_DIM}, Using LangChain + Ollama LLM + Pinecone")
except Exception as e:
    print(f"⚠️  Could not initialize Pinecone at startup: {e}")

# Create Flask app
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    """Home page: ingest folder."""
    message = ""
    if request.method == "POST":
        folder_path = request.form.get("folder_path", "").strip()
        if folder_path and os.path.exists(folder_path):
            try:
                # Auto-clear Pinecone before ingesting new folder
                try:
                    from pinecone import Pinecone as PineconeClient
                    pc = PineconeClient(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
                    index = pc.Index(INDEX_NAME)
                    print(f"🗑️  Clearing old data from Pinecone...")
                    index.delete(delete_all=True)
                    print(f"✅ Cleared!")
                except Exception as e:
                    print(f"⚠️  Could not clear Pinecone: {e}")
                
                # Now ingest new folder
                ingested_count = ingest_folder(folder_path)
                message = "✅ Path read successfully"
            except Exception as e:
                message = f"❌ Error: {str(e)}"
        else:
            message = "❌ Invalid folder path"
    
    return render_template("index.html", message=message)


@app.route("/query", methods=["POST"])
def query_page():
    """Query endpoint: search and answer questions."""
    # Get query text from form, query string, or JSON
    query_text = None
    try:
        query_text = request.values.get("query_text") or request.values.get("query")
        if not query_text and request.is_json:
            payload = request.get_json(silent=True) or {}
            query_text = payload.get("query_text") or payload.get("query")
    except Exception:
        query_text = None
    
    # Normalize
    if isinstance(query_text, str):
        query_text = query_text.strip()
    
    if not query_text:
        msg = "❌ Please enter a query"
        if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": False, "error": msg}), 400
        return msg
    
    try:
        answer = ask_question(query_text)
        
        if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": True, "answer": answer})
        return f"<h2>Answer</h2><pre>{answer}</pre>"
    
    except Exception as e:
        error_msg = str(e)
        if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": False, "error": error_msg}), 500
        return f"❌ Query failed: {error_msg}", 500


if __name__ == "__main__":
    app.run(debug=True)

