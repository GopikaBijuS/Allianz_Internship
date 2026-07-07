import tiktoken
from agent.memory import get_history

MAX_CONTEXT_TOKENS = 3000
RECENT_MESSAGES = 8

encoding = tiktoken.get_encoding(
    "cl100k_base"
)


def count_tokens(text: str):
    return len(
        encoding.encode(text)
    )


def build_context(
        session_id: str
):
    history = get_history(
        session_id
    )

    if not history:
        return []

    total_tokens = sum(
        count_tokens(
            msg["content"]
        )
        for msg in history
    )

    if total_tokens <= MAX_CONTEXT_TOKENS:
        return history

    recent = history[
        -RECENT_MESSAGES:
    ]

    summary = {
        "role": "system",
        "content":
            "Older messages were removed "
            "to fit the context window."
    }

    return [summary] + recent