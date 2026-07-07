from collections import defaultdict

chat_memory = defaultdict(list)


def add_message(
        session_id: str,
        role: str,
        content: str
):
    chat_memory[session_id].append(
        {
            "role": role,
            "content": content
        }
    )


def get_history(
        session_id: str
):
    return chat_memory.get(
        session_id,
        []
    )


def clear_history(
        session_id: str
):
    if session_id in chat_memory:
        del chat_memory[session_id]