import numpy as np
from scipy.stats import lognorm, gaussian_kde
import pandas as pd

def fit_lognormal(data):
    """Fit lognormal distribution to data."""
    data = np.array(data).flatten()
    data = data[data > 0]
    if len(data) == 0:
        raise ValueError("No positive data points for lognormal fitting")
    return lognorm.fit(data, floc=0)

def generate_samples(data, size, method="lognormal", fitted_model=None):
    """Generate synthetic samples using specified distribution method."""
    data = np.array(data).flatten()
    data = data[data > 0]
    
    if len(data) == 0:
        raise ValueError("No valid data points for sample generation")
    
    if method == "lognormal":
        shape, loc, scale = fitted_model or fit_lognormal(data)
        return lognorm.rvs(shape, loc=loc, scale=scale, size=size)
    elif method == "kde":
        kde = gaussian_kde(data)
        return kde.resample(size).flatten()
    else:
        raise ValueError("Unsupported distribution method")

def apply_criteria_filter(df, criteria_settings, indices):
    """Apply criteria filtering to selected indices."""
    if not criteria_settings:
        return np.ones(len(indices), dtype=bool)
    
    filter_mask = np.ones(len(indices), dtype=bool)
    for crit_col, op, thresh in criteria_settings:
        if crit_col not in df.columns:
            continue
        
        col_vals = df[crit_col].values[indices]
        if op == ">=":
            filter_mask &= col_vals >= thresh
        elif op == "<=":
            filter_mask &= col_vals <= thresh
        elif op == "=":
            filter_mask &= np.abs(col_vals - thresh) < 1e-10
        else:
            raise ValueError(f"Unsupported operator: {op}")
    
    return filter_mask

def simulate_workflow(real_data, df, top_x_percent, step1_keep, step2_keep, step3_keep,
                      correlation, n_rep, method, criteria_settings, apply_criteria, workflow_steps):
    """
    Simulate clone selection workflow with Monte Carlo approach.
    
    Returns:
        success_probability, fitted_model, success_counts
    """
    real_data = np.array(real_data).flatten()
    
    # Validate inputs
    if len(real_data) == 0:
        raise ValueError("No valid data provided")
    
    if step1_keep > len(real_data):
        raise ValueError(f"Step 1 keep ({step1_keep}) cannot exceed data size ({len(real_data)})")
    
    if step2_keep > step1_keep:
        raise ValueError(f"Step 2 keep ({step2_keep}) cannot exceed step 1 keep ({step1_keep})")
    
    if workflow_steps == 3 and step3_keep > step2_keep:
        raise ValueError(f"Step 3 keep ({step3_keep}) cannot exceed step 2 keep ({step2_keep})")
    
    # Fit distribution model
    fitted_model = fit_lognormal(real_data) if method == "lognormal" else None
    
    success_count = 0
    success_counts = []
    
    # Calculate cutoff for top X%
    cutoff = np.percentile(real_data, 100 - top_x_percent)
    
    for rep in range(n_rep):
        try:
            # Step 1: Generate assay F results
            assay_f = generate_samples(real_data, len(real_data), method, fitted_model)
            
            # Apply initial filtering if criteria are applied at step 1
            if not apply_criteria:
                filter_mask = apply_criteria_filter(df, criteria_settings, np.arange(len(df)))
                assay_f = assay_f[filter_mask]
                if len(assay_f) < step1_keep:
                    continue
            
            # Select top clones from step 1
            top1_idx = np.argsort(assay_f)[-step1_keep:]
            top1_f = assay_f[top1_idx]
            
            # Step 2: Generate assay G results with correlation
            noise1 = generate_samples(real_data, step1_keep, method, fitted_model)
            assay_g = correlation * top1_f + np.sqrt(1 - correlation**2) * noise1
            
            if len(assay_g) < step2_keep:
                continue
            
            # Select top clones from step 2
            top2_idx = np.argsort(assay_g)[-step2_keep:]
            top2_f = top1_f[top2_idx]
            
            # Step 3 (if 3-step workflow)
            if workflow_steps == 3:
                noise2 = generate_samples(real_data, step2_keep, method, fitted_model)
                assay_h = correlation * top2_f + np.sqrt(1 - correlation**2) * noise2
                
                if len(assay_h) < step3_keep:
                    continue
                
                final_idx = np.argsort(assay_h)[-step3_keep:]
                final_scores = top2_f[final_idx]
            else:
                final_idx = np.argsort(assay_g)[-step3_keep:]
                final_scores = top1_f[final_idx]
            
            # Apply criteria filtering at final step if requested
            if apply_criteria:
                if workflow_steps == 3:
                    # Map back to original indices
                    original_indices = top1_idx[top2_idx[final_idx]]
                    mask = apply_criteria_filter(df, criteria_settings, original_indices)
                else:
                    original_indices = top1_idx[final_idx]
                    mask = apply_criteria_filter(df, criteria_settings, original_indices)
                
                if not all(mask):
                    continue
            
            # Count successful clones
            count_success = np.sum(final_scores >= cutoff)
            success_counts.append(count_success)
            
            # Check if all final clones are successful
            if count_success == step3_keep:
                success_count += 1
                
        except Exception as e:
            # Skip this iteration if there's an error
            continue
    
    success_probability = success_count / n_rep if n_rep > 0 else 0
    return success_probability, fitted_model, success_counts

