import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fuel Tank Scheduler", layout="wide")
st.title("Fuel Tank Production Scheduler")

st.markdown("Upload your project files and configure shop rules below.")

with st.form("upload_form"):
    project_name = st.text_input("Project Name")
    operations_file = st.file_uploader("Operations File (.xlsx)", type="xlsx")
    stalls_file = st.file_uploader("Stalls File (.xlsx)", type="xlsx")
    params_file = st.file_uploader("Parameters File (.xlsx)", type="xlsx")
    submitted = st.form_submit_button("Upload Project")

if submitted and project_name and operations_file and stalls_file and params_file:
    st.success(f"Project '{project_name}' uploaded successfully!")
    # Placeholder: save files, parse, validate, store status, etc.

st.header("Global Shop Settings")
st.number_input("Shifts per Day", min_value=1, max_value=3, value=1)
st.number_input("Shift Length (Hours)", min_value=4, max_value=12, value=8)
st.number_input("WELD Overtime Allowed (Hours)", min_value=0, max_value=4, value=0)

st.button("Generate Schedule (All Active Projects)")
