from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from llm_client import generate_response

from database.db import (
    init_db,
    save_chat,
    get_history,
    get_session_history,
    delete_chat,
    delete_session,
    update_chat,
    save_agent_log,
    get_agent_logs
)

from agent.memory import (
    clear_history
)

init_db()

app = FastAPI()


class PromptRequest(BaseModel):
    session_id: str
    prompt: str
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    max_tokens: int = 500


@app.get("/")
def root():
    return {
        "message":
            "Research Assistant API Running"
    }


@app.post("/generate")
def generate(
        request: PromptRequest
):
    try:
        result = generate_response(
            session_id=request.session_id,
            prompt=request.prompt,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            max_tokens=request.max_tokens
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )

    save_chat(
        request.session_id,
        request.prompt,
        result["response"],
        result["model"],
        request.temperature,
        request.top_p,
        request.top_k,
        request.max_tokens,
        result["input_tokens"],
        result["output_tokens"],
        result["elapsed_time"],
        result["cost"]
    )

    save_agent_log(
        request.session_id,
        request.prompt,
        result["response"],
        result["model"],
        result.get(
            "agent_trace",
            []
        )
    )

    return result


@app.get("/history")
def history():
    return get_history()


@app.get(
    "/history/{session_id}"
)
def session_history(
        session_id: str
):
    return get_session_history(
        session_id
    )


@app.get(
    "/agent_logs/{session_id}"
)
def agent_logs(
        session_id: str
):
    return get_agent_logs(
        session_id
    )


@app.delete(
    "/history/{chat_id}"
)
def delete(
        chat_id: int
):
    delete_chat(chat_id)

    return {
        "message":
            "Deleted Successfully"
    }


@app.delete(
    "/session/{session_id}"
)
def clear_session(
        session_id: str
):
    delete_session(
        session_id
    )

    clear_history(
        session_id
    )

    return {
        "message":
            "Session Deleted"
    }


@app.put(
    "/history/{chat_id}"
)
def update_history(
        chat_id: int,
        request: PromptRequest
):
    try:
        result = generate_response(
            session_id=request.session_id,
            prompt=request.prompt,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            max_tokens=request.max_tokens
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )

    update_chat(
        chat_id,
        request.session_id,
        request.prompt,
        result["response"],
        result["model"],
        request.temperature,
        request.top_p,
        request.top_k,
        request.max_tokens,
        result["input_tokens"],
        result["output_tokens"],
        result["elapsed_time"],
        result["cost"]
    )

    return result