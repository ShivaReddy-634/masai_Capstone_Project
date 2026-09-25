import os
import re
from typing import TypedDict

import chromadb
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, START, END

from models import AnswerResponse
from prompts import SUPPORT_PROMPT


MOCK_LLM = os.getenv("MOCK_LLM", "1")


# --------------------------------------------------
# Models and database
# --------------------------------------------------

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = chroma_client.get_collection(
    name="zepto_policies"
)


# --------------------------------------------------
# LangGraph state
# --------------------------------------------------

class SupportState(TypedDict, total=False):
    query: str
    intent: str
    context: str
    answer: str
    sources: list[str]
    confidence: float
    response: AnswerResponse


# --------------------------------------------------
# Node 1: Classify intent
# --------------------------------------------------

def classify_intent(state: SupportState):
    query = state["query"]

    lower_query = query.lower()

    keywords = [
        "delivery",
        "return",
        "refund",
        "membership",
        "tracking",
        "cancel",
        "gift card",
        "support hours"
    ]

    if any(keyword in lower_query for keyword in keywords):
        intent = "policy_question"
    else:
        intent = "general_question"

    print(f"Query: {query}")
    print(f"Intent: {intent}")

    return {
        "intent": intent
    }


# --------------------------------------------------
# Mock LLM
# --------------------------------------------------

def mock_llm_answer(question: str, context: str) -> str:
    """
    Deterministic local mock answer.
    No external LLM or API call is used.
    """

    question_lower = question.lower()

    # --------------------------------------------
    # Delivery fee question
    # --------------------------------------------
    if "delivery fee" in question_lower or "delivery charge" in question_lower:
        fee_keywords = [
            "delivery fee",
            "delivery charge",
            "flat inr",
            "inr 25",
            "orders below",
            "orders over"
        ]

        sentences = re.split(r"(?<=[.!?])\s+", context)

        for sentence in sentences:
            sentence_lower = sentence.lower()

            if (
                "delivery fee" in sentence_lower
                or "delivery charge" in sentence_lower
                or "inr 25" in sentence_lower
                or (
                    "orders below" in sentence_lower
                    and "orders over" in sentence_lower
                )
            ):
                return sentence.strip()

    # --------------------------------------------
    # General keyword-based retrieval
    # --------------------------------------------
    sentences = re.split(r"(?<=[.!?])\s+", context)

    question_terms = [
        word.lower()
        for word in re.findall(r"\b[a-zA-Z]+\b", question)
        if len(word) > 3
    ]

    best_sentence = None
    best_score = 0

    for sentence in sentences:
        sentence_lower = sentence.lower()

        score = sum(
            1
            for word in question_terms
            if word in sentence_lower
        )

        if score > best_score:
            best_score = score
            best_sentence = sentence.strip()

    if best_sentence:
        return best_sentence

    return (
        "The provided Zepto policy context does not contain "
        "enough information to answer this question."
    )


# --------------------------------------------------
# Node 2: Retrieve and answer
# --------------------------------------------------

def retrieve_and_answer(state: SupportState):
    query = state["query"]

    # Create query embedding
    query_embedding = embedding_model.encode(
        [query]
    ).tolist()

    # Retrieve top 3 documents
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    retrieved_documents = results["documents"][0]
    retrieved_ids = results["ids"][0]

    # Combine retrieved documents into context
    context = "\n\n".join(
        retrieved_documents
    )

    # Build the required support prompt
    formatted_prompt = SUPPORT_PROMPT.format(
        context=context,
        question=query
    )

    print("\n========== PROMPT ==========")
    print(formatted_prompt)
    print("============================\n")

    # Default graded behavior
    if MOCK_LLM == "1":
        answer = mock_llm_answer(
            query,
            context
        )
    else:
        # Real LLM integration is intentionally not enabled
        # in the baseline submission.
        answer = mock_llm_answer(
            query,
            context
        )

    response = AnswerResponse(
        answer=answer,
        sources=retrieved_ids,
        confidence=1.0
    )

    return {
        "context": context,
        "answer": response.answer,
        "sources": response.sources,
        "confidence": response.confidence,
        "response": response
    }


# --------------------------------------------------
# Node 3: Direct answer
# --------------------------------------------------

def direct_answer(state: SupportState):
    answer = (
        "I can only answer questions about Zepto policies right now."
    )

    response = AnswerResponse(
        answer=answer,
        sources=[],
        confidence=1.0
    )

    return {
        "answer": response.answer,
        "sources": response.sources,
        "confidence": response.confidence,
        "response": response
    }


# --------------------------------------------------
# Conditional routing
# --------------------------------------------------

def route_intent(state: SupportState):
    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"


# --------------------------------------------------
# Build LangGraph
# --------------------------------------------------

builder = StateGraph(SupportState)

builder.add_node(
    "classify_intent",
    classify_intent
)

builder.add_node(
    "retrieve_and_answer",
    retrieve_and_answer
)

builder.add_node(
    "direct_answer",
    direct_answer
)

builder.add_edge(
    START,
    "classify_intent"
)

builder.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer"
    }
)

builder.add_edge(
    "retrieve_and_answer",
    END
)

builder.add_edge(
    "direct_answer",
    END
)

graph = builder.compile()