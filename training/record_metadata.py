"""
Dataset Downloader and Metadata Registry for ExplainHealth AI
"""

import os
import json
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")

DATASET_METADATA = {
    "diabetes": {
        "dataset_name": "Pima Indians Diabetes Database",
        "source": "National Institute of Diabetes and Digestive and Kidney Diseases / UCI Machine Learning Repository",
        "license": "CC0: Public Domain",
        "file_name": "diabetes.csv",
        "target": "outcome",
        "positive_label_meaning": "Presence of Diabetes (Type 2)",
        "features": [
            "pregnancies", "glucose", "blood_pressure", "skin_thickness", 
            "insulin", "bmi", "diabetes_pedigree_function", "age"
        ],
        "feature_descriptions": {
            "pregnancies": "Number of times pregnant",
            "glucose": "Plasma glucose concentration a 2 hours in an oral glucose tolerance test (mg/dL)",
            "blood_pressure": "Diastolic blood pressure (mm Hg)",
            "skin_thickness": "Triceps skin fold thickness (mm)",
            "insulin": "2-Hour serum insulin (mu U/ml)",
            "bmi": "Body mass index (weight in kg/(height in m)^2)",
            "diabetes_pedigree_function": "Diabetes pedigree function (genetic score)",
            "age": "Age in years"
        },
        "description": "Diagnostic measurements to predict whether or not a patient has diabetes based on diagnostic metabolic factors.",
        "known_limitations": "All patients are females of Pima Indian heritage aged 21 and older. Zero values in glucose, blood pressure, skin thickness, insulin, and BMI represent missing medical measurements that require imputation."
    },
    "heart_disease": {
        "dataset_name": "UCI Heart Disease (Cleveland Clinic Dataset)",
        "source": "UCI Machine Learning Repository - Cleveland Clinic Foundation",
        "license": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "file_name": "heart.csv",
        "target": "target",
        "positive_label_meaning": "Presence of Heart Disease (> 50% diameter narrowing)",
        "features": [
            "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", 
            "thalach", "exang", "oldpeak", "slope", "ca", "thal"
        ],
        "feature_descriptions": {
            "age": "Age in years",
            "sex": "Sex (1 = male; 0 = female)",
            "cp": "Chest pain type (0: typical angina, 1: atypical angina, 2: non-anginal pain, 3: asymptomatic)",
            "trestbps": "Resting blood pressure in mm Hg on admission to the hospital",
            "chol": "Serum cholesterol in mg/dl",
            "fbs": "Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)",
            "restecg": "Resting electrocardiographic results (0: normal, 1: ST-T wave abnormality, 2: probable or definite left ventricular hypertrophy)",
            "thalach": "Maximum heart rate achieved during exercise stress test",
            "exang": "Exercise induced angina (1 = yes; 0 = no)",
            "oldpeak": "ST depression induced by exercise relative to rest",
            "slope": "The slope of the peak exercise ST segment (0: upsloping, 1: flat, 2: downsloping)",
            "ca": "Number of major vessels (0-3) colored by fluoroscopy",
            "thal": "Thalassemia blood disorder (1: normal, 2: fixed defect, 3: reversible defect)"
        },
        "description": "14 clinical attributes used to predict presence of heart disease in patient.",
        "known_limitations": "Sample size is ~303 patients; predominantly male demographic in Cleveland clinic (1988)."
    },
    "breast_cancer": {
        "dataset_name": "Wisconsin Diagnostic Breast Cancer (WDBC)",
        "source": "UCI Machine Learning Repository / Dr. William H. Wolberg, W. Nick Street, Olvi L. Mangasarian",
        "license": "CC0: Public Domain",
        "file_name": "breast_cancer.csv",
        "target": "target",
        "positive_label_meaning": "Malignant Breast Tumor (1 = Malignant in raw target, inverted if needed for risk probability)",
        "features": [
            "mean_radius", "mean_texture", "mean_perimeter", "mean_area",
            "mean_smoothness", "mean_compactness", "mean_concavity",
            "mean_concave_points", "mean_symmetry", "mean_fractal_dimension",
            "radius_error", "texture_error", "perimeter_error", "area_error",
            "smoothness_error", "compactness_error", "concavity_error",
            "concave_points_error", "symmetry_error",
            "fractal_dimension_error", "worst_radius", "worst_texture",
            "worst_perimeter", "worst_area", "worst_smoothness",
            "worst_compactness", "worst_concavity", "worst_concave_points",
            "worst_symmetry", "worst_fractal_dimension"
        ],
        "feature_descriptions": {
            "mean_radius": "Mean of distances from center to points on the perimeter",
            "mean_texture": "Standard deviation of gray-scale values",
            "mean_perimeter": "Mean size of the core tumor perimeter",
            "mean_area": "Mean size of the core tumor area",
            "mean_smoothness": "Mean of local variation in radius lengths",
            "mean_compactness": "Mean of perimeter^2 / area - 1.0",
            "mean_concavity": "Mean of severity of concave portions of the contour",
            "mean_concave_points": "Mean for number of concave portions of the contour",
            "mean_symmetry": "Mean nuclear symmetry",
            "mean_fractal_dimension": "Mean coastline approximation - 1"
        },
        "description": "Features computed from a digitized image of a fine needle aspirate (FNA) of a breast mass describing characteristics of cell nuclei.",
        "known_limitations": "Extracted from FNA biopsy pathology imaging; requires laboratory cytology measurements."
    },
    "lung_cancer": {
        "dataset_name": "Survey Lung Cancer Dataset",
        "source": "Public Epidemiological Research / Kaggle Public Survey Benchmark",
        "license": "Open Data Commons Open Database License (ODbL) / Public Academic Use",
        "file_name": "lung_cancer.csv",
        "target": "lung_cancer",
        "positive_label_meaning": "Elevated Lung Cancer Risk Indicator",
        "features": [
            "gender", "age", "smoking", "yellow_fingers", "anxiety",
            "peer_pressure", "chronic_disease", "fatigue", "allergy", "wheezing",
            "alcohol_consuming", "coughing", "shortness_of_breath",
            "swallowing_difficulty", "chest_pain"
        ],
        "feature_descriptions": {
            "gender": "Biological sex (M/F)",
            "age": "Age in years",
            "smoking": "Smoking habit (1 = No, 2 = Yes)",
            "yellow_fingers": "Staining of fingers from smoking (1 = No, 2 = Yes)",
            "anxiety": "History of anxiety symptoms (1 = No, 2 = Yes)",
            "peer_pressure": "Exposure to social tobacco smoke peer pressure (1 = No, 2 = Yes)",
            "chronic_disease": "Presence of chronic respiratory or pulmonary conditions (1 = No, 2 = Yes)",
            "fatigue": "Persistent unexplained physical fatigue (1 = No, 2 = Yes)",
            "allergy": "Known respiratory allergies (1 = No, 2 = Yes)",
            "wheezing": "Wheezing breath sounds (1 = No, 2 = Yes)",
            "alcohol_consuming": "Alcohol consumption habits (1 = No, 2 = Yes)",
            "coughing": "Persistent coughing (1 = No, 2 = Yes)",
            "shortness_of_breath": "Shortness of breath / dyspnea (1 = No, 2 = Yes)",
            "swallowing_difficulty": "Dysphagia / swallowing difficulty (1 = No, 2 = Yes)",
            "chest_pain": "Recurrent chest pain (1 = No, 2 = Yes)"
        },
        "description": "Self-reported lifestyle, occupational, and clinical symptoms associated with lung cancer risk.",
        "known_limitations": "Survey-based symptom assessments; categorical ratings 1 (No) and 2 (Yes)."
    },
    "stroke": {
        "dataset_name": "Healthcare Stroke Prediction Dataset",
        "source": "Public Healthcare Benchmark / Kaggle Open Health Dataset",
        "license": "CC0: Public Domain",
        "file_name": "stroke.csv",
        "target": "stroke",
        "positive_label_meaning": "Presence of Stroke Episode",
        "features": [
            "gender", "age", "hypertension", "heart_disease", "ever_married",
            "work_type", "residence_type", "avg_glucose_level", "bmi", "smoking_status"
        ],
        "feature_descriptions": {
            "gender": "Gender ('Male', 'Female', or 'Other')",
            "age": "Age in years",
            "hypertension": "Hypertension (0 = no, 1 = yes)",
            "heart_disease": "Pre-existing heart disease (0 = no, 1 = yes)",
            "ever_married": "Marital history ('No' or 'Yes')",
            "work_type": "Employment category ('children', 'Govt_job', 'Never_worked', 'Private', 'Self-employed')",
            "residence_type": "Residence setting ('Rural' or 'Urban')",
            "avg_glucose_level": "Average blood glucose level (mg/dL)",
            "bmi": "Body Mass Index (kg/m^2)",
            "smoking_status": "Smoking history ('formerly smoked', 'never smoked', 'smokes', 'Unknown')"
        },
        "description": "Clinical and demographic parameters to predict whether a patient is likely to get stroke.",
        "known_limitations": "Severe class imbalance (approx 4.8% stroke positive rate), typical of real-world stroke epidemiology."
    }
}

def write_all_metadata():
    for disease, meta in DATASET_METADATA.items():
        csv_path = os.path.join(RAW_DIR, disease, meta["file_name"])
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            meta["samples"] = int(len(df))
            meta["num_features"] = len(meta["features"])
            target_col = meta["target"]
            if target_col in df.columns:
                val_counts = df[target_col].value_counts().to_dict()
                meta["class_distribution"] = {str(k): int(v) for k, v in val_counts.items()}
            meta_path = os.path.join(RAW_DIR, disease, "metadata.json")
            with open(meta_path, "w") as f:
                json.dump(meta, f, indent=2)
            print(f"Recorded metadata for {disease}: {meta['samples']} samples, distribution={meta.get('class_distribution')}")

if __name__ == "__main__":
    write_all_metadata()
