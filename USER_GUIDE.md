# 🧬 CLD Clone Selection Dashboard - Complete User Guide

## 📋 Table of Contents
1. [Getting Started](#getting-started)
2. [Running the Dashboard](#running-the-dashboard)
3. [Data Preparation](#data-preparation)
4. [Model Configuration](#model-configuration)
5. [Interpreting Results](#interpreting-results)
6. [Evaluating Performance](#evaluating-performance)
7. [Model Validation](#model-validation)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Required packages (see requirements.txt)
- Excel file with assay data

### Installation
```bash
# Clone or download the project
cd "BMS Challenge Project 2(Team - BlackCloud)"

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import streamlit, pandas, numpy, plotly; print('✅ All packages installed successfully!')"
```

---

## 🖥️ Running the Dashboard

### Basic Launch
```bash
streamlit run app.py
```

### Advanced Launch Options
```bash
# Run on specific port
streamlit run app.py --server.port 8502

# Run in headless mode (for servers)
streamlit run app.py --server.headless true

# Run with specific config
streamlit run app.py --server.maxUploadSize 200
```

### Accessing the Dashboard
- **Local URL**: http://localhost:8501 (or 8502 if 8501 is busy)
- **Network URL**: http://192.168.1.154:8501 (for remote access)

---

## 📊 Data Preparation

### Required Data Format
Your Excel file must contain:
- **Required Column**: `Results` (numeric assay values)
- **Optional Columns**: `Criteria1`, `Criteria2`, etc. (for filtering)

### Example Data Structure
| Results | Criteria1 | Criteria2 |
|---------|-----------|-----------|
| 0.116   | 0         | 0.5       |
| 1.059   | 6         | 0.8       |
| 0.293   | 0         | 0.3       |

### Data Quality Checklist
- ✅ No missing values in Results column
- ✅ Numeric values only
- ✅ Reasonable range (typically 0-100 or similar)
- ✅ No extreme outliers (unless biologically relevant)
- ✅ Consistent units across all measurements

### Data Validation
The dashboard automatically:
- Detects and reports data quality issues
- Identifies outliers using IQR method
- Calculates distribution statistics
- Provides data quality recommendations

---

## ⚙️ Model Configuration

### 1. Workflow Configuration
**Number of Workflow Steps**: Choose between 2 or 3 steps
- **2-step**: Initial screening → Final selection
- **3-step**: Initial screening → Secondary screening → Final selection

### 2. Distribution Modeling
**Distribution Method**:
- **Lognormal**: Parametric approach, good for skewed biological data
- **KDE**: Non-parametric approach, flexible for any distribution

**Selection Guide**:
- Use **Lognormal** if data is right-skewed (most biological data)
- Use **KDE** if data has unusual distribution patterns
- Test both methods and compare results

### 3. Success Criteria
**Top X% Threshold**: Percentage of top-performing clones to consider successful
- **1-2%**: Very selective (high quality, low quantity)
- **5-10%**: Moderate selectivity
- **15-20%**: Less selective (lower quality, higher quantity)

### 4. Clone Selection Parameters

#### Step 1 (Initial Screening)
- **Range**: 10 to total available clones
- **Recommendation**: 48-192 clones for datasets >1000 clones
- **Impact**: High sensitivity parameter

#### Step 2 (Secondary Screening)
- **Range**: 1 to Step 1 keep value
- **Recommendation**: 24-96 clones
- **Impact**: Medium sensitivity parameter

#### Step 3 (Final Selection) - 3-step workflow only
- **Range**: 1 to Step 2 keep value
- **Recommendation**: 6-24 clones
- **Impact**: High sensitivity parameter

### 5. Correlation Analysis
**Correlation Range**: Relationship between assay steps (0.0 to 1.0)
- **0.0**: No correlation (independent assays)
- **0.5**: Moderate correlation
- **1.0**: Perfect correlation (same assay)

**Step Size**: Resolution of correlation analysis
- **0.01**: High precision (slow)
- **0.05**: Medium precision (balanced)
- **0.1**: Low precision (fast)

### 6. Simulation Parameters
**Monte Carlo Repetitions**: Number of simulation runs
- **1,000**: Quick testing
- **5,000**: Standard analysis
- **10,000**: High precision
- **50,000**: Maximum precision (slow)

### 7. Criteria Filtering
**Apply Criteria at Final Step**: Enable/disable quality filtering
- **Enabled**: Only clones meeting criteria advance
- **Disabled**: All clones advance regardless of criteria

**Criteria Configuration**:
- Select criteria columns to use
- Choose comparison operators (≥, ≤, =)
- Set threshold values

---

## 📈 Interpreting Results

### 1. Main Simulation Results

#### Success Probability vs Correlation Plot
**What it shows**: How success probability changes with assay correlation

**Key Metrics**:
- **Maximum Success Rate**: Best achievable success probability
- **Optimal Correlation**: Correlation value for maximum success
- **Improvement Range**: Difference between best and worst scenarios

**Interpretation Guide**:
```
Success Rate > 80%: Excellent performance
Success Rate 60-80%: Good performance  
Success Rate 40-60%: Fair performance
Success Rate < 40%: Poor performance
```

#### Clone Success Histogram
**What it shows**: Distribution of successful clones across simulations

**Key Insights**:
- **Peak at maximum**: Most simulations achieve full success
- **Wide distribution**: High variability in selection quality
- **Mean line**: Average number of successful clones

### 2. Sensitivity Analysis Results

#### Parameter Impact Assessment
**Sensitivity Levels**:
- **High (>20%)**: Parameter has major impact on success
- **Medium (10-20%)**: Parameter has moderate impact
- **Low (<10%)**: Parameter has minor impact

**Action Items**:
- **High sensitivity**: Focus optimization efforts here
- **Medium sensitivity**: Fine-tune based on resources
- **Low sensitivity**: Can use default values

#### Sensitivity Summary Table
Review the summary table for:
- Parameter ranges tested
- Maximum and minimum success rates
- Sensitivity scores
- Baseline performance

### 3. Workflow Comparison

#### 2-step vs 3-step Analysis
**Comparison Metrics**:
- Success probability for each workflow
- Difference in performance
- Resource efficiency

**Decision Framework**:
- **3-step better**: Use 3-step workflow
- **2-step better**: Use 2-step workflow
- **Similar performance**: Choose based on resource constraints

### 4. Advanced Visualizations

#### Correlation Heatmap
**What it shows**: Parameter interactions and their effects

**Interpretation**:
- **Red areas**: High success probability
- **Blue areas**: Low success probability
- **Patterns**: Identify optimal parameter combinations

#### Clone Selection Flow
**What it shows**: Visual representation of the selection process

**Key Information**:
- Number of clones at each step
- Reduction ratios
- Flow efficiency

---

## 🎯 Evaluating Performance

### 1. Performance Assessment Framework

#### Success Rate Evaluation
```
Excellent (>80%): Current parameters optimal
Good (60-80%): Room for improvement
Fair (40-60%): Significant optimization needed
Poor (<40%): Major parameter review required
```

#### Correlation Analysis
```
High Optimal (>0.7): Strong correlation beneficial
Medium Optimal (0.5-0.7): Moderate correlation sufficient
Low Optimal (<0.5): Correlation less important
```

#### Parameter Sensitivity
```
High Sensitivity (>20%): Critical parameter
Medium Sensitivity (10-20%): Important parameter
Low Sensitivity (<10%): Minor parameter
```

### 2. Efficiency Metrics

#### Workflow Efficiency
- **Reduction Ratio**: How much you're narrowing down
- **Step Efficiencies**: Percentage advancing to next step
- **Overall Efficiency**: Final selection rate

#### Resource Optimization
- **High correlation**: Can use fewer clones per step
- **Low correlation**: May need more clones
- **Criteria filtering**: Can reduce total clones needed

### 3. Quality Assessment

#### Data Quality Indicators
- **Outliers**: Number of potential outliers
- **Distribution**: Skewness and normality
- **Missing Data**: Completeness of dataset

#### Model Fit Assessment
- **Distribution Comparison**: Real vs synthetic data
- **Fit Quality**: How well the model matches your data
- **Recommendations**: Suggested improvements

---

## 🔍 Model Validation

### 1. Distribution Model Validation

#### Lognormal Model Check
**Validation Steps**:
1. Review distribution comparison plot
2. Check if synthetic data matches real data
3. Verify parameter estimates are reasonable
4. Test with different sample sizes

**Acceptance Criteria**:
- Synthetic data closely matches real data
- Parameter estimates are biologically plausible
- Model captures data distribution shape

#### KDE Model Check
**Validation Steps**:
1. Compare KDE vs lognormal results
2. Check for overfitting (too smooth or too rough)
3. Verify bandwidth selection is appropriate
4. Test with different sample sizes

**Acceptance Criteria**:
- KDE captures data distribution well
- No overfitting or underfitting
- Results are consistent across runs

### 2. Simulation Validation

#### Monte Carlo Convergence
**Check Convergence**:
1. Run simulations with different repetition counts
2. Compare results across different sample sizes
3. Check for stability in probability estimates
4. Verify confidence intervals are reasonable

**Convergence Criteria**:
- Results stabilize with increasing repetitions
- Standard error decreases with more repetitions
- Confidence intervals are reasonable

#### Parameter Sensitivity Validation
**Validation Steps**:
1. Test extreme parameter values
2. Verify logical consistency of results
3. Check for parameter interactions
4. Validate boundary conditions

**Validation Criteria**:
- Results are logically consistent
- Extreme values produce expected outcomes
- Parameter interactions are reasonable

### 3. Cross-Validation

#### Data Splitting
**Approach**:
1. Split data into training and validation sets
2. Run simulations on training data
3. Validate results on validation data
4. Compare performance across splits

#### Bootstrapping
**Approach**:
1. Generate bootstrap samples from your data
2. Run simulations on each bootstrap sample
3. Calculate confidence intervals
4. Assess stability of results

### 4. Model Comparison

#### Distribution Method Comparison
**Comparison Metrics**:
- Success probability estimates
- Confidence intervals
- Computational efficiency
- Interpretability

**Selection Criteria**:
- Choose method with better performance
- Consider computational requirements
- Balance accuracy vs. interpretability

#### Workflow Comparison
**Comparison Metrics**:
- Success probability
- Resource efficiency
- Computational cost
- Practical feasibility

**Selection Criteria**:
- Higher success probability
- Lower resource requirements
- Practical implementation considerations

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Data Loading Problems
**Issue**: "No 'Results' column found"
**Solution**: 
- Check column name spelling (must be exactly "Results")
- Ensure Excel file format is correct
- Verify file is not corrupted

**Issue**: "Selected sheet is empty"
**Solution**:
- Check if sheet contains data
- Verify sheet selection
- Try different sheets in the file

#### 2. Simulation Errors
**Issue**: "Step 1 keep exceeds available clones"
**Solution**:
- Reduce Step 1 keep value
- Check data filtering settings
- Verify criteria thresholds

**Issue**: "No positive data points for lognormal fitting"
**Solution**:
- Check for negative or zero values
- Use KDE method instead
- Clean data to remove invalid values

#### 3. Performance Issues
**Issue**: Simulations running very slowly
**Solutions**:
- Reduce Monte Carlo repetitions
- Use larger correlation step size
- Enable memory optimization
- Use parallel processing (if available)

**Issue**: Memory errors with large datasets
**Solutions**:
- Enable memory optimization
- Reduce simulation parameters
- Use smaller datasets for testing
- Increase system memory

#### 4. Visualization Problems
**Issue**: Charts not displaying
**Solutions**:
- Refresh the browser
- Check browser compatibility
- Clear browser cache
- Try different browser

**Issue**: Interactive features not working
**Solutions**:
- Ensure JavaScript is enabled
- Update browser to latest version
- Check for browser extensions interfering

### Error Messages and Meanings

#### Data-Related Errors
- **"No valid data points"**: All data values are invalid
- **"Insufficient data"**: Not enough data for analysis
- **"Invalid data type"**: Non-numeric values in Results column

#### Parameter-Related Errors
- **"Invalid parameter range"**: Parameter value outside allowed range
- **"Logical inconsistency"**: Parameters violate logical constraints
- **"Resource constraint"**: Parameter combination exceeds available resources

#### Simulation-Related Errors
- **"Convergence failure"**: Simulation did not converge
- **"Memory limit exceeded"**: Insufficient memory for simulation
- **"Timeout error"**: Simulation took too long to complete

---

## 💡 Best Practices

### 1. Data Preparation
- **Clean data thoroughly** before analysis
- **Document data sources** and processing steps
- **Validate data quality** using built-in tools
- **Keep original data** as backup

### 2. Parameter Selection
- **Start with recommended values** based on data size
- **Use sensitivity analysis** to identify key parameters
- **Test parameter ranges** systematically
- **Document parameter choices** and rationale

### 3. Model Validation
- **Always validate model assumptions**
- **Compare multiple approaches** when possible
- **Use cross-validation** for robust results
- **Document validation procedures**

### 4. Result Interpretation
- **Consider biological context** when interpreting results
- **Account for uncertainty** in estimates
- **Validate against domain knowledge**
- **Document interpretation assumptions**

### 5. Workflow Optimization
- **Balance performance vs. resources**
- **Consider practical constraints**
- **Plan for scalability**
- **Document optimization process**

### 6. Quality Assurance
- **Review results critically**
- **Check for logical consistency**
- **Validate against expectations**
- **Document quality checks**

---

## 📞 Support and Resources

### Getting Help
- **Check this guide** for common issues
- **Review error messages** carefully
- **Test with sample data** first
- **Document your workflow** for troubleshooting

### Additional Resources
- **Project documentation**: README.txt
- **Code comments**: Inline documentation in code
- **Streamlit documentation**: https://docs.streamlit.io/
- **Statistical references**: For model understanding

### Contact Information
For technical support or questions about the dashboard functionality, please refer to the inline documentation and tooltips within the application.

---

## 🔄 Version History

### v2.0 (Current) - Enhanced Dashboard
- Interactive visualizations with Plotly
- Comprehensive sensitivity analysis
- Advanced data validation and preprocessing
- Professional user interface
- Workflow comparison tools
- Export and reporting features

### v1.0 (Original) - Basic Dashboard
- Core Monte Carlo simulation
- Basic matplotlib visualizations
- Simple parameter configuration
- Basic data loading functionality

---

*This guide is designed to help you effectively use the CLD Clone Selection Dashboard for optimizing your cell line development processes. For the best results, follow the recommended workflows and validation procedures outlined in this document.* 