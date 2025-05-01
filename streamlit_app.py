import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fuel Tank Scheduler", layout="wide")
st.title("Fuel Tank Production Scheduler")

st.markdown("Upload project files and adjust shop settings.")

with st.form("upload_form"):
    project_name = st.text_input("Project Name")
    ops_file = st.file_uploader("Operations.xlsx", type="xlsx")
    stalls_file = st.file_uploader("Stalls.xlsx", type="xlsx")
    params_file = st.file_uploader("Parameters.xlsx", type="xlsx")
    submitted = st.form_submit_button("Upload")

if submitted and project_name and ops_file and stalls_file and params_file:
    st.success(f"Project '{project_name}' uploaded successfully!")
    # Actual scheduling logic would follow here.

st.header("Global Settings")
st.number_input("Shifts per Day", min_value=1, max_value=3, value=1)
st.number_input("Shift Length (hrs)", min_value=4, max_value=12, value=8)
st.number_input("WELD Overtime (hrs)", min_value=0, max_value=4, value=0)

st.button("Generate Schedule")
