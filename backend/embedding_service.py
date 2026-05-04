from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
import config

class EmbeddingService:
    def __init__(self):
        print(f"Loading embedding model: {config.EMBEDDING_MODEL}")
        self.model = SentenceTransformer(config.EMBEDDING_MODEL)
        print("Embedding model loaded successfully")

    def encode_query(self, query: str) -> np.ndarray:
        formatted_query = f"query: {query}"
        embedding = self.model.encode(formatted_query, normalize_embeddings=True)
        return embedding

    def encode_passages(self, passages: List[str]) -> np.ndarray:
        formatted_passages = [f"passage: {passage}" for passage in passages]
        embeddings = self.model.encode(formatted_passages, normalize_embeddings=True)
        return embeddings

    def encode_single_passage(self, passage: str) -> np.ndarray:
        formatted_passage = f"passage: {passage}"
        embedding = self.model.encode(formatted_passage, normalize_embeddings=True)
        return embedding

embedding_service = EmbeddingService()
