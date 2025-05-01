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
@app.post("/recommend")
def recommend(query: Query):
    query_vec = model.encode([query.query])
    distances, indices = index.search(query_vec, 10)

    seen = set()
    results = []

    for idx in indices[0]:
        a = assessments[idx]
        unique_key = a["name"] + a["url"]
        if unique_key not in seen:
            seen.add(unique_key)
            results.append({
                "name": a["name"],
                "url": a["url"],
                "remote": a["remote"],
                "adaptive": a["adaptive"],
                "duration": a["duration"],
                "type": a["type"]
            })

    return {"recommendations": results}
