import streamlit as st
import requests

st.title("SHL Assessment Recommender")

API_URL = "https://shl-assessment-project.onrender.com"
res = requests.post(API_URL, json={"query": query})

query = st.text_area("Enter job description or query:")
if st.button("Recommend"):
    res = requests.post("http://localhost:8000/recommend", json={"query": query})
    data = res.json()["recommendations"]
    st.write("Top Recommendations:")
    st.table(data)
