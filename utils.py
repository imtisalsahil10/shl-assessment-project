import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def load_assessments():
    with open("assessments.json", "r") as f:
        assessments = json.load(f)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    descriptions = [a["description"] for a in assessments]
    embeddings = model.encode(descriptions)
    index = faiss.IndexFlatL2(embeddings[0].shape[0])
    index.add(np.array(embeddings))
    return assessments, index, model

def embed_query(query_text, model):
    return np.array([model.encode(query_text)])

def search_assessments(query, model, assessments, index, k=10):
    query_vec = embed_query(query, model)
    distances, indices = index.search(query_vec, k)
    results = []
    for idx in indices[0]:
        a = assessments[idx]
        results.append({
            "name": a["name"],
            "url": a["url"],
            "remote": a["remote"],
            "adaptive": a["adaptive"],
            "duration": a["duration"],
            "type": a["type"]
        })
    return results
