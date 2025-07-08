CLD Clone Selection Simulation Dashboard
========================================
Team: BlackCloud
Members: 1. Arvind Chary Padala
         2. Tanishq Sharma
         
Overview:
---------
This Streamlit-based dashboard simulates clone selection workflows in Cell Line Development (CLD). It estimates how likely your final selected clones are to be among the top-performing clones, based on assay data and customizable workflow steps.

Key Features:
-------------
- Upload Excel files with assay results and optional selection criteria
- Visualize distributions for each criteria
- Choose between LogNormal (parametric) and KDE (non-parametric) modeling
- Run Monte Carlo simulations across correlation values
- Visualize success probability vs correlation
- Plot histogram showing how many final clones fall into the top X%
- Apply filtering criteria at any stage of the workflow

Expected Input Format:
----------------------
- Excel file (.xlsx) with:
  - One column named **"Results"** containing numeric assay values
  - Optional columns starting with **"Criteria"** (e.g., Criteria1, Criteria2...) for filtering

Folder Structure:
-----------------
app.py               - Main Streamlit app  
loader.py            - File upload and sheet selector  
sidebar.py           - Sidebar UI and user input controls  
simulation.py        - Monte Carlo simulation logic and sampling  
plots.py             - Plotting logic using matplotlib  
requirements.txt     - Python dependencies  
README.txt           - This file

How to Run:
-----------
1. Make sure Python 3.8+ is installed.

2. Install required dependencies:
   > pip install -r requirements.txt

3. Launch the dashboard:
   > streamlit run app.py

4. The app will open in your browser. Use the sidebar to:
   - Upload your Excel file
   - Configure workflow steps and selection thresholds
   - Choose modeling method (LogNormal / KDE)
   - Run simulations and view results interactively

Tip:
----
To reset the app between uploads or settings, click "Rerun" in the top-right menu of Streamlit.
