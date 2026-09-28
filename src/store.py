import numpy as np


class VectorStore:
    def __init__(self):
        self.chunks = []

    def add_chunks(self, chunks):
        self.chunks.extend(chunks)

    def search(self, query_embedding, top_k=5):
        if not self.chunks:
            return []

        scores = []
        for chunk in self.chunks:
            similarity = self._cosine_similarity(query_embedding, chunk["embedding"])
            scores.append((chunk, similarity))

        scores.sort(key=lambda x: x[1], reverse=True)

        return scores[:top_k]

    def _cosine_similarity(self, vec_a, vec_b):
        dot_product = np.dot(vec_a, vec_b)
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        return dot_product / (norm_a * norm_b)
