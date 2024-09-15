from src.chains import query_resolver_llm_chain, hallucination_llm_chain
from src import utils
from typing_extensions import TypedDict
from typing import List

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM answer
        documents: list of documents
        hallucination: whether answer is hallucinated
        slack_post: whether to post on slack
    """

    question: str
    answer: str
    documents: List[str]
    hallucination: bool
    slack_post: bool

def generate(state):
    """
    Generate answer using RAG on retrieved documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, answer and slack_post, that contains LLM answer
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]

    # RAG generation
    llm_response = dict(query_resolver_llm_chain.invoke({"context": documents, "query": question}))
    print(llm_response)
    answer = llm_response["answer"]
    slack_post = llm_response["slack_post"]

    
    return {"documents": documents, "question": question, "answer": answer, "slack_post": slack_post, "hallucination": False}

def check_hallucination(state):
    """
    Check if answer is hallucinated

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, hallucination, that contains hallucination check
    """

    question = state["question"]
    documents = state["documents"]
    answer = state["answer"]
    slack_post = state["slack_post"]

    # Hallucination check
    hallucination_check = dict(hallucination_llm_chain.invoke({"documents": documents, "answer": answer}))
    print(hallucination_check)
    if not hallucination_check['score']:
        answer = 'Sorry unable to answer this question based on context provided.'
    return {"documents": documents, "question": question, "answer": answer, "hallucination": hallucination_check['score'], "slack_post": slack_post}


def push_to_slack(state):
    """
    Push answer to slack

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, answer, that contains LLM answer
    """
    print("---PUSH TO SLACK---")

    question = state["question"]
    documents = state["documents"]
    answer = state["answer"]
    slack_post = state["slack_post"]
    hallucination = state["hallucination"]

    if (hallucination) and (slack_post):
        message = f"Question: {question}\nAnswer: {answer}"
        utils.add_message_to_slack(message)

    return {"documents": documents, "question": question, "answer": answer, "hallucination": state["hallucination"], "slack_post": slack_post}