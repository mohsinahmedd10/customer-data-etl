"""
Customer Data ETL Pipeline
E = Extract raw customer CSV
T = Clean, transform and validate
L = Save cleaned and transformed CSV files
"""
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE = Path(__file__).resolve().parent
RAW = BASE / "data" / "raw_customer_data.csv"
CLEANED = BASE / "data" / "cleaned_customer_data.csv"
TRANSFORMED = BASE / "data" / "transformed_customer_data.csv"

def run_pipeline():
    # EXTRACT
    df = pd.read_csv(RAW)
    original_rows = len(df)

    # TRANSFORM: remove duplicates
    duplicates = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    # TRANSFORM: missing values
    numerical_cols = df.select_dtypes(include=np.number).columns
    categorical_cols = df.select_dtypes(include="object").columns

    for col in numerical_cols:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].mean())

    for col in categorical_cols:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].mode()[0])

    # Standardize column names
    df.columns = df.columns.str.replace(" ", "_").str.lower()

    # LOAD: cleaned human-readable dataset
    df.to_csv(CLEANED, index=False)

    # Additional transformation for analytics/model-ready data
    encode_cols = ["gender", "city", "preferred_category", "satisfaction"]
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    encoded = encoder.fit_transform(df[encode_cols])
    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.get_feature_names_out(encode_cols),
        index=df.index,
    )

    model_df = df.drop(columns=encode_cols).join(encoded_df)
    scale_cols = ["age", "income", "purchase_count", "total_spend"]
    scaler = StandardScaler()
    model_df[scale_cols] = scaler.fit_transform(model_df[scale_cols])
    model_df.to_csv(TRANSFORMED, index=False)

    return {
        "original_rows": original_rows,
        "duplicates_removed": duplicates,
        "final_rows": len(df),
        "missing_after": int(df.isna().sum().sum()),
        "cleaned_file": str(CLEANED),
        "transformed_file": str(TRANSFORMED),
    }

if __name__ == "__main__":
    print(run_pipeline())
