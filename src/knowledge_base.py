"""Retrieval: chunk the documents, index them and search the index."""

from functools import lru_cache

import faiss
from sentence_transformers import CrossEncoder, SentenceTransformer

from src.chunking import chunk_documents
from src.documents import DOCUMENTS


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# The embedding model reads at most 256 tokens (roughly 190 words), so
# chunks stay well below that limit to avoid silent truncation.
CHUNK_MAX_WORDS = 100

# One repeated sentence keeps a fact that sits on a chunk boundary
# together with the sentence before it.
CHUNK_OVERLAP_SENTENCES = 1

# The re-ranker is too slow to score every chunk in a large index, so it
# only re-orders the best candidates found by the vector search.
RERANK_CANDIDATES = 10


# Loading the model and embedding the chunks takes seconds, so the result
# is cached and reused for every question in the same process.
@lru_cache(maxsize=1)
def get_retriever():
    """Load the embedding model and build the chunk index once."""

    model = SentenceTransformer(EMBEDDING_MODEL)

    chunks = chunk_documents(
        DOCUMENTS,
        max_words=CHUNK_MAX_WORDS,
        overlap_sentences=CHUNK_OVERLAP_SENTENCES,
    )

    texts = [chunk["text"] for chunk in chunks]

    # FAISS expects float32 vectors.
    vectors = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    # The vectors are normalised to length 1, so the inner product used
    # by IndexFlatIP equals cosine similarity. The index is exact (no
    # approximation), which is fine for a handful of chunks.
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    # FAISS stores only vectors. Position i in the index corresponds to
    # chunks[i], which holds the text and source metadata.
    return model, index, chunks


@lru_cache(maxsize=1)
def get_reranker():
    """Load the cross-encoder used to re-rank retrieved chunks once."""

    return CrossEncoder(RERANK_MODEL)


def retrieve_chunks(
    question: str,
    top_k: int = 3,
    rerank: bool = True,
) -> list[dict]:
    """Return the most relevant document chunks with source metadata.

    FAISS selects candidate chunks by embedding similarity. When rerank
    is enabled, a cross-encoder scores each candidate against the
    question and the candidates are re-ordered by that score.
    """

    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question must be a non-empty string.")

    # bool is a subclass of int in Python, so True would otherwise be
    # accepted as top_k=1.
    if (
        not isinstance(top_k, int)
        or isinstance(top_k, bool)
        or top_k <= 0
    ):
        raise ValueError("top_k must be a positive integer.")

    model, index, chunks = get_retriever()

    # The question must be embedded exactly like the chunks, otherwise
    # the similarity scores are not comparable.
    query_vector = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    # Fetch extra candidates when re-ranking, so a relevant chunk that
    # the vector search ranked low can still reach the final top_k.
    candidates = max(top_k, RERANK_CANDIDATES) if rerank else top_k
    k = min(candidates, index.ntotal)
    scores, indices = index.search(query_vector, k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        # FAISS pads the result with -1 when it finds fewer than k hits.
        if idx < 0:
            continue

        chunk = chunks[int(idx)]

        results.append({
            **chunk,
            "similarity_score": float(score),
        })

    if rerank and results:
        # A cross-encoder reads the question and the chunk together,
        # which is more accurate than comparing two separate vectors.
        rerank_scores = get_reranker().predict(
            [(question, result["text"]) for result in results]
        )

        for result, rerank_score in zip(results, rerank_scores):
            result["rerank_score"] = float(rerank_score)

        results.sort(
            key=lambda result: result["rerank_score"],
            reverse=True,
        )

    return results[:top_k]
