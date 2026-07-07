import time
import tiktoken

from routing.router import route_model

from agent.memory import (
    add_message
)

from agent.context_manager import (
    build_context
)

from agent.langchain_agent import (
    build_agent
)

encoding = tiktoken.get_encoding(
    "cl100k_base"
)


def count_tokens(text):
    return len(
        encoding.encode(text)
    )


def generate_response(
        session_id,
        prompt,
        temperature=0.7,
        top_p=0.9,
        top_k=40,
        max_tokens=500
):
    start_time = time.time()

    # --------------------
    # Save user message
    # --------------------

    add_message(
        session_id,
        "user",
        prompt
    )

    history = build_context(
        session_id
    )

    # --------------------
    # Build context string
    # --------------------

    conversation = ""

    for msg in history:
        conversation += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    full_prompt = f"""
Conversation History:

{conversation}

Current Question:
{prompt}
"""

    # --------------------
    # Model Routing
    # --------------------

    selected_model, prompt_type = (
        route_model(
            full_prompt
        )
    )

    # --------------------
    # Build Agent
    # --------------------

    executor = build_agent(
        selected_model,
        temperature
    )

    result = executor.invoke(
        {
            "input": full_prompt
        }
    )

    answer = result["output"]

    # --------------------
    # Save assistant message
    # --------------------

    add_message(
        session_id,
        "assistant",
        answer
    )

    end_time = time.time()

    input_tokens = count_tokens(
        full_prompt
    )

    output_tokens = count_tokens(
        answer
    )

    elapsed_time = round(
        end_time - start_time,
        2
    )

    intermediate_steps = []

    if "intermediate_steps" in result:
        for step in result[
            "intermediate_steps"
        ]:

            intermediate_steps.append(
                str(step)
            )

    return {
        "response": answer,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "elapsed_time": elapsed_time,
        "cost": "$0",
        "model": selected_model,
        "prompt_type": prompt_type,
        "agent_trace":
            intermediate_steps
    }