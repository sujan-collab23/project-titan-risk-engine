import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Project Titan | Strategic Risk Architecture", layout="wide")

# 2. SIMULATION ENGINE
def run_simulation():
    trials = 50000
    jpm_base_ni, zion_base_ni = 57000.0, 895.0
    synergies, debt_drag = 501.26, -146.81
    
    np.random.seed(42)
    jpm_shocks = np.random.normal(0, 0.142, trials)
    zion_shocks = np.random.normal(0, 0.228, trials) * 0.68 + jpm_shocks * 0.32 
    sim_proforma = (jpm_base_ni * np.exp(jpm_shocks - 0.5*(0.142**2))) + \
                   (zion_base_ni * np.exp(zion_shocks - 0.5*(0.228**2))) + synergies + debt_drag
    return np.percentile(sim_proforma, [10, 50, 90])

# 3. DASHBOARD UI
st.title("Project Titan: M&A Strategic Risk Architecture")
st.markdown("---")

col1, col2, col3 = st.columns(3)

if st.button("Execute Monte Carlo Risk Assessment"):
    with st.spinner("Calculating 50,000 trials..."):
        p10, p50, p90 = run_simulation()
        col1.metric("P10 Floor", f"${p10:,.2f}M")
        col2.metric("P50 Median", f"${p50:,.2f}M")
        col3.metric("P90 Ceiling", f"${p90:,.2f}M")

if st.button("Generate Visual Risk Architecture"):
    # Waterfall Chart
    fig = go.Figure(go.Waterfall(
        name="Value Bridge", orientation="v",
        measure=["relative", "relative", "relative", "relative", "total"],
        x=["JPM Base", "Zion Base", "Synergies", "Debt Drag", "Pro Forma"],
        y=[57000, 895, 501, -146, 58250]
    ))
    st.plotly_chart(fig, use_container_width=True)
    
    # Financing Pie Chart
    fig_pie = px.pie(values=[0.4, 0.6], names=['Cash', 'Stock'], title="Transaction Financing Mix")
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# 4. REFERENCE DATA PORTAL
st.subheader("Reference Data")
with st.expander("Click to view Raw Model Data (M&A_ENGINE)"):
    try:
        df = pd.read_excel("Project_Titan_live_model.xlsx", sheet_name="M&A_ENGINE", header=6)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Data Load Error: {e}")
