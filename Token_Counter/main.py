from fastapi import FastAPI
from pydantic import BaseModel

from token_counter import token_cost_estimator
from database import get_history
from database import save_analysis
from database import init_db

init_db()
app = FastAPI()

class TokenCount(BaseModel):
    text: str
    model: str

@app.post("/token_count/")
def count_tokens(request: TokenCount):
    text = request.text
    model = request.model

    result = token_cost_estimator(text, model)

    if result:
        save_analysis(text,result['model'],result['token_count'],result['estimated_cost'])
        return {
            "model": result['model'],
            "token_count": result['token_count'],
            "estimated_cost": result['estimated_cost']
        }
    else:
        return {"error": "Invalid model specified."}
@app.get("/")
def read_root():
    return {"message": "Welcome to the Token Counter API! Use the /token_count/ endpoint to estimate token counts and costs."}

@app.get("/history")
def history():
    return get_history()