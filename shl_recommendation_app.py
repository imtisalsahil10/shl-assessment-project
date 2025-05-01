from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

app = FastAPI()

class Query(BaseModel):
    query: str

# Load assessment data
with open("assessments.json", "r") as f:
    assessments = json.load(f)

# Load model and build vector index
model = SentenceTransformer("all-MiniLM-L6-v2")
descriptions = [a["description"] for a in assessments]
embeddings = model.encode(descriptions)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/recommend")
def recommend(query: Query):
    query_vec = model.encode([query.query])
    distances, indices = index.search(query_vec, 10)

    seen = set()
    results = []

    for idx in indices[0]:
        a = assessments[idx]
        key = a["name"] + a["url"]
        if key not in seen:
            seen.add(key)
            results.append({
                "name": a["name"],
                "url": a["url"],
                "remote": a["remote"],
                "adaptive": a["adaptive"],
                "duration": a["duration"],
                "type": a["type"]
            })

    return {"recommendations": results}
