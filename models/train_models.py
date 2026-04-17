"""
ML Model Training for PCOS and Anemia Risk Detection.
Uses Logistic Regression and XGBoost as specified in the research abstract.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, confusion_matrix
import xgboost as xgb
import joblib

# Add parent to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import PCOS_FEATURES, ANEMIA_FEATURES, MODELS_DIR, DATA_DIR


def train_pcos_models():
    """Train PCOS risk detection models."""
    df = pd.read_csv(Path(DATA_DIR) / "pcos_training_data.csv")
    
    X = df[PCOS_FEATURES]
    y = df["pcos_risk"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Logistic Regression
    lr_model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
    lr_model.fit(X_train, y_train)
    
    lr_pred = lr_model.predict(X_test)
    lr_proba = lr_model.predict_proba(X_test)[:, 1]
    
    print("=== PCOS - Logistic Regression ===")
    print(f"Accuracy: {accuracy_score(y_test, lr_pred):.4f}")
    print(f"AUC-ROC: {roc_auc_score(y_test, lr_proba):.4f}")
    print(classification_report(y_test, lr_pred, target_names=['Low Risk', 'Elevated Risk']))
    print(confusion_matrix(y_test, lr_pred))
    
    # XGBoost
    xgb_model = xgb.XGBClassifier(
        n_estimators=100, max_depth=5, learning_rate=0.1,
        random_state=42, use_label_encoder=False, eval_metric='logloss'
    )
    xgb_model.fit(X_train, y_train)
    
    xgb_pred = xgb_model.predict(X_test)
    xgb_proba = xgb_model.predict_proba(X_test)[:, 1]
    
    print("\n=== PCOS - XGBoost ===")
    print(f"Accuracy: {accuracy_score(y_test, xgb_pred):.4f}")
    print(f"AUC-ROC: {roc_auc_score(y_test, xgb_proba):.4f}")
    print(classification_report(y_test, xgb_pred, target_names=['Low Risk', 'Elevated Risk']))
    print(confusion_matrix(y_test, xgb_pred))
    
    # Save models
    joblib.dump(lr_model, Path(MODELS_DIR) / "pcos_logistic.joblib")
    joblib.dump(xgb_model, Path(MODELS_DIR) / "pcos_xgboost.joblib")
    
    return lr_model, xgb_model


def train_anemia_models():
    """Train Anemia risk detection models."""
    df = pd.read_csv(Path(DATA_DIR) / "anemia_training_data.csv")
    
    X = df[ANEMIA_FEATURES]
    y = df["anemia_risk"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Logistic Regression
    lr_model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
    lr_model.fit(X_train, y_train)
    
    lr_pred = lr_model.predict(X_test)
    lr_proba = lr_model.predict_proba(X_test)[:, 1]
    
    print("\n=== Anemia - Logistic Regression ===")
    print(f"Accuracy: {accuracy_score(y_test, lr_pred):.4f}")
    print(f"AUC-ROC: {roc_auc_score(y_test, lr_proba):.4f}")
    print(classification_report(y_test, lr_pred, target_names=['Low Risk', 'Elevated Risk']))
    print(confusion_matrix(y_test, lr_pred))
    
    # XGBoost
    xgb_model = xgb.XGBClassifier(
        n_estimators=100, max_depth=5, learning_rate=0.1,
        random_state=42, use_label_encoder=False, eval_metric='logloss'
    )
    xgb_model.fit(X_train, y_train)
    
    xgb_pred = xgb_model.predict(X_test)
    xgb_proba = xgb_model.predict_proba(X_test)[:, 1]
    
    print("\n=== Anemia - XGBoost ===")
    print(f"Accuracy: {accuracy_score(y_test, xgb_pred):.4f}")
    print(f"AUC-ROC: {roc_auc_score(y_test, xgb_proba):.4f}")
    print(classification_report(y_test, xgb_pred, target_names=['Low Risk', 'Elevated Risk']))
    print(confusion_matrix(y_test, xgb_pred))
    
    # Save models
    joblib.dump(lr_model, Path(MODELS_DIR) / "anemia_logistic.joblib")
    joblib.dump(xgb_model, Path(MODELS_DIR) / "anemia_xgboost.joblib")
    
    return lr_model, xgb_model


if __name__ == "__main__":
    print("Generating data...")
    from data.generate_data import main as generate_main
    generate_main()
    
    print("\nTraining PCOS models...")
    train_pcos_models()
    
    print("\nTraining Anemia models...")
    train_anemia_models()
    
    print("\n[OK] All models trained and saved successfully!")
