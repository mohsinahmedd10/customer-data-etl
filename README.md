# Customer Data Cleaning and Analysis System

## Project idea
**Customer Data Cleaning and Analysis System** demonstrates a complete ETL workflow on a synthetic customer dataset.

### Why this project?
It is easy to explain because every step has a clear business reason:
1. Extract raw customer data.
2. Detect and remove duplicate records.
3. Handle missing numerical values with the mean.
4. Handle missing categorical values with the mode.
5. Encode categorical data using One-Hot Encoding.
6. Standardize numerical features using StandardScaler.
7. Load the cleaned/transformed data into CSV files.
8. Analyze customers by city, category and spending.

## Folder structure
```
customer_data_etl_project/
├── app.py
├── etl_pipeline.py
├── requirements.txt
├── run_project.bat
├── README.md
└── data/
    ├── raw_customer_data.csv
    ├── cleaned_customer_data.csv
    └── transformed_customer_data.csv
```

## Run in VS Code
1. Open this folder in VS Code.
2. Open Terminal.
3. Run:
   `pip install -r requirements.txt`
4. Then run:
   `streamlit run app.py`
5. A browser tab will open with the project dashboard.
6. Click **Run ETL Pipeline**.

Windows users can also double-click `run_project.bat`.

## Presentation explanation
**Problem:** Raw customer data may contain duplicates, missing values and categorical text that is not directly suitable for analysis.

**Solution:** Build an ETL pipeline.

**Extract:** Read the raw CSV using Pandas.

**Transform:** Remove duplicates, fill numerical missing values with mean, fill categorical missing values with mode, standardize column names, one-hot encode categorical columns and standardize numerical columns.

**Load:** Save the cleaned and transformed datasets as CSV files.

**Result:** The data becomes consistent, complete and ready for analysis.

> Note: The dataset in this project is synthetic and created only for academic demonstration. No real customer information is used.
