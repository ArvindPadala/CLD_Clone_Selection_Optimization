import streamlit as st
from loader import load_data
from sidebar import configure_sidebar
from plots import plot_criteria_distributions, plot_distribution_comparison, plot_success_prob_vs_corr, plot_success_histogram
from simulation import simulate_workflow, generate_samples, fit_lognormal

st.set_page_config(page_title="CLD Clone Selection Simulation", layout="wide")
st.markdown("<style>.block-container {padding-top: 1rem;}</style>", unsafe_allow_html=True)
st.title("CLD Clone Selection Simulation")

uploaded_file = st.sidebar.file_uploader("Upload Excel File with Assay Results", type=["xlsx"])

if uploaded_file:
    df, selected_sheet, criteria_columns = load_data(uploaded_file)

    if criteria_columns:
        plot_criteria_distributions(df, criteria_columns)

    if "Results" in df.columns:
        results = df["Results"].dropna().values
        settings = configure_sidebar(df, results, criteria_columns)

        if st.sidebar.button("Run Simulation and Plot"):
            correlations = settings["correlations"]
            probabilities = []
            success_data_by_corr = {}
            last_fitted_model = None

            for rho in correlations:
                prob, last_fitted_model, success_counts = simulate_workflow(
                    results, df, settings["top_x_percent"], settings["step1_keep"],
                    settings["step2_keep"], settings["step3_keep"], rho,
                    settings["n_rep"], settings["dist_method"],
                    settings["criteria_settings"], settings["apply_criteria_at_step2"],
                    settings["workflow_steps"]
                )
                probabilities.append(prob)
                success_data_by_corr[rho] = success_counts

            st.session_state.update({
                "top_x_percent": settings["top_x_percent"],
                "success_data_by_corr": success_data_by_corr,
                "probabilities": probabilities,
                "correlations": [float(c) for c in correlations],
                "last_fitted_model": last_fitted_model,
                "results": results,
                "step2_keep": settings["step3_keep"]
            })

        if "last_fitted_model" in st.session_state:
            plot_distribution_comparison(st.session_state["results"],
                                         st.session_state["last_fitted_model"],
                                         settings["dist_method"])

        if "probabilities" in st.session_state:
            plot_success_prob_vs_corr(st.session_state["correlations"],
                                      st.session_state["probabilities"])

        if "success_data_by_corr" in st.session_state:
            plot_success_histogram(st.session_state)
    else:
        st.warning("No 'Results' column found in selected sheet.")
