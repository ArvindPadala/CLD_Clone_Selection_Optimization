import streamlit as st
import numpy as np

def configure_sidebar(df, results, criteria_columns):
    """Configure the sidebar with all simulation parameters in an organized manner."""
    
    # Workflow Configuration
    st.sidebar.markdown("### 🔄 Workflow Configuration")
    workflow_steps = st.sidebar.selectbox(
        "Number of Workflow Steps", 
        [2, 3], 
        index=0,
        help="Choose between 2-step or 3-step clone selection workflow"
    )
    
    # Distribution Method
    st.sidebar.markdown("### 📊 Distribution Modeling")
    dist_method = st.sidebar.selectbox(
        "Distribution Method", 
        ["lognormal", "kde"], 
        index=0,
        help="Lognormal: Parametric approach, KDE: Non-parametric approach"
    )
    
    # Success Criteria
    st.sidebar.markdown("### 🎯 Success Criteria")
    top_x_percent = st.sidebar.slider(
        "Top X% Threshold", 
        1, 100, 2,
        help="Percentage of top-performing clones to consider as 'successful'"
    )
    
    # Clone Selection Parameters
    st.sidebar.markdown("### 🔬 Clone Selection Parameters")
    
    # Step 1 parameters
    st.sidebar.markdown("**Step 1 (Initial Screening):**")
    step1_keep = st.sidebar.slider(
        "Clones to Keep in Step 1", 
        1, min(len(results), 2000), 96,
        help="Number of top clones to advance from initial screening"
    )
    
    # Step 2 parameters
    st.sidebar.markdown("**Step 2 (Secondary Screening):**")
    step2_keep = st.sidebar.slider(
        "Clones to Keep in Step 2", 
        1, step1_keep, min(48, step1_keep),
        help="Number of clones to advance from secondary screening"
    )
    
    # Step 3 parameters (only for 3-step workflow)
    if workflow_steps == 3:
        st.sidebar.markdown("**Step 3 (Final Selection):**")
        step3_keep = st.sidebar.slider(
            "Final Clones to Select", 
            1, step2_keep, min(6, step2_keep),
            help="Number of final clones to select"
        )
    else:
        step3_keep = step2_keep
    
    # Correlation Analysis
    st.sidebar.markdown("### 🔗 Correlation Analysis")
    correlation_range = st.sidebar.slider(
        "Correlation Range", 
        0.0, 1.0, 
        value=(0.1, 0.9), 
        step=0.01,
        help="Range of correlation values between assay steps to analyze"
    )
    
    # Generate correlation values
    step_size = st.sidebar.selectbox(
        "Correlation Step Size", 
        [0.01, 0.02, 0.05, 0.1], 
        index=0,
        help="Step size for correlation analysis (smaller = more detailed)"
    )
    correlations = np.round(np.arange(correlation_range[0], correlation_range[1]+step_size, step_size), 2)
    
    # Simulation Parameters
    st.sidebar.markdown("### ⚙️ Simulation Parameters")
    n_rep = st.sidebar.number_input(
        "Monte Carlo Repetitions", 
        100, 100000, 1000,
        step=100,
        help="Number of Monte Carlo simulations (higher = more accurate but slower)"
    )
    
    # Criteria Filtering
    st.sidebar.markdown("### 📋 Criteria Filtering")
    apply_criteria_at_step2 = st.sidebar.checkbox(
        "Apply Criteria at Final Step", 
        value=False,
        help="Apply filtering criteria at the final selection step"
    )
    
    # Criteria settings
    criteria_settings = []
    if criteria_columns:
        st.sidebar.markdown("**Filtering Criteria:**")
        for col in criteria_columns:
            if st.sidebar.checkbox(f"Use {col}", key=f"use_{col}"):
                col1, col2 = st.sidebar.columns(2)
                with col1:
                    op = st.selectbox(
                        f"{col} Operator", 
                        [">=", "<=", "="], 
                        key=f"{col}_comp"
                    )
                with col2:
                    # Get reasonable default value based on data
                    col_data = df[col].dropna()
                    if len(col_data) > 0:
                        default_val = float(col_data.quantile(0.5))
                    else:
                        default_val = 0.0
                    
                    val = st.number_input(
                        f"{col} Threshold", 
                        value=default_val, 
                        format="%.5f", 
                        key=f"{col}_thresh"
                    )
                criteria_settings.append((col, op, val))
    
    # Advanced Options
    with st.sidebar.expander("🔧 Advanced Options", expanded=False):
        st.markdown("**Performance Settings:**")
        
        # Parallel processing option
        use_parallel = st.checkbox(
            "Use Parallel Processing", 
            value=False,
            help="Enable parallel processing for faster simulations (experimental)"
        )
        
        # Memory optimization
        optimize_memory = st.checkbox(
            "Memory Optimization", 
            value=True,
            help="Optimize memory usage for large datasets"
        )
        
        # Random seed for reproducibility
        random_seed = st.number_input(
            "Random Seed", 
            value=42,
            help="Set random seed for reproducible results"
        )
    
    # Information Panel
    with st.sidebar.expander("ℹ️ Information", expanded=False):
        st.markdown(f"""
        **Current Configuration:**
        - **Total Clones:** {len(results):,}
        - **Workflow Steps:** {workflow_steps}
        - **Step 1 → Step 2:** {len(results):,} → {step1_keep}
        - **Step 2 → Step 3:** {step1_keep} → {step2_keep}
        """)
        
        if workflow_steps == 3:
            st.markdown(f"- **Step 3 → Final:** {step2_keep} → {step3_keep}")
        
        st.markdown(f"""
        - **Correlation Range:** {correlation_range[0]:.2f} - {correlation_range[1]:.2f}
        - **Simulations:** {n_rep:,}
        - **Success Threshold:** Top {top_x_percent}%
        """)
        
        if criteria_settings:
            st.markdown("**Active Filters:**")
            for col, op, val in criteria_settings:
                st.markdown(f"- {col} {op} {val}")
    
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
        "criteria_settings": criteria_settings,
        "use_parallel": use_parallel,
        "optimize_memory": optimize_memory,
        "random_seed": random_seed
    }
