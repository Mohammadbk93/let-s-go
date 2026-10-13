"""Tests for the chunking pipeline."""

import pytest

from src.chunking import chunk_documents, chunk_text, split_sentences
from src.documents import DOCUMENTS
from src.knowledge_base import CHUNK_MAX_WORDS, CHUNK_OVERLAP_SENTENCES


TEXT = (
    "Alpha one two three. Bravo one two three. Charlie one two three. "
    "Delta one two three. Echo one two three."
)


def test_chunks_respect_word_limit():
    chunks = chunk_text(TEXT, max_words=8, overlap_sentences=0)

    assert len(chunks) == 3

    for chunk in chunks:
        assert len(chunk.split()) <= 8


def test_chunks_keep_whole_sentences():
    sentences = split_sentences(TEXT)

    for chunk in chunk_text(TEXT, max_words=8, overlap_sentences=0):
        assert split_sentences(chunk) == [
            sentence
            for sentence in sentences
            if sentence in chunk
        ]


def test_consecutive_chunks_overlap_by_one_sentence():
    chunks = chunk_text(TEXT, max_words=12, overlap_sentences=1)

    assert len(chunks) > 1

    for previous, current in zip(chunks, chunks[1:]):
        assert split_sentences(previous)[-1] == split_sentences(current)[0]


def test_no_sentence_is_lost():
    chunks = chunk_text(TEXT, max_words=12, overlap_sentences=1)
    joined = " ".join(chunks)

    for sentence in split_sentences(TEXT):
        assert sentence in joined


def test_short_text_is_a_single_chunk():
    assert chunk_text("Only one sentence.", max_words=50) == [
        "Only one sentence."
    ]


def test_long_sentence_is_kept_whole():
    chunks = chunk_text(
        "Short one. This sentence is far longer than the limit allows.",
        max_words=4,
        overlap_sentences=1,
    )

    assert chunks == [
        "Short one.",
        "This sentence is far longer than the limit allows.",
    ]


def test_invalid_arguments_are_rejected():
    with pytest.raises(ValueError):
        chunk_text("")

    with pytest.raises(ValueError):
        chunk_text(TEXT, max_words=0)

    with pytest.raises(ValueError):
        chunk_text(TEXT, overlap_sentences=-1)


def test_document_chunks_keep_source_metadata():
    chunks = chunk_documents(
        DOCUMENTS,
        max_words=CHUNK_MAX_WORDS,
        overlap_sentences=CHUNK_OVERLAP_SENTENCES,
    )

    assert len(chunks) > len(DOCUMENTS)
    assert len({chunk["chunk_id"] for chunk in chunks}) == len(chunks)

    titles = {doc["document_id"]: doc["title"] for doc in DOCUMENTS}

    for chunk in chunks:
        assert chunk["chunk_id"].startswith(chunk["document_id"])
        assert chunk["title"] == titles[chunk["document_id"]]
        assert chunk["page"] is not None
        assert len(chunk["text"].split()) <= CHUNK_MAX_WORDS
