"""REST front door onto the same core/ logic the Streamlit app uses.

Run standalone with: uvicorn api.main:app --reload
This does not require the Streamlit app to be running - it's an independent
consumer of core.predictor / core.entities / core.router, demonstrating the
prediction logic is usable outside a Streamlit session (curl, Postman, a
future non-Streamlit client, ...).
"""
from fastapi import FastAPI
from pydantic import BaseModel

from core.entities import extract_entities
from core.logging_store import get_stats, log_prediction
from core.predictor import predict_intent
from core.router import route_intent

app = FastAPI(title="AI Function-Calling Assistant API")


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    intent: str
    confidence: float
    entities: dict
    route: str


@app.get("/health")
def health():
    return {"status": "ok"}





@app.get("/stats")
def stats():
    return get_stats()
