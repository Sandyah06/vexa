"""Clear all vectors from Pinecone index."""
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=str(Path(__file__).resolve().parents[0] / '.env'))

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME") or "vexa"

from pinecone import Pinecone as PineconeClient

print(f"🗑️  Clearing Pinecone index: {INDEX_NAME}")
print(f"📍 Environment: {PINECONE_ENV}")

try:
    pc = PineconeClient(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    index = pc.Index(INDEX_NAME)
    
    # Delete all vectors by using delete with delete_all=True
    print("⏳ Deleting all vectors from index...")
    index.delete(delete_all=True)
    
    print("✅ Index cleared successfully!")
    print("📊 Index is now empty and ready for fresh data.")
    
except Exception as e:
    print(f"❌ Error clearing index: {e}")
    import traceback
    traceback.print_exc()
