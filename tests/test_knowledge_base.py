
import pytest

from src.knowledge_base import retrieve_documents


def test_retrieval_returns_relevant_hr_document():
    results = retrieve_documents(
        "How far in advance must remote work be requested?",
        top_k=3,
    )

    assert results
    assert any(
        result["document_id"] == "HR-001"
        for result in results
    )


def test_retrieval_preserves_source_metadata():
    results = retrieve_documents(
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
        retrieve_documents("")


def test_invalid_top_k_is_rejected():
    with pytest.raises(ValueError):
        retrieve_documents("Remote work policy", top_k=0)