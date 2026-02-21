# app/main.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# -------------------------------
# Configuration
# -------------------------------
API_URL = "https://datasight-z9o6.onrender.com/upload"  # Use /api/upload if router prefix is /api

st.set_page_config(page_title="DataSight Dashboard", layout="wide")
st.title("📊 DataSight AI Dashboard")

# -------------------------------
# File uploader
# -------------------------------
uploaded_files = st.file_uploader(
    "Upload SQLite database files (.db)", 
    type=["db"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.info("Uploading files and analyzing...")

    files_payload = [("files", (f.name, f, "application/octet-stream")) for f in uploaded_files]

    try:
        response = requests.post(API_URL, files=files_payload)
        response.raise_for_status()
        analysis = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Analysis failed: {e}")
        st.stop()

    # -------------------------------
    # Display results per file
    # -------------------------------
    for file_name, file_data in analysis.items():
        if file_name == "ai_insights":
            continue  # Cross-file insights handled later

        st.header(f"📁 File: {file_name}")

        # Schema
        st.subheader("Schema")
        for table_name, columns in file_data.get("schema", {}).items():
            st.markdown(f"**Table: {table_name}** → Columns: {', '.join(columns)}")

        # Table profiling
        st.subheader("Table Profiling")
        for table_name, profile in file_data.get("profile", {}).items():
            st.markdown(f"**Table: {table_name}**")
            st.json(profile)

        # AI Insights
        st.subheader("AI Insights")
        ai_insights = file_data.get("ai_insights", {})
        for table_name, insights in ai_insights.items():
            if table_name == "cross_file_relationships":
                continue
            st.markdown(f"**Table: {table_name}**")

            # Correlation matrix
            if "correlation_matrix" in insights:
                corr_df = pd.DataFrame(insights["correlation_matrix"])
                fig = px.imshow(
                    corr_df, text_auto=True, color_continuous_scale='RdBu_r',
                    title=f"{table_name} Correlation Matrix"
                )
                st.plotly_chart(fig, use_container_width=True)

            # Trends + predictions
            if "trends" in insights:
                for trend in insights["trends"]:
                    column = trend["column"]
                    slope = trend.get("slope")
                    pred = trend.get("next_prediction")
                    st.markdown(f"- **{column}** | Slope: {slope:.3f} | Next Prediction: {pred}")

            # NLP Summary
            if "summary" in insights:
                st.markdown(f"**Summary:** {insights['summary']}")

    # -------------------------------
    # Cross-file relationships
    # -------------------------------
    cross_rel = analysis.get("ai_insights", {}).get("cross_file_relationships", [])
    if cross_rel:
        st.subheader("🔗 Cross-File Relationships")
        for rel in cross_rel:
            st.markdown(
                f"- `{rel['file1']}/{rel['table1']}` ↔ `{rel['file2']}/{rel['table2']}` "
                f"| Shared columns: {', '.join(rel['shared_columns'])}"
            )
