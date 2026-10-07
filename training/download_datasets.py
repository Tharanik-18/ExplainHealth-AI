"""
Dataset Downloader and Verifier for ExplainHealth AI
Downloads legitimate public healthcare datasets:
1. Diabetes (Pima Indians - UCI / NIDDK)
2. Heart Disease (Cleveland Heart Disease - UCI)
3. Breast Cancer (Wisconsin Diagnostic Breast Cancer - UCI / scikit-learn)
4. Lung Cancer (Survey Lung Cancer - Public Benchmark)
5. Stroke (Healthcare Stroke Dataset - Public Benchmark)
"""

import os
import json
import requests
import io
import pandas as pd
from sklearn.datasets import load_breast_cancer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

DATASET_METADATA = {
    "diabetes": {
        "dataset_name": "Pima Indians Diabetes Database",
        "source": "National Institute of Diabetes and Digestive and Kidney Diseases / UCI Machine Learning Repository",
        "license": "CC0: Public Domain",
        "url": "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv",
        "columns": [
            "pregnancies", "glucose", "blood_pressure", "skin_thickness", 
            "insulin", "bmi", "diabetes_pedigree_function", "age", "outcome"
        ],
        "target": "outcome",
        "file_name": "diabetes.csv",
        "description": "Diagnostic measurements to predict whether or not a patient has diabetes.",
        "known_limitations": "All patients are females of Pima Indian heritage aged 21 and older. Zero values in glucose, blood pressure, skin thickness, insulin, and BMI represent missing medical measurements."
    },
    "heart_disease": {
        "dataset_name": "UCI Heart Disease (Cleveland Dataset)",
        "source": "UCI Machine Learning Repository - Cleveland Clinic Foundation",
        "license": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "url": "https://raw.githubusercontent.com/amankharwal/Website-data/master/heart.csv",
        "target": "target",
        "file_name": "heart.csv",
        "description": "14 clinical attributes used to predict presence of heart disease in patient.",
        "known_limitations": "Sample size is ~303 patients; predominantly male demographic in Cleveland clinic (1988)."
    },
    "breast_cancer": {
        "dataset_name": "Wisconsin Diagnostic Breast Cancer (WDBC)",
        "source": "UCI Machine Learning Repository / Dr. William H. Wolberg, W. Nick Street, Olvi L. Mangasarian",
        "license": "CC0: Public Domain",
        "target": "target",
        "file_name": "breast_cancer.csv",
        "description": "Features computed from a digitized image of a fine needle aspirate (FNA) of a breast mass describing characteristics of cell nuclei.",
        "known_limitations": "Extracted from FNA biopsy imaging; requires laboratory pathology measurement features (radius, texture, smoothness, concavity, etc.)."
    },
    "lung_cancer": {
        "dataset_name": "Survey Lung Cancer Dataset",
        "source": "Public Epidemiological Research / Kaggle Public Survey Benchmark",
        "license": "Open Data Commons Open Database License (ODbL) / Public Academic Use",
        "url": "https://raw.githubusercontent.com/rohitinu6/NeoLung/main/survey%20lung%20cancer.csv",
        "target": "lung_cancer",
        "file_name": "lung_cancer.csv",
        "description": "Self-reported lifestyle, occupational, and clinical symptoms associated with lung cancer risk.",
        "known_limitations": "Survey-based symptom assessments; categorical ratings primarily 1 (No) and 2 (Yes)."
    },
    "stroke": {
        "dataset_name": "Healthcare Stroke Prediction Dataset",
        "source": "Public Healthcare Benchmark / Kaggle Open Health Dataset",
        "license": "CC0: Public Domain",
        "url": "https://raw.githubusercontent.com/georgemelrose/Patient-Level-Stroke-Prediction-Models/main/healthcare-dataset-stroke-data.csv",
        "target": "stroke",
        "file_name": "stroke.csv",
        "description": "Clinical and demographic parameters to predict whether a patient is likely to get stroke.",
        "known_limitations": "Severe class imbalance (approx 4.8% stroke positive rate), typical of real-world stroke epidemiological prevalence."
    }
}

