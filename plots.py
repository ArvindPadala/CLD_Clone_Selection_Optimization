import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from simulation import generate_samples, fit_lognormal, simulate_workflow
import pandas as pd


def plot_criteria_distributions(df, criteria_columns):
    """Plot distributions of criteria columns using plotly."""
    num_cols = len(criteria_columns)
    if num_cols == 0:
        return
    
    # Create subplots
    cols = min(3, num_cols)
    rows = (num_cols + cols - 1) // cols
    
    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=criteria_columns,
        specs=[[{"secondary_y": False}] * cols] * rows
    )
    
    for i, col in enumerate(criteria_columns):
        row = i // cols + 1
        col_idx = i % cols + 1
        
        # Get data for this column
        data = df[col].dropna()
        
        # Create histogram
        fig.add_trace(
            go.Histogram(
                x=data,
                nbinsx=30,
                name=col,
                showlegend=False,
                marker_color='lightblue',
                opacity=0.7
            ),
            row=row, col=col_idx
        )
        
        # Add mean line
        mean_val = data.mean()
        fig.add_vline(
            x=mean_val, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"Mean: {mean_val:.3f}",
            row=row, col=col_idx
        )
    
    fig.update_layout(
        title="Criteria Distributions",
        height=200 * rows,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_distribution_comparison(real, synthetic_model, method):
    """Plot comparison between real and synthetic data distributions."""
    synthetic = generate_samples(real, size=10000, method=method, fitted_model=synthetic_model)
    
    fig = go.Figure()
    
    # Real data histogram
    fig.add_trace(go.Histogram(
        x=real,
        nbinsx=50,
        name="Real Data",
        opacity=0.7,
        marker_color='blue'
    ))
    
    # Synthetic data histogram
    fig.add_trace(go.Histogram(
        x=synthetic,
        nbinsx=50,
        name=f"Synthetic ({method})",
        opacity=0.7,
        marker_color='orange'
    ))
    
    fig.update_layout(
        title="Distribution Comparison: Real vs Synthetic Data",
        xaxis_title="Assay Result Value",
        yaxis_title="Frequency",
        barmode='overlay',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_success_prob_vs_corr(correlations, probabilities):
    """Plot success probability vs correlation with enhanced styling."""
    fig = go.Figure()
    
    # Main line plot
    fig.add_trace(go.Scatter(
        x=correlations,
        y=probabilities,
        mode='lines+markers',
        name='Success Probability',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8, color='#1f77b4')
    ))
    
    # Highlight maximum point
    max_idx = np.argmax(probabilities)
    fig.add_trace(go.Scatter(
        x=[correlations[max_idx]],
        y=[probabilities[max_idx]],
        mode='markers',
        name='Optimal Point',
        marker=dict(size=15, color='red', symbol='star'),
        showlegend=True
    ))
    
    fig.update_layout(
        title="Success Probability vs Assay Correlation",
        xaxis_title="Correlation Between Assay Steps",
        yaxis_title="Probability (Final Clones in Top X%)",
        height=500,
        hovermode='x unified'
    )
    
    # Add grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display key metrics
    max_prob = max(probabilities)
    max_corr = correlations[np.argmax(probabilities)]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Maximum Success Rate", f"{max_prob:.1%}")
    with col2:
        st.metric("Optimal Correlation", f"{max_corr:.2f}")
    with col3:
        st.metric("Improvement Range", f"{max_prob - min(probabilities):.1%}")

def plot_success_histogram(state):
    """Plot histogram of successful clones with interactive selection."""
    correlations = state["correlations"]
    probabilities = state["probabilities"]
    best_idx = int(np.argmax(probabilities))
    best_corr = correlations[best_idx]
    
    # Create selection widget
    selected_corr = st.selectbox(
        "Select correlation for clone success histogram:",
        correlations, 
        index=best_idx,
        format_func=lambda x: f"{x:.2f} (Success: {probabilities[correlations.index(x)]:.1%})"
    )
    
    counts = state["success_data_by_corr"][selected_corr]
    step2_keep = state["step2_keep"]
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=counts,
        nbinsx=step2_keep + 1,
        name='Success Counts',
        marker_color='lightblue',
        opacity=0.8
    ))
    
    # Add mean line
    mean_count = np.mean(counts)
    fig.add_vline(
        x=mean_count,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mean: {mean_count:.1f}"
    )
    
    fig.update_layout(
        title=f"Clone Success Distribution (Correlation = {selected_corr:.2f})",
        xaxis_title="Number of Final Clones in Top X%",
        yaxis_title="Frequency",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_workflow_comparison(workflow_comparison):
    """Plot comparison between different workflow configurations."""
    workflows = list(workflow_comparison.keys())
    probabilities = list(workflow_comparison.values())
    
    fig = go.Figure(data=[
        go.Bar(
            x=workflows,
            y=probabilities,
            marker_color=['#1f77b4', '#ff7f0e'],
            text=[f'{p:.1%}' for p in probabilities],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Workflow Comparison: Success Probability",
        xaxis_title="Workflow Type",
        yaxis_title="Success Probability",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display comparison metrics
    if len(probabilities) == 2:
        diff = probabilities[1] - probabilities[0]
        st.metric(
            "Difference (3-step - 2-step)", 
            f"{diff:+.1%}",
            delta_color="normal" if diff >= 0 else "inverse"
        )

def plot_sensitivity_analysis(sensitivity_results):
    """Plot sensitivity analysis results."""
    if not sensitivity_results:
        st.warning("No sensitivity analysis results available.")
        return
    
    # Create subplots for each parameter
    param_names = list(sensitivity_results.keys())
    fig = make_subplots(
        rows=1, cols=len(param_names),
        subplot_titles=[f"{param.replace('_', ' ').title()}" for param in param_names],
        specs=[[{"secondary_y": False}] * len(param_names)]
    )
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, (param_name, data) in enumerate(sensitivity_results.items()):
        values = data['values']
        probabilities = data['probabilities']
        
        fig.add_trace(
            go.Scatter(
                x=values,
                y=probabilities,
                mode='lines+markers',
                name=param_name.replace('_', ' ').title(),
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=8),
                showlegend=False
            ),
            row=1, col=i+1
        )
        
        # Add baseline reference
        if len(probabilities) > 2:
            baseline = probabilities[len(probabilities)//2]  # Middle value
            fig.add_hline(
                y=baseline,
                line_dash="dash",
                line_color="gray",
                row=1, col=i+1
            )
    
    fig.update_layout(
        title="Sensitivity Analysis: Parameter Effects on Success Probability",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary table
    st.markdown("### Sensitivity Analysis Summary")
    summary_data = []
    for param_name, data in sensitivity_results.items():
        values = data['values']
        probabilities = data['probabilities']
        
        # Calculate sensitivity metrics
        max_prob = max(probabilities)
        min_prob = min(probabilities)
        range_prob = max_prob - min_prob
        baseline = probabilities[len(probabilities)//2]
        
        summary_data.append({
            'Parameter': param_name.replace('_', ' ').title(),
            'Range': f"{min(values)} - {max(values)}",
            'Max Success': f"{max_prob:.1%}",
            'Min Success': f"{min_prob:.1%}",
            'Sensitivity': f"{range_prob:.1%}",
            'Baseline': f"{baseline:.1%}"
        })
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True)

def plot_correlation_heatmap(state):
    """Plot correlation heatmap showing actual parameter interactions."""
    if "probabilities" not in state:
        return

    correlations = state["correlations"]
    settings = state.get("settings", {})
    results = state.get("results", np.array([]))

    if len(results) == 0 or not settings:
        st.info("Run a simulation first to see the parameter interaction heatmap.")
        return

    base_step1 = settings.get("step1_keep", 96)
    step1_range = sorted(set([
        max(settings.get("step2_keep", 6) + 1, int(base_step1 * 0.7)),
        base_step1,
        min(len(results), int(base_step1 * 1.3))
    ]))

    # Sample a subset of correlations to keep computation fast
    corr_subset = correlations[::max(1, len(correlations) // 8)]
    if len(corr_subset) == 0:
        corr_subset = correlations[:1]

    heatmap_data = np.zeros((len(step1_range), len(corr_subset)))

    with st.spinner("Computing parameter interaction heatmap..."):
        for i, s1 in enumerate(step1_range):
            s2 = min(settings.get("step2_keep", 48), s1)
            s3 = min(settings.get("step3_keep", 6), s2)
            for j, rho in enumerate(corr_subset):
                try:
                    prob, _, _, _ = simulate_workflow(
                        results, state.get("df", pd.DataFrame()),
                        settings["top_x_percent"], s1, s2, s3,
                        float(rho), min(500, settings.get("n_rep", 500)),
                        settings["dist_method"],
                        settings.get("criteria_settings", []),
                        settings.get("apply_criteria_at_step2", False),
                        settings.get("workflow_steps", 2)
                    )
                    heatmap_data[i][j] = prob
                except Exception:
                    heatmap_data[i][j] = 0.0

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=[f"{c:.2f}" for c in corr_subset],
        y=[str(s) for s in step1_range],
        colorscale='Viridis',
        text=np.round(heatmap_data, 3),
        texttemplate="%{text}",
        textfont={"size": 10},
        colorbar=dict(title="Success Probability")
    ))

    fig.update_layout(
        title="Parameter Interaction Heatmap (Step 1 Keep × Correlation)",
        xaxis_title="Correlation",
        yaxis_title="Step 1 Keep",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_clone_selection_flow(state, settings):
    """Plot the clone selection flow diagram."""
    if "probabilities" not in state:
        return
    
    # Create a Sankey-like flow diagram
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = [
                f"Initial Clones\n({len(state['results']):,})",
                f"Step 1 Selection\n({settings['step1_keep']})",
                f"Step 2 Selection\n({settings['step2_keep']})",
                f"Final Selection\n({settings['step3_keep']})"
            ],
            color = "blue"
        ),
        link = dict(
            source = [0, 1, 2],  # indices correspond to labels
            target = [1, 2, 3],
            value = [
                settings['step1_keep'],
                settings['step2_keep'],
                settings['step3_keep']
            ]
        )
    )])
    
    fig.update_layout(
        title_text="Clone Selection Flow",
        font_size=10,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_efficiency_metrics(settings):
    """Plot workflow efficiency metrics."""
    from simulation import calculate_workflow_efficiency
    
    efficiency = calculate_workflow_efficiency(
        settings['step1_keep'],
        settings['step2_keep'],
        settings['step3_keep'],
        settings['workflow_steps']
    )
    
    # Create radar chart for efficiency metrics
    categories = ['Reduction Ratio', 'Step 1 Efficiency', 'Step 2 Efficiency', 'Overall Efficiency']
    values = [
        efficiency['reduction_ratio'] / 100,  # Normalize
        efficiency['step1_efficiency'],
        efficiency['step2_efficiency'],
        efficiency['overall_efficiency']
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Efficiency Metrics',
        line_color='#1f77b4'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=False,
        title="Workflow Efficiency Metrics",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display efficiency table
    st.markdown("### Efficiency Metrics")
    eff_data = {
        'Metric': ['Reduction Ratio', 'Step 1 Efficiency', 'Step 2 Efficiency', 'Overall Efficiency'],
        'Value': [
            f"{efficiency['reduction_ratio']:.1f}x",
            f"{efficiency['step1_efficiency']:.1%}",
            f"{efficiency['step2_efficiency']:.1%}",
            f"{efficiency['overall_efficiency']:.1%}"
        ]
    }
    eff_df = pd.DataFrame(eff_data)
    st.dataframe(eff_df, use_container_width=True)
