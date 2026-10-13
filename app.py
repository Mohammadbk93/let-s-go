
import logging

import streamlit as st

from src.generation import generate_answer
from src.knowledge_base import retrieve_documents

logger = logging.getLogger(__name__)


st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="📚",
    layout="wide",
)

st.title("Enterprise Knowledge Assistant")

st.write(
    "Ask questions about the sample HR, IT, and Finance policies. "
    "Answers are generated using retrieved document evidence."
)

with st.sidebar:
    st.header("Settings")

    top_k = st.slider(
        "Number of documents to retrieve",
        min_value=1,
        max_value=3,
        value=3,
    )

    st.caption(
        "Prototype only: sample documents, no user authentication, "
        "and no production access controls."
    )

question = st.text_area(
    "Your question",
    placeholder="How far in advance must I request remote work?",
    height=100,
)

if st.button("Ask question", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Searching documents..."):
                retrieved_documents = retrieve_documents(
                    question,
                    top_k=top_k,
                )

            with st.spinner("Generating answer..."):
                answer = generate_answer(
                    question,
                    retrieved_documents,
                )

            st.subheader("Answer")
            st.write(answer)

            st.subheader("Retrieved evidence")

            for doc in retrieved_documents:
                with st.expander(
                    f"{doc['title']} — Page {doc['page']}"
                ):
                    st.caption(
                        f"Document ID: {doc['document_id']} | "
                        f"Similarity: {doc['similarity_score']:.3f}"
                    )
                    st.write(doc["text"])

        except Exception:
            logger.exception("Request failed")
            st.error(
                "The request could not be completed. "
                "Please try again later."
            )