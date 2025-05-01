import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fuel Tank Scheduler", layout="wide")
st.title("Fuel Tank Production Scheduler")

# Upload form
with st.form("upload"):
    project_name = st.text_input("Project Name")
    ops_file = st.file_uploader("Operations File", type="xlsx")
    stalls_file = st.file_uploader("Stalls File", type="xlsx")
    params_file = st.file_uploader("Parameters File", type="xlsx")
    submitted = st.form_submit_button("Upload Project")

if submitted and project_name and ops_file and stalls_file and params_file:
    st.success(f"'{project_name}' uploaded. Scheduling logic would execute here.")
    # Logic placeholders
    try:
        ops_df = pd.read_excel(ops_file)
        stalls_df = pd.read_excel(stalls_file)
        params_df = pd.read_excel(params_file, header=None, names=["Param", "Value"])

        st.write("### Operations Preview", ops_df.head())
        st.write("### Stalls Preview", stalls_df.head())
        st.write("### Parameters", params_df.set_index("Param").T)
    except Exception as e:
        st.error(f"Failed to process inputs: {e}")

# Global settings
st.sidebar.header("Global Shift Rules")
st.sidebar.number_input("Shifts per Day", min_value=1, max_value=3, value=1)
st.sidebar.number_input("Shift Length (hours)", min_value=4, max_value=12, value=8)
st.sidebar.number_input("WELD Overtime (hours)", min_value=0, max_value=4, value=0)

# Stubbed action
if st.button("Generate Merged Schedule"):
    st.info("Scheduling logic would run here and generate downloadable files.")
