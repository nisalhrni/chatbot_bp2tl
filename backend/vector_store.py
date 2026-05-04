import faiss
import numpy as np
from typing import List, Tuple
import pickle
import os

class VectorStore:
    def __init__(self, dimension: int = 768):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.documents = []
        self.metadata = []

    def add_documents(self, embeddings: np.ndarray, documents: List[str], metadata: List[dict]):
        if len(embeddings.shape) == 1:
            embeddings = embeddings.reshape(1, -1)

        embeddings = embeddings.astype('float32')
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)
        self.documents.extend(documents)
        self.metadata.extend(metadata)

    def search(self, query_embedding: np.ndarray, top_k: int = 10) -> List[Tuple[str, dict, float]]:
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)

        query_embedding = query_embedding.astype('float32')
        faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))

        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx < len(self.documents):
                results.append((
                    self.documents[idx],
                    self.metadata[idx],
                    float(score)
                ))

        return results

    def save(self, path: str):
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
        faiss.write_index(self.index, f"{path}.index")
        with open(f"{path}.data", "wb") as f:
            pickle.dump({"documents": self.documents, "metadata": self.metadata}, f)

    def load(self, path: str):
        if os.path.exists(f"{path}.index") and os.path.exists(f"{path}.data"):
            self.index = faiss.read_index(f"{path}.index")
            with open(f"{path}.data", "rb") as f:
                data = pickle.load(f)
                self.documents = data["documents"]
                self.metadata = data["metadata"]
            return True
        return False

vector_store = VectorStore()
