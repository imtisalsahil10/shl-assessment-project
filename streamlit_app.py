import streamlit as st
import requests

st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")
st.title("🔍 SHL Assessment Recommender")

API_URL = "https://shl-assessment-project.onrender.com/recommend"  # Replace with your Render URL

# Input box for user query
query = st.text_area("Enter job description or query:")

# On button click, send request to FastAPI backend
if st.button("Recommend"):
    if query.strip() == "":
        st.warning("Please enter a valid query.")
    else:
        try:
            res = requests.post(API_URL, json={"query": query})
            res.raise_for_status()  # Check for HTTP errors
            
            # Try parsing JSON
            data = res.json()
            if "recommendations" in data:
                recommendations = data["recommendations"]
                if recommendations:
                    st.success("✅ Recommendations retrieved:")
                    st.table(recommendations)
                else:
                    st.info("No relevant assessments found.")
            else:
                st.error("Unexpected response format: 'recommendations' key not found.")

        except requests.exceptions.RequestException as e:
            st.error(f"API connection error: {e}")
        except ValueError:
            st.error("❌ Invalid JSON response from the backend API.")
