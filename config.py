from dotenv import load_dotenv
import os

# Load .env file
load_dotenv(dotenv_path=r"C:\Users\KAVITHA\OneDrive\Desktop\san\vexa\.env")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")  # Must be "vexa"
VECTOR_DIM = int(os.getenv("VECTOR_DIM", "384"))
EMBED_CACHE = os.getenv("EMBED_CACHE")
LLM_MODEL = os.getenv("LLM_MODEL")
