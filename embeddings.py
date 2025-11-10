"""Embeddings using Ollama nomic-embed-text for semantic understanding.

Uses Ollama's nomic-embed-text model for fast, local semantic embeddings.
"""
from typing import List
import hashlib
import struct
import os
import ollama


class MockEmbeddings:
    """Semantic embeddings using Ollama's nomic-embed-text model.
    
    Uses Ollama locally for semantic embeddings (no downloads needed if model exists).
    Falls back to hash-based approach if Ollama unavailable.
    Dimension: 768 (matches Pinecone index config).
    """
    
    def __init__(self, dimension: int = 768):
        self.dimension = dimension
        self.use_ollama = False
        self._test_ollama()
    
    def _test_ollama(self):
        """Test if Ollama is available with nomic-embed-text model."""
        try:
            # Test embedding
            result = ollama.embeddings(model="nomic-embed-text", prompt="test")
            if result and "embedding" in result:
                emb = result["embedding"]
                actual_dim = len(emb)
                print(f"✅ Using Ollama nomic-embed-text ({actual_dim} dimensions) for embeddings!")
                self.use_ollama = True
                self.actual_dimension = actual_dim
                return
        except Exception as e:
            print(f"⚠️  Ollama nomic-embed-text not available: {e}")
        
        print("⚠️  Using fallback hash-based embeddings")
        self.use_ollama = False
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        if self.use_ollama:
            embeddings = []
            for i, text in enumerate(texts):
                emb = self._embed_with_ollama(text)
                embeddings.append(emb)
                if (i + 1) % 5 == 0:
                    print(f"   Embedded {i + 1}/{len(texts)} documents...")
            return embeddings
        else:
            return [self._embed_hash(text) for text in texts]
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query."""
        if self.use_ollama:
            return self._embed_with_ollama(text)
        else:
            return self._embed_hash(text)
    
    def _embed_with_ollama(self, text: str) -> List[float]:
        """Embed using Ollama's nomic-embed-text endpoint."""
        try:
            result = ollama.embeddings(model="nomic-embed-text", prompt=text)
            embedding = result.get("embedding", [])
            return self._pad_or_truncate(embedding)
        except Exception as e:
            print(f"⚠️  Ollama embedding failed: {e}, using hash fallback")
            return self._embed_hash(text)
    
    def _pad_or_truncate(self, embedding: List[float]) -> List[float]:
        """Pad or truncate embedding to exact dimension."""
        if len(embedding) == self.dimension:
            return embedding
        elif len(embedding) < self.dimension:
            return embedding + [0.0] * (self.dimension - len(embedding))
        else:
            return embedding[:self.dimension]
    
    def _embed_hash(self, text: str) -> List[float]:
        """Fallback: create a deterministic embedding using hashing."""
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        
        embedding = []
        for i in range(self.dimension):
            chunk_start = (i * 8) % len(hash_bytes)
            chunk = hash_bytes[chunk_start:chunk_start + 8]
            int_val = struct.unpack('<Q', chunk + b'\x00' * (8 - len(chunk)))[0]
            val = 2.0 * ((int_val % 1000) / 1000.0) - 1.0
            embedding.append(val)
        
        # Normalize to unit length
        norm = sum(x ** 2 for x in embedding) ** 0.5
        if norm > 0:
            embedding = [x / norm for x in embedding]
        
        return embedding
