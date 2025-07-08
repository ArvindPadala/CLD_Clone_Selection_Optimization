import pandas as pd
import streamlit as st
import numpy as np

def load_data(uploaded_file):
    """
    Load and validate data from uploaded Excel file.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        tuple: (dataframe, selected_sheet, criteria_columns)
    """
    try:
        # Get sheet names
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names
        
        if not sheet_names:
            st.error("❌ No sheets found in the Excel file.")
            return None, None, []
        
        # Sheet selection
        selected_sheet = st.sidebar.selectbox(
            "Select Sheet", 
            sheet_names,
            help="Choose the sheet containing your assay data"
        )
        
        # Load data
        df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
        
        # Basic validation
        if df.empty:
            st.error("❌ Selected sheet is empty.")
            return None, selected_sheet, []
        
        # Check for required columns
        if "Results" not in df.columns:
            st.error("❌ No 'Results' column found. Please ensure your data has a column named 'Results'.")
            return None, selected_sheet, []
        
        # Data cleaning and preprocessing
        df = preprocess_data(df)
        
        # Identify criteria columns
        criteria_columns = [col for col in df.columns if col.lower().startswith("criteria")]
        
        # Display data summary
        display_data_summary(df, selected_sheet, criteria_columns)
        
        return df, selected_sheet, criteria_columns
        
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.exception(e)
        return None, None, []

def preprocess_data(df):
    """Preprocess and clean the data."""
    df_clean = df.copy()
    
    # Convert Results column to numeric, handling errors
    if "Results" in df_clean.columns:
        df_clean["Results"] = pd.to_numeric(df_clean["Results"], errors='coerce')
        
        # Remove rows with invalid Results
        initial_count = len(df_clean)
        df_clean = df_clean.dropna(subset=["Results"])
        removed_count = initial_count - len(df_clean)
        
        if removed_count > 0:
            st.warning(f"⚠️ Removed {removed_count} rows with invalid Results values.")
    
    # Process criteria columns
    criteria_columns = [col for col in df_clean.columns if col.lower().startswith("criteria")]
    for col in criteria_columns:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # Remove completely empty rows
    df_clean = df_clean.dropna(how='all')
    
    return df_clean

def display_data_summary(df, sheet_name, criteria_columns):
    """Display a summary of the loaded data."""
    st.sidebar.markdown("### 📊 Data Summary")
    
    # Basic statistics
    total_rows = len(df)
    valid_results = df["Results"].notna().sum()
    missing_results = total_rows - valid_results
    
    # Results statistics
    if valid_results > 0:
        results_stats = df["Results"].describe()
        
        st.sidebar.markdown(f"""
        **📈 Results Statistics:**
        - **Total Rows:** {total_rows:,}
        - **Valid Results:** {valid_results:,}
        - **Missing Results:** {missing_results:,}
        - **Mean:** {results_stats['mean']:.3f}
        - **Std Dev:** {results_stats['std']:.3f}
        - **Min:** {results_stats['min']:.3f}
        - **Max:** {results_stats['max']:.3f}
        """)
    
    # Criteria columns summary
    if criteria_columns:
        st.sidebar.markdown(f"**📋 Criteria Columns:** {len(criteria_columns)}")
        for col in criteria_columns:
            valid_count = df[col].notna().sum()
            st.sidebar.markdown(f"- {col}: {valid_count:,} valid values")
    
    # Data quality indicators
    st.sidebar.markdown("**🔍 Data Quality:**")
    
    # Check for outliers in Results
    if valid_results > 0:
        Q1 = df["Results"].quantile(0.25)
        Q3 = df["Results"].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df["Results"] < Q1 - 1.5 * IQR) | (df["Results"] > Q3 + 1.5 * IQR)]
        
        if len(outliers) > 0:
            st.sidebar.markdown(f"⚠️ **Outliers:** {len(outliers)} potential outliers detected")
        else:
            st.sidebar.markdown("✅ **Outliers:** No significant outliers detected")
    
    # Check data distribution
    if valid_results > 0:
        skewness = df["Results"].skew()
        if abs(skewness) > 1:
            st.sidebar.markdown(f"📊 **Distribution:** Skewed ({skewness:.2f})")
        else:
            st.sidebar.markdown("📊 **Distribution:** Approximately normal")

def validate_workflow_parameters(df, step1_keep, step2_keep, step3_keep, workflow_steps):
    """Validate workflow parameters against the data."""
    errors = []
    warnings = []
    
    total_clones = len(df["Results"].dropna())
    
    # Check if step1_keep exceeds available data
    if step1_keep > total_clones:
        errors.append(f"Step 1 keep ({step1_keep}) exceeds available clones ({total_clones})")
    
    # Check logical consistency
    if step2_keep > step1_keep:
        errors.append(f"Step 2 keep ({step2_keep}) cannot exceed step 1 keep ({step1_keep})")
    
    if workflow_steps == 3 and step3_keep > step2_keep:
        errors.append(f"Step 3 keep ({step3_keep}) cannot exceed step 2 keep ({step2_keep})")
    
    # Check for reasonable values
    if step1_keep < 10:
        warnings.append("Step 1 keep is very small (< 10), which may lead to poor selection")
    
    if step2_keep < 5:
        warnings.append("Step 2 keep is very small (< 5), which may lead to poor selection")
    
    if step3_keep < 3:
        warnings.append("Final selection is very small (< 3), consider increasing")
    
    # Check reduction ratios
    reduction_ratio_1 = step1_keep / step2_keep if step2_keep > 0 else float('inf')
    reduction_ratio_2 = step2_keep / step3_keep if step3_keep > 0 else float('inf')
    
    if reduction_ratio_1 < 2:
        warnings.append("Step 1 to Step 2 reduction ratio is low (< 2)")
    
    if workflow_steps == 3 and reduction_ratio_2 < 2:
        warnings.append("Step 2 to Step 3 reduction ratio is low (< 2)")
    
    return errors, warnings

def get_data_recommendations(df, criteria_columns):
    """Generate recommendations based on data characteristics."""
    recommendations = []
    
    total_clones = len(df["Results"].dropna())
    
    # Recommend step sizes based on data size
    if total_clones >= 2000:
        recommendations.append("📊 **Large dataset detected** - Consider using 96-192 clones in Step 1")
    elif total_clones >= 1000:
        recommendations.append("📊 **Medium dataset detected** - Consider using 48-96 clones in Step 1")
    else:
        recommendations.append("📊 **Small dataset detected** - Consider using 24-48 clones in Step 1")
    
    # Check for criteria columns
    if criteria_columns:
        recommendations.append("📋 **Criteria columns found** - Consider using filtering to improve selection quality")
    else:
        recommendations.append("📋 **No criteria columns** - Consider adding quality criteria for better filtering")
    
    # Check data distribution
    if len(df["Results"].dropna()) > 0:
        skewness = df["Results"].skew()
        if abs(skewness) > 2:
            recommendations.append("📈 **Highly skewed data** - Consider using KDE instead of lognormal distribution")
        elif abs(skewness) > 1:
            recommendations.append("📈 **Moderately skewed data** - Both lognormal and KDE should work well")
        else:
            recommendations.append("📈 **Normal-like data** - Lognormal distribution should work well")
    
    return recommendations
