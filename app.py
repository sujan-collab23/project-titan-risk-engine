import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# 1. SIMULATION LOGIC
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

# 2. UI LAYOUT
st.title("Project Titan // M&A Simulation Architecture")

if st.button("Execute Monte Carlo Risk Assessment"):
    with st.spinner("Processing..."):
        p10, p50, p90 = run_simulation()
        c1, c2, c3 = st.columns(3)
        c1.metric("P10 Floor", f"${p10:,.2f}M")
        c2.metric("P50 Median", f"${p50:,.2f}M")
        c3.metric("P90 Ceiling", f"${p90:,.2f}M")

# 3. VISUAL ARCHITECTURE
if st.button("Generate Visual Risk Architecture"):
    # Waterfall Bridge
    fig = go.Figure(go.Waterfall(
        name="Value Bridge", orientation="v",
        measure=["relative", "relative", "relative", "relative", "total"],
        x=["JPM Base", "Zion Base", "Synergies", "Debt Drag", "Pro Forma"],
        y=[57000, 895, 501, -146, 58250]
    ))
    st.plotly_chart(fig)
    
    # Financing Mix
    fig_pie = px.pie(values=[0.4, 0.6], names=['Cash', 'Stock'], title="Transaction Financing Mix")
    st.plotly_chart(fig_pie)
