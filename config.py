"""Configuration settings for AI-based PCOS & Anemia Risk Detector."""

import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
DB_PATH = os.path.join(BASE_DIR, "pcos_anemia.db")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Feature columns for models
PCOS_FEATURES = [
    "age", "bmi", "menstrual_regularity", "cycle_length_days",
    "irregular_periods", "hirsutism", "acne", "hair_loss",
    "weight_gain", "stress_level", "exercise_frequency",
    "fast_food_frequency", "diet_quality", "sleep_hours"
]

ANEMIA_FEATURES = [
    "age", "hemoglobin", "fatigue_level", "vegetarian_diet",
    "iron_rich_food", "menstrual_blood_loss", "pregnancy_count",
    "diet_quality", "sleep_hours", "stress_level"
]
