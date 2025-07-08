import numpy as np
from scipy.stats import lognorm, gaussian_kde

def fit_lognormal(data):
    data = np.array(data).flatten()
    data = data[data > 0]
    return lognorm.fit(data, floc=0)

def generate_samples(data, size, method="lognormal", fitted_model=None):
    data = np.array(data).flatten()
    data = data[data > 0]
    if method == "lognormal":
        shape, loc, scale = fitted_model or fit_lognormal(data)
        return lognorm.rvs(shape, loc=loc, scale=scale, size=size)
    elif method == "kde":
        kde = gaussian_kde(data)
        return kde.resample(size).flatten()
    else:
        raise ValueError("Unsupported distribution method")

def simulate_workflow(real_data, df, top_x_percent, step1_keep, step2_keep, step3_keep,
                      correlation, n_rep, method, criteria_settings, apply_criteria, workflow_steps):
    real_data = np.array(real_data).flatten()
    fitted_model = fit_lognormal(real_data) if method == "lognormal" else None
    success_count = 0
    success_counts = []

    for _ in range(n_rep):
        assay_f = generate_samples(real_data, len(real_data), method, fitted_model)
        filter_mask = np.ones(len(df), dtype=bool)
        for crit_col, op, thresh in criteria_settings:
            col_vals = df[crit_col].values
            if op == ">=": filter_mask &= col_vals >= thresh
            elif op == "<=": filter_mask &= col_vals <= thresh
            else: filter_mask &= col_vals == thresh
        if not apply_criteria:
            assay_f = assay_f[filter_mask]
        if len(assay_f) < step1_keep:
            continue

        top1_idx = np.argsort(assay_f)[-step1_keep:]
        top1_f = assay_f[top1_idx]
        noise1 = generate_samples(real_data, step1_keep, method, fitted_model)
        assay_g = correlation * top1_f + np.sqrt(1 - correlation**2) * noise1

        if len(assay_g) < step2_keep:
            continue
        top2_idx = np.argsort(assay_g)[-step2_keep:]
        top2_f = top1_f[top2_idx]

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

        if apply_criteria:
            if workflow_steps == 3:
                mask = filter_mask[top1_idx][top2_idx][final_idx]
            else:
                mask = filter_mask[top1_idx][final_idx]
            if not all(mask):
                continue

        cutoff = np.percentile(assay_f, 100 - top_x_percent)
        count_success = np.sum(final_scores >= cutoff)
        if count_success == step3_keep:
            success_count += 1
        success_counts.append(count_success)

    return success_count / n_rep, fitted_model, success_counts
