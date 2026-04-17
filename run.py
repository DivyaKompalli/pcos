"""
Setup and run script for AI-based PCOS & Anemia Risk Detector.
Generates data, trains models (if needed), and launches the Streamlit app.
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent


def main():
    # Check if models exist
    models_dir = PROJECT_ROOT / "models"
    data_dir = PROJECT_ROOT / "data"
    
    required_models = ["pcos_logistic.joblib", "pcos_xgboost.joblib", "anemia_logistic.joblib", "anemia_xgboost.joblib"]
    models_exist = all((models_dir / m).exists() for m in required_models)
    
    if not models_exist:
        print("First-time setup: Generating data and training ML models...")
        sys.path.insert(0, str(PROJECT_ROOT))
        
        from data.generate_data import main as gen_main
        gen_main()
        
        from models.train_models import train_pcos_models, train_anemia_models
        train_pcos_models()
        train_anemia_models()
        
        print("Setup complete!")
    
    print("Launching Streamlit app...")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        str(PROJECT_ROOT / "app.py"),
        "--server.headless", "true",
        "--server.port", "8501"
    ])


if __name__ == "__main__":
    main()
