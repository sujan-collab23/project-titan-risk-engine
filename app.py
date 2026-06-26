import streamlit as st
import pandas as pd

# Path to the file
MODEL_PATH = "Project_Titan_live_model.xlsx"

st.subheader("Project Titan: Data Access Portal")

# 1. OPTION A: Interactive Raw Data Table
# This allows them to see the data directly in the browser
try:
    if st.checkbox("Show Raw Data Preview"):
        df = pd.read_excel(MODEL_PATH, sheet_name="M&A_ENGINE", header=6)
        st.dataframe(df)
except Exception as e:
    st.error(f"Could not load data: {e}")

# 2. OPTION B: Direct Download Link
# This provides a link for the user to download the file
with open(MODEL_PATH, "rb") as f:
    st.download_button(
        label="📥 Download Raw Model File",
        data=f,
        file_name="Project_Titan_Raw_Data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
