# Research Methodology for AI-based PCOS & Anemia Early Risk Detector

## System Overview

This document describes the methodology and implementation details for the research prototype, suitable for inclusion in academic papers or technical reports.

## 1. Problem Statement

PCOS and Anemia are prevalent yet underdiagnosed conditions among Indian women due to:
- Delayed symptom recognition
- Lack of awareness
- Limited access to preventive healthcare
- Stigma around reproductive health discussions

## 2. Proposed Solution

A non-diagnostic AI-based risk assessment system that:
- Accepts user-provided lifestyle, menstrual, dietary, and basic lab inputs
- Outputs personalized risk probabilities for PCOS and Anemia
- Encourages early medical consultation
- Serves both rural and urban populations via web interface

## 3. Data

### 3.1 Synthetic Data Generation

Due to privacy and availability constraints, synthetic training data was generated using parameters from Indian population studies:

**PCOS Dataset (n=2500)**
- Prevalence: ~25% (aligned with literature range 3.7–22.5%)
- Features: Age, BMI, menstrual regularity, cycle length, irregular periods, hirsutism, acne, hair loss, weight gain, stress, exercise, fast food, diet quality, sleep
- Target: Binary (elevated risk / low risk)

**Anemia Dataset (n=2500)**
- Prevalence: ~52% (NFHS estimates for Indian women)
- Features: Age, hemoglobin, fatigue, vegetarian diet, iron-rich food intake, menstrual blood loss, pregnancy count, diet quality, sleep, stress
- Target: Binary (elevated risk / low risk)

### 3.2 Feature Selection Rationale

Features were selected based on:
- Rotterdam criteria (PCOS)
- WHO/Indian guidelines for anemia
- NFHS and Indian epidemiological studies
- Clinically actionable, self-reportable inputs

## 4. Machine Learning Models

### 4.1 Algorithms

1. **Logistic Regression** – Interpretable baseline, suitable for medical applications
2. **XGBoost** – Gradient boosting for non-linear pattern capture

### 4.2 Training

- Train/test split: 80/20, stratified
- Class weighting: Balanced for imbalanced targets
- Hyperparameters: Default scikit-learn/XGBoost with n_estimators=100, max_depth=5

### 4.3 Ensemble

Final risk probability = (P_LR + P_XGB) / 2

### 4.4 Model Performance (Synthetic Data)

| Condition | Model            | Accuracy | AUC-ROC |
|-----------|------------------|----------|---------|
| PCOS      | Logistic Reg     | ~87%     | ~0.91   |
| PCOS      | XGBoost          | ~86%     | ~0.90   |
| Anemia    | Logistic Reg     | ~85%     | ~0.94   |
| Anemia    | XGBoost          | ~87%     | ~0.93   |

*Note: Results on synthetic data; clinical validation required.*

## 5. Risk Stratification

- **Low:** Probability < 30%
- **Moderate:** 30% ≤ Probability < 60%
- **Elevated:** Probability ≥ 60%

## 6. Technology Implementation

- **Language:** Python 3.8+
- **ML Libraries:** scikit-learn, XGBoost
- **Interface:** Streamlit (web-based, no installation for end-users)
- **Storage:** SQLite (lightweight, portable)
- **Deployment:** Single-machine; suitable for research kiosks or local clinics

## 7. Limitations

- Synthetic training data; real-world validation needed
- Self-reported inputs subject to recall bias
- Non-diagnostic; does not replace clinical evaluation
- Hemoglobin input optional (default used if unknown)

## 8. Future Work

- Prospective validation with clinical datasets
- Multilingual support (Hindi, regional languages)
- Mobile/offline deployment for low-connectivity areas
- Integration with telemedicine platforms

---

*For technical implementation details, refer to the source code and README.*
