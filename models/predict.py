"""
Inference module for PCOS and Anemia risk prediction.
Provides ensemble predictions using Logistic Regression and XGBoost.
"""

import numpy as np
import pandas as pd
from pathlib import Path
import joblib

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import PCOS_FEATURES, ANEMIA_FEATURES, MODELS_DIR


def load_models(condition: str):
    """Load trained models for PCOS or Anemia."""
    models_dir = Path(MODELS_DIR)
    
    if condition == "pcos":
        lr = joblib.load(models_dir / "pcos_logistic.joblib")
        xgb_model = joblib.load(models_dir / "pcos_xgboost.joblib")
        features = PCOS_FEATURES
    else:  # anemia
        lr = joblib.load(models_dir / "anemia_logistic.joblib")
        xgb_model = joblib.load(models_dir / "anemia_xgboost.joblib")
        features = ANEMIA_FEATURES
    
    return lr, xgb_model, features


def predict_pcos(user_input: dict):
    """
    Predict PCOS risk probability.
    Returns (probability 0-1, risk level string)
    """
    lr, xgb_model, features = load_models("pcos")
    
    X = pd.DataFrame([{f: user_input.get(f, 0) for f in features}])
    X = X[features]  # Ensure column order
    
    lr_proba = lr.predict_proba(X)[0, 1]
    xgb_proba = xgb_model.predict_proba(X)[0, 1]
    
    # Ensemble: average of both models
    proba = (lr_proba + xgb_proba) / 2
    
    if proba < 0.3:
        level = "Low"
    elif proba < 0.6:
        level = "Moderate"
    else:
        level = "Elevated"
    
    return float(proba), level


def predict_anemia(user_input: dict):
    """
    Predict Anemia risk probability.
    Returns (probability 0-1, risk level string)
    """
    lr, xgb_model, features = load_models("anemia")
    
    X = pd.DataFrame([{f: user_input.get(f, 0) for f in features}])
    X = X[features]
    
    lr_proba = lr.predict_proba(X)[0, 1]
    xgb_proba = xgb_model.predict_proba(X)[0, 1]
    
    proba = (lr_proba + xgb_proba) / 2
    
    if proba < 0.3:
        level = "Low"
    elif proba < 0.6:
        level = "Moderate"
    else:
        level = "Elevated"
    
    return float(proba), level


def get_shap_explanation(condition: str, user_input: dict):
    """
    Generate SHAP explanation for the XGBoost model.
    Returns (explainer, shap_values, X)
    """
    import shap
    _, xgb_model, features = load_models(condition)
    
    X = pd.DataFrame([{f: user_input.get(f, 0) for f in features}])
    X = X[features]
    
    explainer = shap.TreeExplainer(xgb_model)
    shap_values = explainer(X)
    
    return explainer, shap_values, X
