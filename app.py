import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
from etl_pipeline import run_pipeline

st.set_page_config(page_title="Customer ETL Dashboard", page_icon="📊", layout="wide")

st.title("📊 Customer Data Cleaning & Analysis System")
st.caption("Academic ETL project — Extract → Transform → Load → Analyze")

if st.button("▶ Run ETL Pipeline", type="primary"):
    with st.spinner("Running ETL pipeline..."):
        result = run_pipeline()
    st.session_state["result"] = result
    st.success("ETL pipeline completed successfully.")

raw = pd.read_csv(BASE/"data/raw_customer_data.csv")
clean = pd.read_csv(BASE/"data/cleaned_customer_data.csv")

r = st.session_state.get("result")
c1,c2,c3,c4 = st.columns(4)
c1.metric("Raw Records", len(raw))
c2.metric("Duplicates", int(raw.duplicated().sum()))
c3.metric("Clean Records", len(clean))
c4.metric("Missing After ETL", int(clean.isna().sum().sum()))

st.divider()
tab1, tab2, tab3, tab4 = st.tabs(["🔎 Data Quality", "📈 Analysis", "🧹 ETL Preview", "📥 Output"])

with tab1:
    st.subheader("Data quality before and after")
    before_missing = int(raw.isna().sum().sum())
    after_missing = int(clean.isna().sum().sum())
    st.write(f"Missing values before cleaning: **{before_missing}**")
    st.write(f"Missing values after cleaning: **{after_missing}**")
    st.dataframe(pd.DataFrame({
        "Column": raw.columns,
        "Missing Before": raw.isna().sum().values,
        "Missing After": clean.isna().sum().values
    }), use_container_width=True)

with tab2:
    st.subheader("Customer analysis")
    col1,col2 = st.columns(2)
    with col1:
        st.write("Customers by city")
        st.bar_chart(clean["city"].value_counts())
    with col2:
        st.write("Preferred category")
        st.bar_chart(clean["preferred_category"].value_counts())
    st.write("Average total spend by preferred category")
    st.bar_chart(clean.groupby("preferred_category")["total_spend"].mean().sort_values(ascending=False))

with tab3:
    st.subheader("Raw data")
    st.dataframe(raw.head(10), use_container_width=True)
    st.subheader("Cleaned data")
    st.dataframe(clean.head(10), use_container_width=True)
    st.info("Transformations: duplicate removal → mean imputation for numerical columns → mode imputation for categorical columns → lowercase/underscore column names → one-hot encoding → standardization.")

with tab4:
    st.subheader("Generated files")
    st.write("**cleaned_customer_data.csv** — cleaned, readable dataset")
    st.write("**transformed_customer_data.csv** — encoded and standardized dataset")
    for fn in ["cleaned_customer_data.csv","transformed_customer_data.csv"]:
        data=(BASE/"data"/fn).read_bytes()
        st.download_button(f"Download {fn}", data=data, file_name=fn, mime="text/csv")

st.divider()
st.caption("Prepared for college ETL/Data Science presentation. Dataset is synthetic and intended for academic demonstration.")
