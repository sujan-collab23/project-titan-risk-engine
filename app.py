import streamlit as st
import pandas as pd

st.title("Project Titan Debugger")

file_path = "Project_Titan_live_model.xlsx"

try:
    # 1. Load the Excel file object
    xls = pd.ExcelFile(file_path)
    
    # 2. Display all detected sheet names so we can see the real names
    st.write("Successfully loaded file. Available sheet names are:")
    st.write(xls.sheet_names)
    
    # 3. Try to read using one of the names found
    # Once you see the output, update this if necessary
    df = pd.read_excel(file_path, sheet_name=xls.sheet_names[0]) 
    st.dataframe(df)

except Exception as e:
    st.error(f"Error: {e}")