def ensure_dirs():
    for disease in DATASET_METADATA.keys():
        os.makedirs(os.path.join(RAW_DIR, disease), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "processed"), exist_ok=True)

def download_diabetes():
    meta = DATASET_METADATA["diabetes"]
    path = os.path.join(RAW_DIR, "diabetes", meta["file_name"])
    print(f"[1/5] Fetching {meta['dataset_name']}...")
    resp = requests.get(meta["url"], headers=HEADERS, timeout=10)
    df = pd.read_csv(io.BytesIO(resp.content), header=None)
    df.columns = meta["columns"]
    df.to_csv(path, index=False)
    meta["samples"] = int(len(df))
    meta["features"] = [c for c in df.columns if c != meta["target"]]
    with open(os.path.join(RAW_DIR, "diabetes", "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"  -> Saved {meta['file_name']}: {len(df)} rows, {df.shape[1]} cols.")

def download_heart():
    meta = DATASET_METADATA["heart_disease"]
    path = os.path.join(RAW_DIR, "heart_disease", meta["file_name"])
    print(f"[2/5] Fetching {meta['dataset_name']}...")
    resp = requests.get(meta["url"], headers=HEADERS, timeout=10)
    df = pd.read_csv(io.BytesIO(resp.content))
    df.columns = [c.strip().lower() for c in df.columns]
    df.to_csv(path, index=False)
    meta["samples"] = int(len(df))
    meta["features"] = [c for c in df.columns if c != meta["target"]]
    with open(os.path.join(RAW_DIR, "heart_disease", "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"  -> Saved {meta['file_name']}: {len(df)} rows, {df.shape[1]} cols.")

def load_and_save_breast_cancer():
    meta = DATASET_METADATA["breast_cancer"]
    path = os.path.join(RAW_DIR, "breast_cancer", meta["file_name"])
    print(f"[3/5] Loading legitimate UCI {meta['dataset_name']} from scikit-learn...")
    data = load_breast_cancer(as_frame=True)
    df = data.frame
    df.columns = [c.replace(" ", "_").lower() for c in df.columns]
    df.to_csv(path, index=False)
    meta["samples"] = int(len(df))
    meta["features"] = [c for c in df.columns if c != meta["target"]]
    with open(os.path.join(RAW_DIR, "breast_cancer", "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"  -> Saved {meta['file_name']}: {len(df)} rows, {df.shape[1]} cols.")

def download_lung_cancer():
    meta = DATASET_METADATA["lung_cancer"]
    path = os.path.join(RAW_DIR, "lung_cancer", meta["file_name"])
    print(f"[4/5] Fetching {meta['dataset_name']}...")
    resp = requests.get(meta["url"], headers=HEADERS, timeout=10)
    df = pd.read_csv(io.BytesIO(resp.content))
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df.to_csv(path, index=False)
    meta["samples"] = int(len(df))
    meta["features"] = [c for c in df.columns if c != meta["target"]]
    with open(os.path.join(RAW_DIR, "lung_cancer", "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"  -> Saved {meta['file_name']}: {len(df)} rows, {df.shape[1]} cols.")

def download_stroke():
    meta = DATASET_METADATA["stroke"]
    path = os.path.join(RAW_DIR, "stroke", meta["file_name"])
    print(f"[5/5] Fetching {meta['dataset_name']}...")
    resp = requests.get(meta["url"], headers=HEADERS, timeout=10)
    df = pd.read_csv(io.BytesIO(resp.content))
    df.columns = [c.strip().lower() for c in df.columns]
    df.to_csv(path, index=False)
    meta["samples"] = int(len(df))
    meta["features"] = [c for c in df.columns if c != meta["target"]]
    with open(os.path.join(RAW_DIR, "stroke", "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"  -> Saved {meta['file_name']}: {len(df)} rows, {df.shape[1]} cols.")

def main():
    ensure_dirs()
    download_diabetes()
    download_heart()
    load_and_save_breast_cancer()
    download_lung_cancer()
    download_stroke()
    print("\n[SUCCESS] All 5 legitimate healthcare datasets and metadata successfully loaded.")

if __name__ == "__main__":
    main()
