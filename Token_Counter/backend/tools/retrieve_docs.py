from vector_store.chroma_manager import (
    load_vector_store
)

vector_store = load_vector_store()


def retrieve_docs(query: str):
    docs = vector_store.similarity_search(
        query,
        k=3
    )

    if not docs:
        return "No relevant information found."

    context = []

    for doc in docs:
        source = doc.metadata.get("source","Unknown")

        context.append(
            f"""
            Source: {source}

            Content:
            {doc.page_content}
            """
                    )

    return "\n\n".join(
        context
    )