def run_sensitivity_analysis(results, df, settings, correlations):
    """
    Run sensitivity analysis to understand parameter effects.
    
    Returns:
        Dictionary with sensitivity analysis results
    """
    base_settings = settings.copy()
    sensitivity_results = {}
    
    # Parameter ranges for sensitivity analysis
    param_ranges = {
        'step1_keep': [int(base_settings['step1_keep'] * 0.5), 
                      int(base_settings['step1_keep'] * 0.75),
                      base_settings['step1_keep'],
                      int(base_settings['step1_keep'] * 1.25),
                      int(base_settings['step1_keep'] * 1.5)],
        'step2_keep': [int(base_settings['step2_keep'] * 0.5),
                      int(base_settings['step2_keep'] * 0.75),
                      base_settings['step2_keep'],
                      int(base_settings['step2_keep'] * 1.25),
                      int(base_settings['step2_keep'] * 1.5)],
        'top_x_percent': [1, 2, 5, 10, 15]
    }
    
    # Use a single correlation value for sensitivity analysis
    correlation = correlations[0] if len(correlations) > 0 else 0.5
    
    for param_name, param_values in param_ranges.items():
        probabilities = []
        
        for param_value in param_values:
            # Create modified settings
            test_settings = base_settings.copy()
            test_settings[param_name] = param_value
            
            # Ensure logical constraints
            if param_name == 'step1_keep':
                test_settings['step2_keep'] = min(test_settings['step2_keep'], param_value)
                test_settings['step3_keep'] = min(test_settings['step3_keep'], test_settings['step2_keep'])
            elif param_name == 'step2_keep':
                test_settings['step3_keep'] = min(test_settings['step3_keep'], param_value)
            
            try:
                prob, _, _ = simulate_workflow(
                    results, df, test_settings['top_x_percent'],
                    test_settings['step1_keep'], test_settings['step2_keep'],
                    test_settings['step3_keep'], correlation, 1000,  # Reduced n_rep for speed
                    test_settings['dist_method'], test_settings['criteria_settings'],
                    test_settings['apply_criteria_at_step2'], test_settings['workflow_steps']
                )
                probabilities.append(prob)
            except Exception as e:
                probabilities.append(0)  # Default to 0 if simulation fails
        
        sensitivity_results[param_name] = {
            'values': param_values,
            'probabilities': probabilities
        }
    
    return sensitivity_results

def calculate_workflow_efficiency(step1_keep, step2_keep, step3_keep, workflow_steps):
    """Calculate workflow efficiency metrics."""
    total_screened = step1_keep
    final_selected = step3_keep if workflow_steps == 3 else step2_keep
    
    efficiency_metrics = {
        'reduction_ratio': total_screened / final_selected,
        'step1_efficiency': step2_keep / step1_keep,
        'step2_efficiency': step3_keep / step2_keep if workflow_steps == 3 else 1.0,
        'overall_efficiency': final_selected / total_screened
    }
    
    return efficiency_metrics

def validate_workflow_parameters(step1_keep, step2_keep, step3_keep, workflow_steps, total_clones):
    """Validate workflow parameters for logical consistency."""
    errors = []
    
    if step1_keep > total_clones:
        errors.append(f"Step 1 keep ({step1_keep}) exceeds total clones ({total_clones})")
    
    if step2_keep > step1_keep:
        errors.append(f"Step 2 keep ({step2_keep}) exceeds step 1 keep ({step1_keep})")
    
    if workflow_steps == 3 and step3_keep > step2_keep:
        errors.append(f"Step 3 keep ({step3_keep}) exceeds step 2 keep ({step2_keep})")
    
    if step1_keep <= 0 or step2_keep <= 0 or step3_keep <= 0:
        errors.append("All keep values must be positive")
    
    return errors
