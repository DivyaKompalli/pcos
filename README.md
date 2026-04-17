# AI-based PCOS & Anemia Early Risk Detector

**Research Prototype for Preventive Health Awareness**

## Abstract

Polycystic Ovary Syndrome (PCOS) and Anemia are among the most prevalent yet underdiagnosed health conditions affecting women in India, largely due to delayed symptom recognition, lack of awareness, and limited access to preventive healthcare. This project presents an AI-based early risk detection system designed to provide **non-diagnostic risk assessment** and health awareness support.

The system analyzes user-provided inputs such as lifestyle habits, menstrual irregularities, fatigue levels, dietary patterns, and basic lab values like hemoglobin range to estimate a personalized risk probability for PCOS and Anemia. **Machine learning models** including **Logistic Regression** and **XGBoost** are employed to identify patterns associated with elevated risk levels.

## Technology Stack

- **Backend:** Python
- **ML Models:** Logistic Regression, XGBoost (scikit-learn, XGBoost)
- **Interface:** Streamlit
- **Database:** SQLite

## Project Structure

```
pcos/
├── app.py              # Main Streamlit application
├── config.py           # Configuration and feature definitions
├── run.py              # Setup and launch script
├── requirements.txt
├── data/
│   ├── generate_data.py    # Synthetic training data generation
│   ├── pcos_training_data.csv
│   └── anemia_training_data.csv
├── models/
│   ├── train_models.py     # Model training (LR + XGBoost)
│   ├── predict.py          # Inference module
│   ├── pcos_logistic.joblib
│   ├── pcos_xgboost.joblib
│   ├── anemia_logistic.joblib
│   └── anemia_xgboost.joblib
└── database/
    └── db.py               # SQLite storage
```

## Installation

### Prerequisites

- Python 3.8 or higher

### Setup

```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

### Option 1: One-command run (recommended)

```bash
python run.py
```

This will automatically generate data, train models (on first run), and launch the Streamlit app at `http://localhost:8501`.

### Option 2: Manual setup

```bash
# 1. Generate training data
python -c "from data.generate_data import main; main()"

# 2. Train models
python -m models.train_models

# 3. Launch app
streamlit run app.py
```

## Features

### PCOS Risk Assessment
- Age, BMI
- Menstrual regularity and cycle length
- Irregular periods frequency
- Hirsutism, acne, hair loss
- Weight gain tendency
- Stress, exercise, diet, sleep

### Anemia Risk Assessment
- Age, hemoglobin level
- Fatigue level
- Vegetarian diet
- Iron-rich food consumption
- Menstrual blood loss
- Pregnancy history
- Diet quality, sleep, stress

### Output
- **Risk probability** (0–100%)
- **Risk level:** Low / Moderate / Elevated
- Recommendations for consultation
- Data stored in SQLite for research audit

## Disclaimer

**This tool is for research and health awareness only.** It provides a non-diagnostic risk estimate and does NOT constitute medical diagnosis. Users should always consult qualified healthcare providers for proper evaluation and treatment.

## Research Citation

If using this prototype in research, please cite the project and acknowledge the use of Logistic Regression and XGBoost for ensemble risk estimation tailored to Indian women's health parameters.

---

*Designed to encourage early medical consultation and improve health outcomes across rural and urban populations in India.*
