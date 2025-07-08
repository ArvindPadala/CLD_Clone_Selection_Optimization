import pandas as pd
import streamlit as st

def load_data(uploaded_file):
    sheet_names = pd.ExcelFile(uploaded_file).sheet_names
    selected_sheet = st.sidebar.selectbox("Select Sheet", sheet_names)
    df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
    criteria_columns = [col for col in df.columns if col.lower().startswith("criteria")]
    return df, selected_sheet, criteria_columns
