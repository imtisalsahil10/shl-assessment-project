import streamlit as st
import requests

st.title("SHL Assessment Recommender")

query = st.text_area("Enter job description or query:")
if st.button("Recommend"):
    res = requests.post("https://shl-assessment-project.onrender.com/recommend", json={"query": query})
    data = res.json()["recommendations"]
    st.write("Top Recommendations:")
    st.table(data)
