from tools.retrieve_docs import (
    retrieve_docs
)


def summarize_topic(
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

    lines = context.split(
        "\n"
    )

    summary = []

    for line in lines:
        line = line.strip()

        if (
                line
                and not line.startswith(
                    "Source:"
                )
                and not line.startswith(
                    "Content:"
                )
        ):
            summary.append(
                line
            )

    summary = summary[:5]

    return (
        "Summary:\n\n- "
        + "\n- ".join(
            summary
        )
    )