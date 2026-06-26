import time

import tiktoken
from ollama import chat

from routing.router import route_model


def count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def generate_response(
        prompt,
        temperature=0.7,
        top_p=0.9,
        top_k=40,
        max_tokens=500
):

    start_time = time.time()

    # --------------------------
    # Model Routing
    # --------------------------

    selected_model, prompt_type = route_model(prompt)

    try:
        response = chat(
            model=selected_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "num_predict": max_tokens
            }
        )

    except Exception as exc:
        raise RuntimeError(
            f"LLM generation failed for model "
            f"'{selected_model}': {exc}"
        ) from exc

    end_time = time.time()

    answer = response["message"]["content"]

    input_tokens = count_tokens(prompt)
    output_tokens = count_tokens(answer)

    elapsed_time = round(
        end_time - start_time,
        2
    )

    return {
        "response": answer,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "elapsed_time": elapsed_time,
        "cost": "$0",
        "model": selected_model,
        "prompt_type": prompt_type
    }