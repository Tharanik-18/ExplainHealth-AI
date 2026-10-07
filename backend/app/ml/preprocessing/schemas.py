"""
Disease Feature Schemas and Clinical Metadata for ExplainHealth AI
Defines for each disease:
- Feature types (numerical, categorical)
- Actionability (actionable vs immutable for counterfactual analysis)
- Clinical valid bounds [min, max] (for OOD input reliability checks)
- Units and user-friendly labels in English and Tamil transliteration
- Target interpretation
"""

from typing import Dict, List, Any

DISEASE_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "diabetes": {
        "display_name": "Type 2 Diabetes Risk",
        "description": "Evaluates metabolic risk indicators based on the Pima Indians clinical study dataset.",
        "target_name": "outcome",
        "positive_label": "High Risk of Diabetes",
        "negative_label": "Lower Risk of Diabetes",
        "features": {
            "pregnancies": {
                "type": "numerical",
                "label": "Number of Pregnancies",
                "label_ta": "கர்ப்பங்களின் எண்ணிக்கை",
                "unit": "count",
                "min": 0,
                "max": 20,
                "actionable": False,
                "step": 1,
                "default": 0,
                "description": "Number of times pregnant"
            },
            "glucose": {
                "type": "numerical",
                "label": "Fasting / 2hr Blood Glucose",
                "label_ta": "ரத்த சர்க்கரை அளவு",
                "unit": "mg/dL",
                "min": 40,
                "max": 350,
                "zero_is_missing": True,
                "actionable": True,
                "step": 1,
                "default": 120,
                "description": "Plasma glucose concentration a 2 hours in an oral glucose tolerance test"
            },
            "blood_pressure": {
                "type": "numerical",
                "label": "Diastolic Blood Pressure",
                "label_ta": "ரத்த அழுத்தம் (Diastolic)",
                "unit": "mm Hg",
                "min": 30,
                "max": 180,
                "zero_is_missing": True,
                "actionable": True,
                "step": 1,
                "default": 72,
                "description": "Diastolic blood pressure"
            },
            "skin_thickness": {
                "type": "numerical",
                "label": "Triceps Skinfold Thickness",
                "label_ta": "தோல் மடிப்பு தடிமன்",
                "unit": "mm",
                "min": 5,
                "max": 99,
                "zero_is_missing": True,
                "actionable": True,
                "step": 1,
                "default": 23,
                "description": "Triceps skin fold thickness measuring body fat"
            },
            "insulin": {
                "type": "numerical",
                "label": "Serum Insulin",
                "label_ta": "சீரம் இன்சுலின் அளவு",
                "unit": "mu U/ml",
                "min": 10,
                "max": 850,
                "zero_is_missing": True,
                "actionable": True,
                "step": 1,
                "default": 100,
                "description": "2-Hour serum insulin"
            },
            "bmi": {
                "type": "numerical",
                "label": "Body Mass Index (BMI)",
                "label_ta": "உடல் நிறை குறியீட்டெண் (BMI)",
                "unit": "kg/m²",
                "min": 12.0,
                "max": 65.0,
                "zero_is_missing": True,
                "actionable": True,
                "step": 0.1,
                "default": 27.5,
                "description": "Weight in kg / (height in meters)^2"
            },
            "diabetes_pedigree_function": {
                "type": "numerical",
                "label": "Diabetes Pedigree Score",
                "label_ta": "குடும்ப மரபணு வரலாறு ஸ்கோர்",
                "unit": "score",
                "min": 0.05,
                "max": 2.5,
                "actionable": False,
                "step": 0.01,
                "default": 0.47,
                "description": "Genetic scoring function based on family history"
            },
            "age": {
                "type": "numerical",
                "label": "Age",
                "label_ta": "வயது",
                "unit": "years",
                "min": 18,
                "max": 100,
                "actionable": False,
                "step": 1,
                "default": 45,
                "description": "Age in completed years"
            }
        },
        "required_features": ["glucose", "bmi", "age", "blood_pressure"]
    },

    "heart_disease": {
        "display_name": "Coronary Heart Disease Risk",
        "description": "Evaluates cardiovascular risk indicators based on the UCI Cleveland Clinic study.",
        "target_name": "target",
        "positive_label": "Elevated Heart Disease Indicator",
        "negative_label": "Lower Heart Disease Indicator",
        "features": {
            "age": {
                "type": "numerical",
                "label": "Age",
                "label_ta": "வயது",
                "unit": "years",
                "min": 20,
                "max": 95,
                "actionable": False,
                "step": 1,
                "default": 55,
                "description": "Age in years"
            },
            "sex": {
                "type": "categorical",
                "label": "Biological Sex",
                "label_ta": "பாலினம்",
                "options": [
                    {"value": 1, "label": "Male (ஆண்)"},
                    {"value": 0, "label": "Female (பெண்)"}
                ],
                "actionable": False,
                "default": 1,
                "description": "Biological sex (1 = male; 0 = female)"
            },
            "cp": {
                "type": "categorical",
                "label": "Chest Pain Type",
                "label_ta": "மார்பு வலி வகை",
                "options": [
                    {"value": 0, "label": "Typical Angina (வழக்கமான நெஞ்சு வலி)"},
                    {"value": 1, "label": "Atypical Angina (அசாதாரண நெஞ்சு வலி)"},
                    {"value": 2, "label": "Non-anginal Pain (இதயம் சாரா வலி)"},
                    {"value": 3, "label": "Asymptomatic (அறிகுறியற்ற)"}
                ],
                "actionable": False,
                "default": 0,
                "description": "Chest pain type experienced"
            },
            "trestbps": {
                "type": "numerical",
                "label": "Resting Blood Pressure",
                "label_ta": "ஓய்வு நேர ரத்த அழுத்தம்",
                "unit": "mm Hg",
                "min": 80,
                "max": 220,
                "actionable": True,
                "step": 1,
                "default": 130,
                "description": "Resting systolic blood pressure upon clinical admission"
            },
            "chol": {
                "type": "numerical",
                "label": "Serum Cholesterol",
                "label_ta": "கொலஸ்ட்ரால் அளவு",
                "unit": "mg/dL",
                "min": 100,
                "max": 600,
                "actionable": True,
                "step": 1,
                "default": 240,
                "description": "Serum cholesterol in mg/dL"
            },
            "fbs": {
                "type": "categorical",
                "label": "Fasting Blood Sugar > 120 mg/dL",
                "label_ta": "உணவுக்கு முன் ரத்த சர்க்கரை > 120",
                "options": [
                    {"value": 0, "label": "No (இல்லை - normal)"},
                    {"value": 1, "label": "Yes (ஆம் - elevated)"}
                ],
                "actionable": True,
                "default": 0,
                "description": "Fasting blood sugar > 120 mg/dl"
            },
            "restecg": {
                "type": "categorical",
                "label": "Resting ECG Results",
                "label_ta": "ஓய்வு நேர ECG முடிவு",
                "options": [
                    {"value": 0, "label": "Normal (இயல்பு)"},
                    {"value": 1, "label": "ST-T Wave Abnormality (அலை மாறுபாடு)"},
                    {"value": 2, "label": "Left Ventricular Hypertrophy (தசை தடிமன்)"}
                ],
                "actionable": False,
                "default": 0,
                "description": "Resting electrocardiographic results"
            },
            "thalach": {
                "type": "numerical",
                "label": "Maximum Heart Rate Achieved",
                "label_ta": "அதிகபட்ச இதய துடிப்பு",
                "unit": "bpm",
                "min": 60,
                "max": 220,
                "actionable": True,
                "step": 1,
                "default": 150,
                "description": "Maximum heart rate achieved during exercise stress"
            },
            "exang": {
                "type": "categorical",
                "label": "Exercise Induced Angina",
                "label_ta": "உடற்பயிற்சியினால் ஏற்படும் நெஞ்சு வலி",
                "options": [
                    {"value": 0, "label": "No (இல்லை)"},
                    {"value": 1, "label": "Yes (ஆம்)"}
                ],
                "actionable": False,
                "default": 0,
                "description": "Exercise induced chest pain"
            },
            "oldpeak": {
                "type": "numerical",
                "label": "ST Depression (Oldpeak)",
                "label_ta": "ST மனச்சோர்வு அளவு",
                "unit": "depression",
                "min": 0.0,
                "max": 6.5,
                "actionable": True,
                "step": 0.1,
                "default": 1.0,
                "description": "ST depression induced by exercise relative to rest"
            },
            "slope": {
                "type": "categorical",
                "label": "Peak Exercise ST Segment Slope",
                "label_ta": "ST சரிவு வகை",
                "options": [
                    {"value": 0, "label": "Upsloping (மேல்நோக்கிய)"},
                    {"value": 1, "label": "Flat (சமமான)"},
                    {"value": 2, "label": "Downsloping (கீழ்நோக்கிய)"}
                ],
                "actionable": False,
                "default": 1,
                "description": "The slope of the peak exercise ST segment"
            },
            "ca": {
                "type": "categorical",
                "label": "Major Vessels Colored by Fluoroscopy",
                "label_ta": "ஃப்ளோரோஸ்கோபி நாளங்கள் எண்ணிக்கை",
                "options": [
                    {"value": 0, "label": "0 vessels"},
                    {"value": 1, "label": "1 vessel"},
                    {"value": 2, "label": "2 vessels"},
                    {"value": 3, "label": "3 vessels"}
                ],
                "actionable": False,
                "default": 0,
                "description": "Number of major vessels (0-3) colored by fluoroscopy"
            },
            "thal": {
                "type": "categorical",
                "label": "Thalassemia Blood Factor",
                "label_ta": "தலசீமியா காரணி",
                "options": [
                    {"value": 1, "label": "Normal (இயல்பு)"},
                    {"value": 2, "label": "Fixed Defect (நிலையான குறைபாடு)"},
                    {"value": 3, "label": "Reversible Defect (மாறக்கூடிய குறைபாடு)"}
                ],
                "actionable": False,
                "default": 2,
                "description": "Thalassemia blood disorder status"
            }
        },
        "required_features": ["age", "sex", "cp", "trestbps", "chol", "thalach"]
    },

    "breast_cancer": {
        "display_name": "Breast Mass Malignancy Risk",
        "description": "Evaluates cytology cell nuclei morphological features from FNA biopsy image analysis (UCI WDBC).",
        "target_name": "target",
        "positive_label": "Malignant Contour Characteristics",
        "negative_label": "Benign Contour Characteristics",
        "features": {
            "mean_radius": {
                "type": "numerical",
                "label": "Mean Cell Radius",
                "label_ta": "செல் சராசரி ஆரம்",
                "unit": "μm",
                "min": 6.0,
                "max": 30.0,
                "actionable": False,
                "step": 0.1,
                "default": 14.1,
                "description": "Mean of distances from center to points on the perimeter"
            },
            "mean_texture": {
                "type": "numerical",
                "label": "Mean Texture",
                "label_ta": "செல் அமைப்பு (Texture)",
                "unit": "grayscale",
                "min": 9.0,
                "max": 40.0,
                "actionable": False,
                "step": 0.1,
                "default": 19.3,
                "description": "Standard deviation of gray-scale values"
            },
            "mean_perimeter": {
                "type": "numerical",
                "label": "Mean Perimeter",
                "label_ta": "செல் சுற்றளவு",
                "unit": "μm",
                "min": 40.0,
                "max": 190.0,
                "actionable": False,
                "step": 0.1,
                "default": 92.0,
                "description": "Mean size of the core tumor perimeter"
            },
            "mean_area": {
                "type": "numerical",
                "label": "Mean Area",
                "label_ta": "செல் பரப்பளவு",
                "unit": "μm²",
                "min": 140.0,
                "max": 2600.0,
                "actionable": False,
                "step": 1.0,
                "default": 654.0,
                "description": "Mean size of the core tumor area"
            },
            "mean_smoothness": {
                "type": "numerical",
                "label": "Mean Smoothness",
                "label_ta": "செல் மேற்பரப்பு வழுவழுப்பு",
                "unit": "ratio",
                "min": 0.05,
                "max": 0.20,
                "actionable": False,
                "step": 0.001,
                "default": 0.096,
                "description": "Mean of local variation in radius lengths"
            },
            "mean_compactness": {
                "type": "numerical",
                "label": "Mean Compactness",
                "label_ta": "செல் அடர்த்தி",
                "unit": "ratio",
                "min": 0.01,
                "max": 0.35,
                "actionable": False,
                "step": 0.001,
                "default": 0.104,
                "description": "Perimeter^2 / area - 1.0"
            },
            "mean_concavity": {
                "type": "numerical",
                "label": "Mean Concavity",
                "label_ta": "குழிவான விளிம்பு அளவு",
                "unit": "ratio",
                "min": 0.0,
                "max": 0.45,
                "actionable": False,
                "step": 0.001,
                "default": 0.088,
                "description": "Severity of concave portions of the contour"
            },
            "mean_concave_points": {
                "type": "numerical",
                "label": "Mean Concave Points",
                "label_ta": "குழிவான புள்ளிகள்",
                "unit": "ratio",
                "min": 0.0,
                "max": 0.25,
                "actionable": False,
                "step": 0.001,
                "default": 0.048,
                "description": "Number of concave portions of the contour"
            },
            "mean_symmetry": {
                "type": "numerical",
                "label": "Mean Symmetry",
                "label_ta": "சமச்சீர்மை",
                "unit": "ratio",
                "min": 0.10,
                "max": 0.35,
                "actionable": False,
                "step": 0.001,
                "default": 0.181,
                "description": "Nuclear contour symmetry"
            },
            "mean_fractal_dimension": {
                "type": "numerical",
                "label": "Mean Fractal Dimension",
                "label_ta": "ஃபிராக்டல் பரிமாணம்",
                "unit": "ratio",
                "min": 0.04,
                "max": 0.10,
                "actionable": False,
                "step": 0.001,
                "default": 0.062,
                "description": "Coastline approximation - 1"
            }
        },
        "required_features": ["mean_radius", "mean_texture", "mean_perimeter", "mean_area", "mean_concavity"]
    },

    "lung_cancer": {
        "display_name": "Lung Cancer Symptom Risk Profile",
        "description": "Evaluates pulmonary symptom presentation and tobacco exposure patterns.",
        "target_name": "lung_cancer",
        "positive_label": "High Pulmonary Cancer Risk Indicator",
        "negative_label": "Lower Pulmonary Cancer Risk Indicator",
        "features": {
            "gender": {
                "type": "categorical",
                "label": "Biological Sex",
                "label_ta": "பாலினம்",
                "options": [
                    {"value": "M", "label": "Male (ஆண்)"},
                    {"value": "F", "label": "Female (பெண்)"}
                ],
                "actionable": False,
                "default": "M",
                "description": "Biological sex"
            },
            "age": {
                "type": "numerical",
                "label": "Age",
                "label_ta": "வயது",
                "unit": "years",
                "min": 20,
                "max": 95,
                "actionable": False,
                "step": 1,
                "default": 62,
                "description": "Age in years"
            },
            "smoking": {
                "type": "categorical",
                "label": "Smoking Habit",
                "label_ta": "புகைபிடிக்கும் பழக்கம்",
                "options": [
                    {"value": 1, "label": "Non-smoker / No (இல்லை)"},
                    {"value": 2, "label": "Smoker / Yes (ஆம்)"}
                ],
                "actionable": True,
                "default": 2,
                "description": "Tobacco smoking history"
            },
            "yellow_fingers": {
                "type": "categorical",
                "label": "Yellow Nicotine-Stained Fingers",
                "label_ta": "விரல்களில் மஞ்சள் கறை",
                "options": [{"value": 1, "label": "No (இல்லை)"}, {"value": 2, "label": "Yes (ஆம்)"}],
                "actionable": True,
                "default": 1
            },
            "anxiety": {
                "type": "categorical",
                "label": "Persistent Anxiety",
                "label_ta": "பதட்டம் / மனக்கவலை",
                "options": [{"value": 1, "label": "No (இல்லை)"}, {"value": 2, "label": "Yes (ஆம்)"}],
                "actionable": True,
                "default": 1
            },
            "peer_pressure": {
                "type": "categorical",
                "label": "Second-hand / Peer Smoke Exposure",
                "label_ta": "புகை வெளிப்பாடு / சக புகைபிடித்தல்",
                "options": [{"value": 1, "label": "No (இல்லை)"}, {"value": 2, "label": "Yes (ஆம்)"}],
                "actionable": True,
                "default": 1
            },
            "chronic_disease": {
                "type": "categorical",
                "label": "Chronic Respiratory Disease",
                "label_ta": "நாள்பட்ட நுரையீரல் நோய்",
                "options": [{"value": 1, "label": "No (இல்லை)"}, {"value": 2, "label": "Yes (ஆம்)"}],
                "actionable": False,
                "default": 1
            },
            "fatigue": {
                "type": "categorical",
                "label": "Unexplained Chronic Fatigue",
                "label_ta": "தீராத உடல் சோர்வு",
                "options": [{"value": 1, "label": "No (இல்லை)"}, {"value": 2, "label": "Yes (ஆம்)"}],
                "actionable": True,
                "default": 2
            },
            "allergy": {
                "type": "categorical",
                "label": "Respiratory Allergies",
                "label_ta": "சுவாச ஒவ்வாமை",
                "options": [{"value": 1, "label": "No (இல்லை)"}, {"value": 2, "label": "Yes (ஆம்)"}],
                "actionable": False,
                "default": 1
            },
            "wheezing": {
                "type": "categorical",
                "label": "Wheezing Breath Sounds",
                "label_ta": "மூச்சிரைப்பு சத்தம்",
                "options": [{"value": 1, "label": "No (இல்லை)"}, {"value": 2, "label": "Yes (ஆம்)"}],
                "actionable": True,
                "default": 2
            },
            "alcohol_consuming": {
                "type": "categorical",
                "label": "Alcohol Consumption",
                "label_ta": "மது அருந்தும் பழக்கம்",
                "options": [{"value": 1, "label": "No (இல்லை)"}, {"value": 2, "label": "Yes (ஆம்)"}],
                "actionable": True,
                "default": 1
            },
            "coughing": {
                "type": "categorical",
                "label": "Persistent Cough",
                "label_ta": "தொடர் இருமல்",
                "options": [{"value": 1, "label": "No (இல்லை)"}, {"value": 2, "label": "Yes (ஆம்)"}],
                "actionable": True,
                "default": 2
            },
            "shortness_of_breath": {
                "type": "categorical",
                "label": "Shortness of Breath (Dyspnea)",
                "label_ta": "மூச்சுத் திணறல்",
                "options": [{"value": 1, "label": "No (இல்லை)"}, {"value": 2, "label": "Yes (ஆம்)"}],
                "actionable": True,
                "default": 2
            },
            "swallowing_difficulty": {
                "type": "categorical",
                "label": "Difficulty Swallowing (Dysphagia)",
                "label_ta": "விழுங்குவதில் சிரமம்",
                "options": [{"value": 1, "label": "No (இல்லை)"}, {"value": 2, "label": "Yes (ஆம்)"}],
                "actionable": False,
                "default": 1
            },
            "chest_pain": {
                "type": "categorical",
                "label": "Chest Pain",
                "label_ta": "மார்பு வலி",
                "options": [{"value": 1, "label": "No (இல்லை)"}, {"value": 2, "label": "Yes (ஆம்)"}],
                "actionable": True,
                "default": 2
            }
        },
        "required_features": ["age", "smoking", "coughing", "shortness_of_breath", "chest_pain"]
    },

    "stroke": {
        "display_name": "Cerebrovascular Stroke Risk",
        "description": "Evaluates cerebrovascular accident likelihood based on clinical, lifestyle, and vascular risk factors.",
        "target_name": "stroke",
        "positive_label": "High Stroke Risk Indicator",
        "negative_label": "Lower Stroke Risk Indicator",
        "features": {
            "gender": {
                "type": "categorical",
                "label": "Gender",
                "label_ta": "பாலினம்",
                "options": [
                    {"value": "Male", "label": "Male (ஆண்)"},
                    {"value": "Female", "label": "Female (பெண்)"}
                ],
                "actionable": False,
                "default": "Male"
            },
            "age": {
                "type": "numerical",
                "label": "Age",
                "label_ta": "வயது",
                "unit": "years",
                "min": 18,
                "max": 100,
                "actionable": False,
                "step": 1,
                "default": 65
            },
            "hypertension": {
                "type": "categorical",
                "label": "Chronic Hypertension",
                "label_ta": "உயர் ரத்த அழுத்தம் (BP)",
                "options": [
                    {"value": 0, "label": "No (இல்லை)"},
                    {"value": 1, "label": "Yes (ஆம்)"}
                ],
                "actionable": True,
                "default": 1
            },
            "heart_disease": {
                "type": "categorical",
                "label": "Pre-existing Heart Disease",
                "label_ta": "இதய நோய் வரலாறு",
                "options": [
                    {"value": 0, "label": "No (இல்லை)"},
                    {"value": 1, "label": "Yes (ஆம்)"}
                ],
                "actionable": False,
                "default": 0
            },
            "ever_married": {
                "type": "categorical",
                "label": "Ever Married",
                "label_ta": "திருமணமானவரா",
                "options": [
                    {"value": "No", "label": "No (இல்லை)"},
                    {"value": "Yes", "label": "Yes (ஆம்)"}
                ],
                "actionable": False,
                "default": "Yes"
            },
            "work_type": {
                "type": "categorical",
                "label": "Work Nature",
                "label_ta": "பணி வகை",
                "options": [
                    {"value": "Private", "label": "Private Company"},
                    {"value": "Self-employed", "label": "Self-employed"},
                    {"value": "Govt_job", "label": "Government Job"},
                    {"value": "children", "label": "Student / Child"},
                    {"value": "Never_worked", "label": "Never Worked"}
                ],
                "actionable": False,
                "default": "Private"
            },
            "residence_type": {
                "type": "categorical",
                "label": "Residence Setting",
                "label_ta": "வசிப்பிடம்",
                "options": [
                    {"value": "Urban", "label": "Urban (நகர்ப்புறம்)"},
                    {"value": "Rural", "label": "Rural (கிராமப்புறம்)"}
                ],
                "actionable": False,
                "default": "Urban"
            },
            "avg_glucose_level": {
                "type": "numerical",
                "label": "Average Blood Glucose",
                "label_ta": "சராசரி ரத்த சர்க்கரை அளவு",
                "unit": "mg/dL",
                "min": 50.0,
                "max": 320.0,
                "actionable": True,
                "step": 0.5,
                "default": 150.0
            },
            "bmi": {
                "type": "numerical",
                "label": "Body Mass Index (BMI)",
                "label_ta": "உடல் நிறை குறியீட்டெண் (BMI)",
                "unit": "kg/m²",
                "min": 12.0,
                "max": 65.0,
                "actionable": True,
                "step": 0.1,
                "default": 30.5
            },
            "smoking_status": {
                "type": "categorical",
                "label": "Smoking Status",
                "label_ta": "புகைபிடித்தல் நிலை",
                "options": [
                    {"value": "never smoked", "label": "Never Smoked (புகை பிடிக்காதவர்)"},
                    {"value": "formerly smoked", "label": "Formerly Smoked (முன்னாள் புகைபிடித்தவர்)"},
                    {"value": "smokes", "label": "Currently Smokes (தற்போது புகைபிடிப்பவர்)"},
                    {"value": "Unknown", "label": "Unknown / Not Disclosed"}
                ],
                "actionable": True,
                "default": "formerly smoked"
            }
        },
        "required_features": ["age", "hypertension", "avg_glucose_level", "bmi", "smoking_status"]
    }
}
