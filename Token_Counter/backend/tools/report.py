from tools.retrieve_docs import (
    retrieve_docs
)


def generate_report(
        topic: str
):
    context = retrieve_docs(
        topic
    )

    if (
            not context
            or context ==
            "No relevant information found."
    ):
        return (
            f"No information found "
            f"about {topic}."
        )

    return f"""
# Research Report

## Topic
{topic}

## Findings
{context}

## Conclusion
This report summarizes the
available information about
{topic}.
"""