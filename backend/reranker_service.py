from sentence_transformers import CrossEncoder
import config
from typing import List, Tuple

class RerankerService:
    def __init__(self):
        print(f"Loading reranker model: {config.RERANKER_MODEL}")
        self.model = CrossEncoder(config.RERANKER_MODEL)
        print("Reranker model loaded successfully")

    def rerank(self, query: str, documents: List[str]) -> List[Tuple[int, float]]:
        pairs = [[query, doc] for doc in documents]
        scores = self.model.predict(pairs)

        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

        return [(idx, float(scores[idx])) for idx in ranked_indices]

reranker_service = RerankerService()
