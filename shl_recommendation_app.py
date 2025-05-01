# SHL Recommendation System (FastAPI + Streamlit)

# --- 1. Requirements ---
# pip install fastapi uvicorn streamlit sentence-transformers faiss-cpu requests beautifulsoup4

# --- 2. Sample Assessment Data (Mock) ---
# You can later scrape from SHL's site
shl_assessments = [
    {
        "name": "Java Developer Test",
        "url": "https://www.shl.com/java-developer-test",
        "remote": "Yes",
        "adaptive": "Yes",
        "duration": "40 mins",
        "type": "Technical"
    },
    {
        "name": "Full Stack Developer Test",
        "url": "https://www.shl.com/fullstack-test",
        "remote": "Yes",
        "adaptive": "No",
        "duration": "60 mins",
        "type": "Technical"
    },
    {
        "name": "Cognitive Ability + Personality",
        "url": "https://www.shl.com/cognitive-personality",
        "remote": "Yes",
        "adaptive": "Yes",
        "duration": "45 mins",
        "type": "Cognitive + Personality"
    },
    # Add more as needed...
]

# --- 3. Embedding Setup ---
from sentence_transformers import SentenceTransformer, util
import numpy as np
model = SentenceTransformer('all-MiniLM-L6-v2')

assessment_texts = [
    f"{a['name']} {a['type']} {a['duration']} Remote:{a['remote']} Adaptive:{a['adaptive']}"
    for a in shl_assessments
]
embeddings = model.encode(assessment_texts, convert_to_tensor=True)

# --- 4. FastAPI Backend ---
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommend")
def recommend(q: Query):
    query_emb = model.encode(q.query, convert_to_tensor=True)
    scores = util.cos_sim(query_emb, embeddings)[0].cpu().numpy()
    top_indices = np.argsort(scores)[::-1][:10]
    results = [shl_assessments[i] for i in top_indices]
    return {"recommendations": results}

# --- 5. Streamlit Frontend ---
# Save this part separately as `streamlit_app.py`

"""
import streamlit as st
import requests

st.title("🔍 SHL Assessment Recommender")
query = st.text_area("Enter job description or query:", height=200)

if st.button("Recommend Assessments"):
    with st.spinner("Finding best matches..."):
        res = requests.post("http://localhost:8000/recommend", json={"query": query})
        data = res.json()
        if "recommendations" in data:
            st.success("Top Recommendations:")
            st.table([
                {
                    "Name": f"[{a['name']}]({a['url']})",
                    "Remote": a['remote'],
                    "Adaptive": a['adaptive'],
                    "Duration": a['duration'],
                    "Type": a['type']
                }
                for a in data["recommendations"]
            ])
"""

# --- 6. Run Instructions ---
# Start API server:
# uvicorn shl_recommendation_app:app --reload

# Start Streamlit frontend:
# streamlit run streamlit_app.py

# Optional: Replace mock `shl_assessments` with scraped and processed SHL catalog
