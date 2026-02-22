# app/dashboard.py
import streamlit as st
import requests

API_URL = "http://localhost:8000/api/upload"

st.title("DataSight Unified Dashboard")

uploaded_files = st.file_uploader(
    "Upload SQLite DB files", type=["db"], accept_multiple_files=True
)

if st.button("Analyze"):
    if uploaded_files:
        files = [
            ("files", (f.name, f.getvalue(), "application/octet-stream"))
            for f in uploaded_files
        ]

        response = requests.post(API_URL, files=files)

        if response.status_code == 200:
            data = response.json()
            st.json(data)
        else:
            st.error(response.text)
