import streamlit as st
import numpy as np

def configure_sidebar(df, results, criteria_columns):
    workflow_steps = st.sidebar.selectbox("Number of Workflow Steps", [2, 3], index=0)
    dist_method = st.sidebar.selectbox("Distribution Method", ["lognormal", "kde"], index=0)

    top_x_percent = st.sidebar.slider("Top X% Threshold", 1, 100, 2)
    step1_keep = st.sidebar.slider("Clones in Step 1", 1, len(results), 96)
    step2_keep = st.sidebar.slider("Clones in Step 2", 1, step1_keep, 48)
    step3_keep = st.sidebar.slider("Final Clones (Step 3)", 1, step2_keep, 6) if workflow_steps == 3 else step2_keep

    correlation_range = st.sidebar.slider("Range of Correlation Values", 0.0, 1.0, value=(0.1, 0.9), step=0.01)
    correlations = np.round(np.arange(correlation_range[0], correlation_range[1]+0.001, 0.01), 2)
    n_rep = st.sidebar.number_input("Number of Monte Carlo Simulations", 10, 50000, 1000)
    apply_criteria_at_step2 = st.sidebar.checkbox("Apply Criteria Filtering at Final Step", value=False)

    criteria_settings = []
    for col in criteria_columns:
        if st.sidebar.checkbox(f"Use {col}"):
            op = st.sidebar.selectbox(f"{col} Comparison", [">=", "<=", "="], key=col+"_comp")
            val = st.sidebar.number_input(f"{col} Threshold", value=1e-4, format="%.5f", key=col+"_thresh")
            criteria_settings.append((col, op, val))

    return {
        "workflow_steps": workflow_steps,
        "dist_method": dist_method,
        "top_x_percent": top_x_percent,
        "step1_keep": step1_keep,
        "step2_keep": step2_keep,
        "step3_keep": step3_keep,
        "correlations": correlations,
        "n_rep": n_rep,
        "apply_criteria_at_step2": apply_criteria_at_step2,
        "criteria_settings": criteria_settings
    }
