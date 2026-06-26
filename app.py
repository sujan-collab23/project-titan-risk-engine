import streamlit as st
import pandas as pd

# 1. Use the EXACT name your debugger found
SHEET_NAME = "M&A_ENGINE" 

try:
    # 2. Skip rows 0-5 so that the real headers (if they exist) 
    # or the actual data starts at the right place.
    # You might need to adjust 'header=' depending on which row your 
    # actual column titles start on.
    df = pd.read_excel("Project_Titan_live_model.xlsx", sheet_name=SHEET_NAME, header=6)
    
    st.success("Successfully loaded 'M&A_ENGINE'!")
    st.dataframe(df)

except Exception as e:
    st.error(f"Error loading sheet: {e})
