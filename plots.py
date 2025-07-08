import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from simulation import generate_samples, fit_lognormal

def plot_criteria_distributions(df, criteria_columns):
    num = len(criteria_columns)
    cols = 3
    rows = -(-num // cols)
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
    axes = np.array(axes).flatten()
    for i, col in enumerate(criteria_columns):
        axes[i].hist(df[col].dropna(), bins=30, color='green', alpha=0.7)
        axes[i].set_title(f"Distribution of {col}")
        axes[i].set_xlabel(col)
        axes[i].set_ylabel("Frequency")
    for j in range(num, len(axes)):
        fig.delaxes(axes[j])
    fig.tight_layout()
    st.pyplot(fig)

def plot_distribution_comparison(real, synthetic_model, method):
    synthetic = generate_samples(real, size=10000, method=method, fitted_model=synthetic_model)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(real, bins=50, alpha=0.6, density=True, label="Real", color="blue")
    ax.hist(synthetic, bins=50, alpha=0.5, density=True, label=f"Synthetic ({method})", color="orange")
    ax.set_title("Distribution Comparison: Real vs Synthetic")
    ax.set_xlabel("Assay Result Value")
    ax.set_ylabel("Density")
    ax.legend()
    st.pyplot(fig)

def plot_success_prob_vs_corr(correlations, probabilities):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(correlations, probabilities, marker='o')
    ax.set_title("Success Probability vs Assay Correlation")
    ax.set_xlabel("Correlation Between Assay F and G")
    ax.set_ylabel("Probability (Final Clones in Top X%)")
    ax.grid(True)
    st.success(f"Highest Success Probability: {max(probabilities):.3f} at Correlation = {correlations[np.argmax(probabilities)]}")
    st.pyplot(fig)

def plot_success_histogram(state):
    correlations = state["correlations"]
    probabilities = state["probabilities"]
    best_idx = int(np.argmax(probabilities))
    best_corr = correlations[best_idx]
    selected_corr = st.selectbox("Select correlation for clone success histogram:", correlations, index=best_idx)
    counts = state["success_data_by_corr"][selected_corr]
    step2_keep = state["step2_keep"]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(counts, bins=np.arange(0, step2_keep + 2) - 0.5, rwidth=0.8, color='skyblue', edgecolor='black')
    ax.set_title(f"Clone Success Histogram (Correlation = {selected_corr})")
    ax.set_xlabel("Number of Final Clones in Top X%")
    ax.set_ylabel("Frequency")
    ax.set_xticks(range(0, step2_keep + 1))
    st.pyplot(fig)
