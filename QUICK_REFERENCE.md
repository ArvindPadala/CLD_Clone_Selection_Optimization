# 🧬 CLD Dashboard - Quick Reference Card

## 🚀 Quick Start

### Run Dashboard
```bash
streamlit run app.py
```
**Access**: http://localhost:8501 (or 8502 if busy)

### Data Format
- **Required**: `Results` column (numeric values)
- **Optional**: `Criteria1`, `Criteria2`, etc. (for filtering)

---

## ⚙️ Key Parameters

### Workflow Steps
- **2-step**: Initial → Final selection
- **3-step**: Initial → Secondary → Final selection

### Distribution Methods
- **Lognormal**: For skewed biological data
- **KDE**: For any distribution shape

### Success Thresholds
- **1-2%**: Very selective
- **5-10%**: Moderate
- **15-20%**: Less selective

### Recommended Clone Numbers
| Dataset Size | Step 1 | Step 2 | Final |
|-------------|--------|--------|-------|
| <500        | 24-48  | 12-24  | 6-12  |
| 500-1000    | 48-96  | 24-48  | 6-12  |
| >1000       | 96-192 | 48-96  | 6-24  |

---

## 📊 Interpreting Results

### Success Rate Guide
```
> 80%: Excellent - Current parameters optimal
60-80%: Good - Room for improvement
40-60%: Fair - Significant optimization needed
< 40%: Poor - Major parameter review required
```

### Correlation Analysis
```
> 0.7: High correlation beneficial
0.5-0.7: Moderate correlation sufficient
< 0.5: Correlation less important
```

### Sensitivity Levels
```
> 20%: High sensitivity - Focus optimization here
10-20%: Medium sensitivity - Fine-tune based on resources
< 10%: Low sensitivity - Can use default values
```

---

## 🔍 Model Validation Checklist

### Distribution Model
- [ ] Synthetic data matches real data
- [ ] Parameter estimates are reasonable
- [ ] Model captures data distribution shape

### Simulation
- [ ] Results stabilize with more repetitions
- [ ] Logical consistency across parameters
- [ ] Confidence intervals are reasonable

### Cross-Validation
- [ ] Results consistent across data splits
- [ ] Bootstrap confidence intervals calculated
- [ ] Model performance validated

---

## 🎯 Optimization Strategy

### High Performance (>80%)
- ✅ Current parameters optimal
- Consider reducing resources
- Focus on maintaining workflow

### Medium Performance (60-80%)
- ⚠️ Use sensitivity analysis
- Optimize high-sensitivity parameters
- Test different correlation ranges

### Low Performance (<60%)
- ❌ Review all parameters
- Check data quality
- Consider alternative workflows

---

## 🔧 Troubleshooting

### Common Issues
| Issue | Solution |
|-------|----------|
| "No Results column" | Check column name spelling |
| "Step 1 exceeds clones" | Reduce Step 1 keep value |
| "Simulation slow" | Reduce repetitions, increase step size |
| "Memory error" | Enable memory optimization |

### Performance Tips
- Start with 1,000 repetitions for testing
- Use 0.05 correlation step size for balance
- Enable memory optimization for large datasets
- Test with smaller datasets first

---

## 📈 Key Metrics to Monitor

### Primary Metrics
- **Success Probability**: Likelihood of selecting top clones
- **Optimal Correlation**: Best correlation for maximum success
- **Sensitivity Scores**: Parameter impact on results

### Efficiency Metrics
- **Reduction Ratio**: How much you're narrowing down
- **Step Efficiencies**: Percentage advancing to next step
- **Overall Efficiency**: Final selection rate

### Quality Indicators
- **Data Completeness**: Percentage of valid data
- **Outlier Count**: Number of potential outliers
- **Distribution Shape**: Skewness and normality

---

## 💡 Best Practices

### Data Preparation
- Clean data thoroughly before analysis
- Document data sources and processing
- Validate data quality using built-in tools

### Parameter Selection
- Start with recommended values
- Use sensitivity analysis to identify key parameters
- Test parameter ranges systematically

### Model Validation
- Always validate model assumptions
- Compare multiple approaches when possible
- Use cross-validation for robust results

### Result Interpretation
- Consider biological context
- Account for uncertainty in estimates
- Validate against domain knowledge

---

## 📞 Quick Commands

### Installation
```bash
pip install -r requirements.txt
```

### Test Installation
```bash
python -c "import streamlit, pandas, plotly; print('✅ Ready!')"
```

### Run with Options
```bash
# Specific port
streamlit run app.py --server.port 8502

# Headless mode
streamlit run app.py --server.headless true
```

---

## 🔄 Workflow Summary

1. **Upload Data** → Excel file with Results column
2. **Configure Parameters** → Set workflow and selection criteria
3. **Run Simulation** → Execute Monte Carlo analysis
4. **Review Results** → Check success probability and correlation
5. **Sensitivity Analysis** → Identify key parameters
6. **Optimize** → Adjust parameters based on analysis
7. **Validate** → Cross-validate results
8. **Export** → Download results and recommendations

---

*For detailed information, see the complete USER_GUIDE.md* 