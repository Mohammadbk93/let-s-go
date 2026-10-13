
import re


SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")


def split_sentences(text: str) -> list[str]:
    """Split text into sentences on terminal punctuation."""

    return [
        sentence.strip()
        for sentence in SENTENCE_BOUNDARY.split(text)
        if sentence.strip()
    ]


def chunk_text(
    text: str,
    max_words: int = 100,
    overlap_sentences: int = 1,
) -> list[str]:
    """Pack whole sentences into chunks of at most max_words words.

    Each chunk starts with the last overlap_sentences sentences of the
    previous chunk. A single sentence longer than max_words is kept
    whole as its own chunk.
    """

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text must be a non-empty string.")

    if max_words <= 0:
        raise ValueError("max_words must be a positive integer.")

    if overlap_sentences < 0:
        raise ValueError("overlap_sentences must not be negative.")

    chunks = []
    current = []
    current_words = 0

    for sentence in split_sentences(text):
        sentence_words = len(sentence.split())

        if current and current_words + sentence_words > max_words:
            chunks.append(" ".join(current))

            current = (
                current[-overlap_sentences:]
                if overlap_sentences
                else []
            )
            current_words = sum(len(s.split()) for s in current)

            if current_words + sentence_words > max_words:
                current = []
                current_words = 0

        current.append(sentence)
        current_words += sentence_words

    if current:
        chunks.append(" ".join(current))

    return chunks


def chunk_documents(
    documents: list[dict],
    max_words: int = 100,
    overlap_sentences: int = 1,
) -> list[dict]:
    """Split documents into chunks that keep their source metadata."""

    chunks = []

    for doc in documents:
        texts = chunk_text(
            doc["text"],
            max_words=max_words,
            overlap_sentences=overlap_sentences,
        )

        for position, text in enumerate(texts, start=1):
            chunks.append({
                **doc,
                "chunk_id": f"{doc['document_id']}-c{position}",
                "chunk_index": position,
                "text": text,
            })

    return chunks
