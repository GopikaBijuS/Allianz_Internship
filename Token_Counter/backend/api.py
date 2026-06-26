from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from llm_client import generate_response

from database.db import (init_db, save_chat, get_history, delete_chat, update_chat)

init_db()

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str
    temperature: float
    top_p: float
    top_k: int
    max_tokens: int


@app.get("/")
def root():

    return {
        "message": "LLM Analyzer API Running"
    }


@app.post("/generate")
def generate(request: PromptRequest):

    try:
        result = generate_response(
            prompt=request.prompt,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            max_tokens=request.max_tokens
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    save_chat(
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


@app.get("/history")
def history():
    return get_history()


@app.delete("/history/{chat_id}")
def delete(chat_id: int):

    delete_chat(chat_id)

    return {
        "message": "Deleted Successfully"
    }

@app.put("/history/{chat_id}")
def update_history(chat_id: int, request: PromptRequest):

    try:
        result = generate_response(
            prompt=request.prompt,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            max_tokens=request.max_tokens
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    update_chat(
        chat_id,
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