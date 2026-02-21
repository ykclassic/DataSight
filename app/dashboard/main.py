# app/dashboard/main.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from io import BytesIO

# ----------------------------------------
# Configuration
# ----------------------------------------
API_URL = "https://datasight-z9o6.onrender.com/upload"

st.set_page_config(page_title="DataSight Dashboard", layout="wide")
st.title("📊 DataSight AI Dashboard")
st.markdown(
    "Upload SQLite `.db` files to see schema, profiling stats, trends, correlations, and cross-file relationships visually."
)

# ----------------------------------------
# File Upload
# ----------------------------------------
uploaded_files = st.file_uploader(
    "Upload SQLite DB Files", type=["db"], accept_multiple_files=True
)

if uploaded_files:
    with st.spinner("Analyzing files..."):
        files_payload = [("files", (f.name, f, "application/octet-stream")) for f in uploaded_files]
        response = requests.post(API_URL, files=files_payload)

    if response.status_code == 200:
        results = response.json()
        st.success("Analysis Complete ✅")

        # ----------------------------------------
        # Schema & Profile
        # ----------------------------------------
        st.header("📋 Schema & Profiling")
        for filename, data in results.items():
            if filename == "ai_insights":
                continue

            st.subheader(f"{filename}")
            st.markdown("**Tables:**")
            for table_name, table_info in data["schema"].items():
                st.markdown(f"- {table_name}: {len(table_info)} columns")
                if table_name in data["profile"]:
                    st.dataframe(pd.DataFrame(data["profile"][table_name]))

        # ----------------------------------------
        # AI Insights
        # ----------------------------------------
        st.header("🤖 AI Insights")
        insights = results["ai_insights"]

        # 1️⃣ Per-file high correlations
        for filename, file_data in insights.items():
            if filename == "cross_file_relationships":
                continue

            st.subheader(f"{filename}")
            for table_name, table_insight in file_data.items():
                st.markdown(f"**Table:** {table_name}")

                # High correlations
                if table_insight.get("high_correlations"):
                    st.markdown("**High Correlations:**")
                    corr_df = pd.DataFrame(table_insight["high_correlations"], columns=["Column1","Column2","Correlation"])
                    st.dataframe(corr_df)

                    # Correlation heatmap
                    try:
                        numeric_cols = list(set(corr_df["Column1"].tolist() + corr_df["Column2"].tolist()))
                        corr_matrix = pd.DataFrame(numeric_cols, columns=["col"])
                        # For demonstration, using placeholder heatmap
                        fig = px.imshow([[v for v in range(len(numeric_cols))]]*len(numeric_cols),
                                        x=numeric_cols, y=numeric_cols,
                                        color_continuous_scale='RdBu_r',
                                        labels=dict(x="Columns", y="Columns", color="Correlation"))
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.warning(f"Heatmap generation failed: {e}")

                # Trends
                if table_insight.get("trends"):
                    st.markdown("**Trends:**")
                    trend_df = pd.DataFrame(table_insight["trends"])
                    st.dataframe(trend_df)

                    # Trend line charts
                    for _, row in trend_df.iterrows():
                        # Example line chart placeholder
                        fig = px.line(y=[i*(1+row['slope']) for i in range(10)],
                                      x=list(range(10)),
                                      labels={"x": "Index", "y": row['column']},
                                      title=f"{row['column']} Trend")
                        st.plotly_chart(fig, use_container_width=True)

        # 2️⃣ Cross-file relationships
        if insights.get("cross_file_relationships"):
            st.header("🔗 Cross-File Relationships")
            cross_df = pd.DataFrame(insights["cross_file_relationships"])
            st.dataframe(cross_df)

    else:
        st.error(f"Analysis failed: {response.text}")
