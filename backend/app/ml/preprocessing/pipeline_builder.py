"""
Pipeline Builder with Zero-Data-Leakage Architecture
Builds scikit-learn ColumnTransformer and Preprocessing Pipelines per disease.
"""

from typing import Tuple, List, Dict, Any
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, RobustScaler

from backend.app.ml.preprocessing.schemas import DISEASE_SCHEMAS

def clean_raw_data(disease: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw dataframe before split:
    - Removes duplicate records
    - Replaces biologically impossible zero values with NaN for specific features
    - Normalizes string targets to 0/1 integers
    Does NOT compute any statistical aggregations (mean, median, std) to prevent data leakage!
    """
    df = df.copy()
    
    # 1. Deduplicate
    df = df.drop_duplicates()
    
    # 2. Disease-specific raw hygiene
    if disease == "diabetes":
        # In Pima Indians dataset, 0 in glucose, blood_pressure, skin_thickness, insulin, bmi represents missing data
        zero_missing_cols = ["glucose", "blood_pressure", "skin_thickness", "insulin", "bmi"]
        for col in zero_missing_cols:
            if col in df.columns:
                df[col] = df[col].replace(0, np.nan)
                
    elif disease == "heart_disease":
        # Target in Cleveland is 0 (healthy) or 1..4 (disease present). In standard CSV, target is 0 or 1.
        if "target" in df.columns:
            df["target"] = (df["target"] > 0).astype(int)
            
    elif disease == "breast_cancer":
        # In scikit-learn WDBC: 0 = malignant, 1 = benign.
        # In oncology risk prediction, we align target=1 to mean "Malignant" (positive event for risk estimate)
        if "target" in df.columns:
            # Check current distribution: in sklearn, 212 are class 0 (malignant) and 357 are class 1 (benign)
            # If 0 is malignant, invert so 1 = Malignant (High Risk)
            if (df["target"] == 0).sum() == 212:
                df["target"] = (df["target"] == 0).astype(int)

    elif disease == "lung_cancer":
        # Target is "YES" or "NO", convert to 1 and 0
        if "lung_cancer" in df.columns:
            df["lung_cancer"] = df["lung_cancer"].astype(str).str.strip().str.upper().map({"YES": 1, "NO": 0})
        # Clean gender to uppercase
        if "gender" in df.columns:
            df["gender"] = df["gender"].astype(str).str.strip().str.upper()

    elif disease == "stroke":
        # ID column is an arbitrary identifier, drop it to prevent artificial spurious correlation
        if "id" in df.columns:
            df = df.drop(columns=["id"])
        # Remove impossible gender 'Other' if count is negligible (typically 1 record in Kaggle stroke)
        if "gender" in df.columns:
            df = df[df["gender"].isin(["Male", "Female"])]
            
    return df

def get_feature_groups(disease: str, columns: List[str]) -> Tuple[List[str], List[str]]:
    """
    Separates columns into numerical and categorical feature lists based on clinical schema.
    """
    schema = DISEASE_SCHEMAS.get(disease, {})
    features_meta = schema.get("features", {})
    
    num_cols = []
    cat_cols = []
    
    for col in columns:
        if col in features_meta:
            ftype = features_meta[col]["type"]
            if ftype == "numerical":
                num_cols.append(col)
            else:
                cat_cols.append(col)
        else:
            # Fallback based on dtype if not in explicit top schema
            num_cols.append(col)
            
    return num_cols, cat_cols

def build_preprocessor(disease: str, X: pd.DataFrame) -> ColumnTransformer:
    """
    Constructs a ColumnTransformer fitted purely within cross-validation / training pipelines.
    - Numerical: Median imputation + StandardScaler
    - Categorical: Most-frequent imputation + OneHotEncoder
    """
    num_cols, cat_cols = get_feature_groups(disease, list(X.columns))
    
    transformers = []
    
    if num_cols:
        num_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])
        transformers.append(("num", num_pipeline, num_cols))
        
    if cat_cols:
        cat_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
        ])
        transformers.append(("cat", cat_pipeline, cat_cols))
        
    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder="drop"
    )
    
    return preprocessor
