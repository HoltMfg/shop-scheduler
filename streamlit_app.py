import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Fuel Tank Scheduler", layout="wide")
st.title("Fuel Tank Production Scheduler")

with st.sidebar:
    st.header("Global Shop Settings")
    shifts_per_day = st.number_input("Shifts per Day", min_value=1, max_value=3, value=1)
    shift_length = st.number_input("Shift Length (Hours)", min_value=4, max_value=12, value=8)
    weld_ot = st.number_input("WELD Overtime (hrs)", min_value=0, max_value=4, value=0)

# Upload form
with st.form("upload"):
    project_name = st.text_input("Project Name")
    ops_file = st.file_uploader("Operations File", type="xlsx")
    stalls_file = st.file_uploader("Stalls File", type="xlsx")
    params_file = st.file_uploader("Parameters File", type="xlsx")
    submitted = st.form_submit_button("Upload Project")

if submitted and project_name and ops_file and stalls_file and params_file:
    try:
        ops_df = pd.read_excel(ops_file)
        stalls_df = pd.read_excel(stalls_file)
        params_df = pd.read_excel(params_file, header=None, names=["Param", "Value"])

        st.success(f"'{project_name}' uploaded successfully.")
        st.write("### Operations", ops_df)
        st.write("### Stalls", stalls_df)
        st.write("### Parameters", params_df.set_index("Param").T)

        # Simplified schedule generation (group by stall type and operation order)
        st.subheader("📅 Schedule Preview (Gantt-style)")
        schedule_df = ops_df.copy()
        schedule_df["Tank"] = "T1"
        schedule_df["Day"] = schedule_df.index + 1
        schedule_df["Stall"] = schedule_df["Stall Type"]
        schedule_df["Cycle Time"] = schedule_df["Hours"]
        gantt_view = schedule_df[["Tank", "Operation", "Stall", "Cycle Time", "Day"]]
        st.dataframe(gantt_view)

        # Simplified staffing matrix
        st.subheader("👷 Staffing Matrix")
        staffing = ops_df.groupby("Stall Type")["ManHours"].sum().reset_index()
        staffing["Workers Needed"] = (staffing["ManHours"] / (shifts_per_day * shift_length)).apply(lambda x: int(round(x + 0.5)))
        st.dataframe(staffing)

        # Excel export
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            ops_df.to_excel(writer, sheet_name="Operations", index=False)
            stalls_df.to_excel(writer, sheet_name="Stalls", index=False)
            params_df.to_excel(writer, sheet_name="Parameters", index=False)
            gantt_view.to_excel(writer, sheet_name="Schedule", index=False)
            staffing.to_excel(writer, sheet_name="Staffing", index=False)

        st.download_button(
            label="📥 Download Full Output Excel",
            data=output.getvalue(),
            file_name=f"{project_name}_Scheduler_Output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Error processing project: {e}")
