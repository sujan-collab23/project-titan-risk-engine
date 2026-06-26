import streamlit as st
import pandas as pd
import numpy as np

# --- 1. SIMULATION ENGINE ---
def run_simulation():
    trials = 50000
    jpm_base_ni = 57000.00   
    zion_base_ni = 895.00     
    synergies = 501.26        
    debt_drag = -146.81       
    
    np.random.seed(42)
    jpm_shocks = np.random.normal(0, 0.142, trials)
    zion_shocks = np.random.normal(0, 0.228, trials) * 0.68 + jpm_shocks * 0.32 
    
    sim_jpm = jpm_base_ni * np.exp(jpm_shocks - 0.5 * (0.142**2))
    sim_zion = zion_base_ni * np.exp(zion_shocks - 0.5 * (0.228**2))
    sim_proforma = sim_jpm + sim_zion + synergies + debt_drag
    
    return np.percentile(sim_proforma, [10, 50, 90])

# --- 2. STREAMLIT UI ---
st.title("Project Titan // M&A Simulation Architecture")

# Simulation Section
if st.button("Execute Monte Carlo Risk Assessment", type="primary"):
    with st.spinner("Running 50,000 trials..."):
        p10, p50, p90 = run_simulation()
        c1, c2, c3 = st.columns(3)
        c1.metric("P10 Floor", f"${p10:,.2f}M")
        c2.metric("P50 Median", f"${p50:,.2f}M")
        c3.metric("P90 Ceiling", f"${p90:,.2f}M")

st.divider()

# Data Portal Section
st.subheader("Project Titan: Data Access Portal")
if st.checkbox("Show Raw Data Preview"):
    df = pd.read_excel("Project_Titan_live_model.xlsx", sheet_name="M&A_ENGINE")
    st.dataframe(df)

with open("Project_Titan_live_model.xlsx", "rb") as f:
    st.download_button("📥 Download Raw Model File", f, "Project_Titan_Raw_Data.xlsx")
