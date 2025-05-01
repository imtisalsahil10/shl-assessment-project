import streamlit as st
import requests

st.title("SHL Assessment Recommender")

API_URL = "https://shl-assessment-project.onrender.com/recommend"

# First define the input
query = st.text_area("Enter job description or query:")

# Only call the API when the button is clicked
if st.button("Recommend"):
    if query.strip() != "":
        res = requests.post(API_URL, json={"query": query})
        data = res.json()["recommendations"]
        st.write("Top Recommendations:")
        st.table(data)
    else:
        st.warning("Please enter a query.")
