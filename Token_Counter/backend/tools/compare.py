from tools.retrieve_docs import (
    retrieve_docs
)


def compare_topics(
        topic1: str,
        topic2: str
):
    context1 = retrieve_docs(
        topic1
    )

    context2 = retrieve_docs(
        topic2
    )

    return f"""
## Comparison

### {topic1}
{context1}

------------------------

### {topic2}
{context2}

------------------------

Compare these topics based on:

1. Purpose
2. Features
3. Advantages
4. Use Cases
5. Limitations
"""