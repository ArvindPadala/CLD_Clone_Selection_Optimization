import streamlit as st
import pandas as pd
import numpy as np
from loader import load_data
from sidebar import configure_sidebar
from plots import (
    plot_criteria_distributions, 
    plot_distribution_comparison, 
    plot_success_prob_vs_corr, 
    plot_success_histogram,
    plot_workflow_comparison,
    plot_sensitivity_analysis,
    plot_correlation_heatmap,
    plot_clone_selection_flow
)
from simulation import simulate_workflow, generate_samples, fit_lognormal, run_sensitivity_analysis
from ai_agent import create_ai_agent_interface

# Page configuration
st.set_page_config(
    page_title="CLD Clone Selection Optimization Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .info-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🧬 CLD Clone Selection Optimization Dashboard</h1>', unsafe_allow_html=True)
    
    # Introduction
    with st.expander("📋 Project Overview", expanded=False):
        st.markdown("""
        **Cell Line Development (CLD) Clone Selection Process Optimization**
        
        This dashboard simulates clone selection workflows to optimize the process of identifying 
        the best-performing cell lines for therapeutic protein production. The simulation helps 
        evaluate how different parameters affect the probability of selecting clones among the top performers.
        
        **Key Features:**
        - 📊 Multi-step workflow simulation (2 or 3 steps)
        - 🔄 Monte Carlo simulation with configurable correlation
        - 📈 Sensitivity analysis for parameter optimization
        - 🎯 Success probability visualization
        - 📋 Criteria-based filtering at any workflow step
        - 🤖 AI Agent for intelligent recommendations and analysis
        """)
    
    # File upload section
    st.sidebar.markdown("## 📁 Data Upload")
    uploaded_file = st.sidebar.file_uploader(
        "Upload Excel File with Assay Results", 
        type=["xlsx"],
        help="Upload an Excel file containing 'Results' column and optional 'Criteria' columns"
    )
    
    if not uploaded_file:
        st.info("👆 Please upload an Excel file to begin the analysis.")
        st.markdown("""
        **Expected File Format:**
        - Column named **"Results"** containing numeric assay values
        - Optional columns starting with **"Criteria"** (e.g., Criteria1, Criteria2...) for filtering
        - Multiple sheets supported
        """)
        return
    
    # Load and process data
    try:
        df, selected_sheet, criteria_columns = load_data(uploaded_file)
        
        # Store data in session state for AI agent
        st.session_state.df = df
        
        # Display data summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Clones", len(df))
        with col2:
            st.metric("Valid Results", len(df["Results"].dropna()))
        with col3:
            st.metric("Criteria Columns", len(criteria_columns))
        with col4:
            st.metric("Data Completeness", f"{df['Results'].notna().mean():.1%}")
        
        # Show data preview
        with st.expander("📊 Data Preview", expanded=False):
            st.dataframe(df.head(10), use_container_width=True)
            st.write(f"**Sheet:** {selected_sheet}")
        
        if criteria_columns:
            st.markdown("## 📈 Criteria Distributions")
            plot_criteria_distributions(df, criteria_columns)
        
        if "Results" not in df.columns:
            st.error("❌ No 'Results' column found in the selected sheet. Please check your data format.")
            return
        
        results = df["Results"].dropna().values
        
        # Configure simulation parameters
        st.sidebar.markdown("## ⚙️ Simulation Parameters")
        settings = configure_sidebar(df, results, criteria_columns)
        
        # Main analysis section
        st.markdown("## 🔬 Clone Selection Analysis")
        
        # Create tabs for different analyses
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🎯 Main Simulation", 
            "📊 Sensitivity Analysis", 
            "🔄 Workflow Comparison", 
            "📈 Advanced Plots", 
            "🤖 AI Assistant",
            "📋 Results Summary"
        ])
        
        with tab1:
            st.markdown("### Run Monte Carlo Simulation")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("🚀 Run Simulation", type="primary", use_container_width=True):
                    with st.spinner("Running simulation..."):
                        correlations = settings["correlations"]
                        probabilities = []
                        success_data_by_corr = {}
                        last_fitted_model = None
                        
                        # Progress bar
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for i, rho in enumerate(correlations):
                            status_text.text(f"Processing correlation {rho:.2f}...")
                            
                            prob, last_fitted_model, success_counts = simulate_workflow(
                                results, df, settings["top_x_percent"], settings["step1_keep"],
                                settings["step2_keep"], settings["step3_keep"], rho,
                                settings["n_rep"], settings["dist_method"],
                                settings["criteria_settings"], settings["apply_criteria_at_step2"],
                                settings["workflow_steps"]
                            )
                            probabilities.append(prob)
                            success_data_by_corr[rho] = success_counts
                            
                            progress_bar.progress((i + 1) / len(correlations))
                        
                        status_text.text("Simulation complete!")
                        
                        # Store results in session state
                        st.session_state.update({
                            "top_x_percent": settings["top_x_percent"],
                            "success_data_by_corr": success_data_by_corr,
                            "probabilities": probabilities,
                            "correlations": [float(c) for c in correlations],
                            "last_fitted_model": last_fitted_model,
                            "results": results,
                            "step2_keep": settings["step3_keep"],
                            "settings": settings
                        })
                        
                        st.success("✅ Simulation completed successfully!")
            
            with col2:
                st.markdown("""
                **Simulation Parameters:**
                - **Workflow Steps:** {workflow_steps}
                - **Top X%:** {top_x_percent}%
                - **Step 1 Keep:** {step1_keep} clones
                - **Step 2 Keep:** {step2_keep} clones
                - **Final Clones:** {step3_keep} clones
                - **Monte Carlo Repetitions:** {n_rep:,}
                - **Distribution Method:** {dist_method}
                """.format(**settings))
            
            # Display results if available
            if "probabilities" in st.session_state:
                st.markdown("### 📊 Simulation Results")
                
                # Key metrics
                max_prob = max(st.session_state["probabilities"])
                max_corr = st.session_state["correlations"][np.argmax(st.session_state["probabilities"])]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Max Success Probability", f"{max_prob:.3f}")
                with col2:
                    st.metric("Optimal Correlation", f"{max_corr:.2f}")
                with col3:
                    st.metric("Correlation Range", f"{min(st.session_state['correlations']):.2f} - {max(st.session_state['correlations']):.2f}")
                
                # Plots
                plot_success_prob_vs_corr(st.session_state["correlations"], st.session_state["probabilities"])
                
                if "last_fitted_model" in st.session_state:
                    plot_distribution_comparison(
                        st.session_state["results"],
                        st.session_state["last_fitted_model"],
                        settings["dist_method"]
                    )
                
                if "success_data_by_corr" in st.session_state:
                    plot_success_histogram(st.session_state)
        
        with tab2:
            st.markdown("### 📊 Sensitivity Analysis")
            st.markdown("Analyze how changes in key parameters affect success probability.")
            
            if st.button("🔍 Run Sensitivity Analysis", type="primary"):
                with st.spinner("Running sensitivity analysis..."):
                    sensitivity_results = run_sensitivity_analysis(
                        results, df, settings, st.session_state.get("correlations", [0.5])
                    )
                    st.session_state["sensitivity_results"] = sensitivity_results
                    plot_sensitivity_analysis(sensitivity_results)
        
        with tab3:
            st.markdown("### 🔄 Workflow Comparison")
            st.markdown("Compare different workflow configurations.")
            
            if st.button("⚖️ Compare Workflows", type="primary"):
                with st.spinner("Comparing workflows..."):
                    # Compare 2-step vs 3-step workflows
                    workflow_comparison = {}
                    
                    # 2-step workflow
                    settings_2step = settings.copy()
                    settings_2step["workflow_steps"] = 2
                    settings_2step["step3_keep"] = settings_2step["step2_keep"]
                    
                    prob_2step, _, _ = simulate_workflow(
                        results, df, settings["top_x_percent"], settings["step1_keep"],
                        settings["step2_keep"], settings["step2_keep"], 0.5,
                        settings["n_rep"], settings["dist_method"],
                        settings["criteria_settings"], settings["apply_criteria_at_step2"], 2
                    )
                    
                    # 3-step workflow
                    prob_3step, _, _ = simulate_workflow(
                        results, df, settings["top_x_percent"], settings["step1_keep"],
                        settings["step2_keep"], settings["step3_keep"], 0.5,
                        settings["n_rep"], settings["dist_method"],
                        settings["criteria_settings"], settings["apply_criteria_at_step2"], 3
                    )
                    
                    workflow_comparison = {
                        "2-step": prob_2step,
                        "3-step": prob_3step
                    }
                    
                    st.session_state["workflow_comparison"] = workflow_comparison
                    plot_workflow_comparison(workflow_comparison)
        
        with tab4:
            st.markdown("### 📈 Advanced Visualizations")
            
            if "probabilities" in st.session_state:
                plot_correlation_heatmap(st.session_state)
                plot_clone_selection_flow(st.session_state, settings)
        
        with tab5:
            # AI Agent Interface
            create_ai_agent_interface()
        
        with tab6:
            st.markdown("### 📋 Results Summary")
            
            if "probabilities" in st.session_state:
                # Summary statistics
                st.markdown("#### Key Findings")
                
                max_prob = max(st.session_state["probabilities"])
                min_prob = min(st.session_state["probabilities"])
                avg_prob = np.mean(st.session_state["probabilities"])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Maximum Success Rate", f"{max_prob:.1%}")
                with col2:
                    st.metric("Minimum Success Rate", f"{min_prob:.1%}")
                with col3:
                    st.metric("Average Success Rate", f"{avg_prob:.1%}")
                
                # Recommendations
                st.markdown("#### 💡 Recommendations")
                
                optimal_corr = st.session_state["correlations"][np.argmax(st.session_state["probabilities"])]
                
                recommendations = []
                if max_prob > 0.8:
                    recommendations.append("✅ **Excellent performance** - Current parameters achieve high success rates")
                elif max_prob > 0.6:
                    recommendations.append("⚠️ **Good performance** - Consider parameter optimization for better results")
                else:
                    recommendations.append("❌ **Low performance** - Significant parameter adjustments recommended")
                
                if optimal_corr > 0.7:
                    recommendations.append("✅ **High correlation beneficial** - Strong assay correlation improves selection")
                else:
                    recommendations.append("ℹ️ **Moderate correlation sufficient** - Lower correlation still achieves good results")
                
                for rec in recommendations:
                    st.markdown(rec)
                
                # Export results
                st.markdown("#### 📤 Export Results")
                if st.button("💾 Export Results to CSV"):
                    results_df = pd.DataFrame({
                        "Correlation": st.session_state["correlations"],
                        "Success_Probability": st.session_state["probabilities"]
                    })
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name="clone_selection_results.csv",
                        mime="text/csv"
                    )
    
    except Exception as e:
        st.error(f"❌ Error processing data: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()
