"""Tests for retrieval and re-ranking."""

import pytest

from src.knowledge_base import retrieve_chunks


def test_retrieval_returns_relevant_hr_document():
    results = retrieve_chunks(
        "How far in advance must remote work be requested?",
        top_k=3,
    )

    assert results
    assert any(
        result["document_id"] == "HR-001"
        for result in results
    )


def test_retrieval_preserves_source_metadata():
    results = retrieve_chunks(
        "What are the password security requirements?",
        top_k=2,
    )

    assert results

    for result in results:
        assert result["document_id"]
        assert result["title"]
        assert result["page"] is not None
        assert result["text"]


def test_empty_question_is_rejected():
    with pytest.raises(ValueError):
        retrieve_chunks("")


def test_invalid_top_k_is_rejected():
    with pytest.raises(ValueError):
        retrieve_chunks("Remote work policy", top_k=0)


def test_retrieval_returns_chunks_not_whole_documents():
    results = retrieve_chunks(
        "How long do I have to submit an expense claim?",
        top_k=1,
    )

    assert results[0]["document_id"] == "FIN-001"
    assert results[0]["chunk_id"].startswith("FIN-001-c")
    assert "thirty calendar days" in results[0]["text"]


def test_reranking_puts_the_answer_chunk_first():
    question = "How far in advance must remote work be requested?"

    results = retrieve_chunks(question, top_k=3, rerank=True)

    assert "two working days in advance" in results[0]["text"]

    scores = [result["rerank_score"] for result in results]

    assert scores == sorted(scores, reverse=True)


def test_reranking_can_be_disabled():
    results = retrieve_chunks(
        "What are the password security requirements?",
        top_k=2,
        rerank=False,
    )

    assert len(results) == 2
    assert all("rerank_score" not in result for result in results)

    scores = [result["similarity_score"] for result in results]

    assert scores == sorted(scores, reverse=True)
