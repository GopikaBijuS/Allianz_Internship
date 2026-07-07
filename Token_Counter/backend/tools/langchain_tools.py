from langchain.tools import tool

from tools.retrieve_docs import (
    retrieve_docs
)

from tools.summarize import (
    summarize_topic
)

from tools.compare import (
    compare_topics
)

from tools.report import (
    generate_report
)


@tool
def retrieve_documents(query: str):
    """
    Search local documents
    when additional context
    is needed.
    """
    return retrieve_docs(query)


@tool
def summarize_topic_tool(
        topic: str
):
    """"
    Summarize a topic ONLY when the user explicitly asks for a summary.
    Examples:
    - Summarize Docker
    - Give me a summary of FastAPI

    Do NOT use for:
    - What is Docker?
    - Explain FastAPI.
    - Compare Docker and FastAPI.
    """
    return summarize_topic(
        topic
    )


@tool
def compare_topics_tool(text: str):
    """
    Compare two topics.

    Action Input should be:
    Docker,FastAPI

    or

    Flask,FastAPI

    Provide only the topics separated by a comma.

    Examples:
    - Compare Docker and FastAPI
    - Differentiate Flask and FastAPI
    """
    try:
        topic1, topic2 = (
            text.split(",")
        )

        return compare_topics(
            topic1.strip(),
            topic2.strip()
        )

    except:
        return (
            "Input format should be:"
            " topic1, topic2"
        )


@tool
def generate_report_tool(
        topic: str
):
    """
    Generate a structured report ONLY when the user explicitly asks for a report.
    """
    return generate_report(
        topic
    )