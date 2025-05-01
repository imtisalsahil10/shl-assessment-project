from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils import load_assessments, embed_query, search_assessments

app = FastAPI()

# Load assessment data and vector index
assessments, index, embeddings = load_assessments()

class Query(BaseModel):
    query: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/recommend")
def recommend(query: Query):
    top_results = search_assessments(query.query, embeddings, assessments, index)
    return {"recommendations": top_results}
