
from functools import lru_cache

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


DOCUMENTS = [
    {
        "document_id": "HR-001",
        "title": "Remote Work Policy",
        "department": "HR",
        "page": 1,
        "text": (
            "Employees may work remotely up to two days per week, "
            "subject to approval from their direct manager. "
            "Remote work requests should be submitted at least "
            "two working days in advance. Employees must use "
            "company-approved devices when accessing internal systems."
        ),
    },
    {
        "document_id": "IT-001",
        "title": "Password Security Policy",
        "department": "IT",
        "page": 1,
        "text": (
            "Employees must use multi-factor authentication when "
            "accessing company systems that support it. Passwords "
            "must never be shared with colleagues. Suspected security "
            "incidents must be reported to the IT security team immediately."
        ),
    },
    {
        "document_id": "FIN-001",
        "title": "Expense Reimbursement Policy",
        "department": "Finance",
        "page": 1,
        "text": (
            "Employees must submit expense claims within thirty "
            "calendar days of the expense date. Receipts are required "
            "for all reimbursement claims. Reimbursement requests are "
            "reviewed by the finance department before payment."
        ),
    },
]


@lru_cache(maxsize=1)
def get_retriever():
    """Load the embedding model and build the vector index once."""

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    texts = [doc["text"] for doc in DOCUMENTS]

    vectors = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    return model, index


def retrieve_documents(question: str, top_k: int = 3) -> list[dict]:
    """Return the most similar documents with source metadata."""

    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question must be a non-empty string.")

    if (
        not isinstance(top_k, int)
        or isinstance(top_k, bool)
        or top_k <= 0
    ):
        raise ValueError("top_k must be a positive integer.")

    model, index = get_retriever()

    query_vector = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    k = min(top_k, index.ntotal)
    scores, indices = index.search(query_vector, k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        doc = DOCUMENTS[int(idx)]

        results.append({
            **doc,
            "similarity_score": float(score),
        })

    return results