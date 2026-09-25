from fastapi import FastAPI
from pydantic import BaseModel

from graph import graph
from models import AnswerResponse

class AskRequest(BaseModel):
    query: str

app = FastAPI(
    title="Zepto Support Assistant",
    description="RAG-based Zepto policy support assistant",
    version="1.0.0"
)

@app.post("/ask", response_model=AnswerResponse)
def ask(request: AskRequest):

    result = graph.invoke({
        "query": request.query
    })

    return result["response"]

