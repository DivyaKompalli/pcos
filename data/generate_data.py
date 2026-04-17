"""
Synthetic data generation for PCOS and Anemia risk detection models.
Generates research-grade training data based on clinical literature and Indian population parameters.
"""

import numpy as np
import pandas as pd
from pathlib import Path

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Indian population parameters
# PCOS prevalence: ~3.7-22.5% in reproductive-age women
# Anemia prevalence: ~50-57% in Indian women of reproductive age

def generate_pcos_data(n_samples: int = 2000) -> pd.DataFrame:
    """Generate synthetic PCOS risk assessment data."""
    n = n_samples
    
    # Age: 18-45 (reproductive age)
    age = np.random.randint(18, 46, n)
    
    # BMI: Higher BMI associated with PCOS risk (Indian: normal 18.5-24.9)
    # PCOS group tends to have higher BMI
    pcos_flag = np.random.binomial(1, 0.25, n)  # ~25% PCOS positive for training
    bmi = np.where(pcos_flag == 1, 
                   np.random.normal(26, 4, n).clip(18, 40),
                   np.random.normal(22, 3, n).clip(18, 35))
    
    # Menstrual regularity: 0=regular, 1=irregular (PCOS indicator)
    menstrual_regularity = np.where(pcos_flag == 1,
                                    np.random.choice([0, 1], n, p=[0.2, 0.8]),
                                    np.random.choice([0, 1], n, p=[0.85, 0.15]))
    
    # Cycle length: 21-35 normal, >35 or <21 irregular
    cycle_length = np.where(pcos_flag == 1,
                            np.random.normal(38, 10, n).clip(15, 60),
                            np.random.normal(28, 4, n).clip(21, 35))
    
    # Irregular periods count (0-4 scale)
    irregular_periods = np.where(pcos_flag == 1,
                                 np.random.choice([0, 1, 2, 3, 4], n, p=[0.1, 0.2, 0.3, 0.25, 0.15]),
                                 np.random.choice([0, 1, 2, 3, 4], n, p=[0.7, 0.2, 0.07, 0.02, 0.01]))
    
    # Hirsutism: 0-4 scale (PCOS indicator)
    hirsutism = np.where(pcos_flag == 1,
                         np.random.choice([0, 1, 2, 3, 4], n, p=[0.1, 0.25, 0.35, 0.2, 0.1]),
                         np.random.choice([0, 1, 2, 3, 4], n, p=[0.6, 0.3, 0.08, 0.015, 0.005]))
    
    # Acne: 0-4 scale
    acne = np.where(pcos_flag == 1,
                    np.random.choice([0, 1, 2, 3, 4], n, p=[0.15, 0.25, 0.35, 0.15, 0.1]),
                    np.random.choice([0, 1, 2, 3, 4], n, p=[0.5, 0.35, 0.12, 0.02, 0.01]))
    
    # Hair loss: 0-4 scale
    hair_loss = np.where(pcos_flag == 1,
                         np.random.choice([0, 1, 2, 3, 4], n, p=[0.2, 0.3, 0.3, 0.12, 0.08]),
                         np.random.choice([0, 1, 2, 3, 4], n, p=[0.6, 0.3, 0.08, 0.015, 0.005]))
    
    # Weight gain tendency: 0-4 scale
    weight_gain = np.where(pcos_flag == 1,
                           np.random.choice([0, 1, 2, 3, 4], n, p=[0.05, 0.15, 0.35, 0.3, 0.15]),
                           np.random.choice([0, 1, 2, 3, 4], n, p=[0.4, 0.35, 0.2, 0.04, 0.01]))
    
    # Stress: 0-4 scale
    stress_level = np.random.randint(0, 5, n)
    
    # Exercise: 0-4 scale (0=never, 4=daily)
    exercise_frequency = np.random.randint(0, 5, n)
    
    # Fast food: 0-4 scale
    fast_food_frequency = np.where(pcos_flag == 1,
                                   np.random.choice([0, 1, 2, 3, 4], n, p=[0.1, 0.2, 0.35, 0.25, 0.1]),
                                   np.random.choice([0, 1, 2, 3, 4], n, p=[0.25, 0.35, 0.25, 0.1, 0.05]))
    
    # Diet quality: 0-4 scale (0=poor, 4=excellent)
    diet_quality = np.random.randint(0, 5, n)
    
    # Sleep hours: 4-10
    sleep_hours = np.random.normal(6.5, 1.5, n).clip(4, 10)
    
    # Create target with some noise
    risk_score = (0.15 * (bmi - 20) + 0.2 * menstrual_regularity + 0.15 * irregular_periods + 
                  0.15 * hirsutism + 0.1 * acne + 0.1 * hair_loss + 0.1 * weight_gain +
                  0.05 * fast_food_frequency - 0.05 * exercise_frequency - 0.05 * diet_quality)
    risk_score = (risk_score - risk_score.min()) / (risk_score.max() - risk_score.min() + 1e-8)
    pcos_target = (risk_score + np.random.normal(0, 0.15, n) > 0.5).astype(int)
    
    df = pd.DataFrame({
        "age": age, "bmi": np.round(bmi, 1), "menstrual_regularity": menstrual_regularity,
        "cycle_length_days": cycle_length.astype(int), "irregular_periods": irregular_periods,
        "hirsutism": hirsutism, "acne": acne, "hair_loss": hair_loss, "weight_gain": weight_gain,
        "stress_level": stress_level, "exercise_frequency": exercise_frequency,
        "fast_food_frequency": fast_food_frequency, "diet_quality": diet_quality,
        "sleep_hours": np.round(sleep_hours, 1), "pcos_risk": pcos_target
    })
    
    return df


def generate_anemia_data(n_samples: int = 2000) -> pd.DataFrame:
    """Generate synthetic Anemia risk assessment data."""
    n = n_samples
    
    # Anemia prevalence ~52% in Indian women
    anemia_flag = np.random.binomial(1, 0.52, n)
    
    # Age: 18-49
    age = np.random.randint(18, 50, n)
    
    # Hemoglobin: Normal 12-16 g/dL, Anemia <12 (mild 10-12, moderate 8-10, severe <8)
    hemoglobin = np.where(anemia_flag == 1,
                          np.random.normal(10.5, 1.5, n).clip(6, 12),
                          np.random.normal(13, 1.2, n).clip(12, 16))
    
    # Fatigue: 0-4 scale
    fatigue_level = np.where(anemia_flag == 1,
                             np.random.choice([0, 1, 2, 3, 4], n, p=[0.02, 0.1, 0.3, 0.38, 0.2]),
                             np.random.choice([0, 1, 2, 3, 4], n, p=[0.4, 0.35, 0.2, 0.04, 0.01]))
    
    # Vegetarian diet: Higher anemia risk in vegetarians (common in India)
    vegetarian_diet = np.random.binomial(1, 0.65, n)  # ~65% vegetarian in India
    
    # Iron-rich food consumption: 0-4 scale
    iron_rich_food = np.where(anemia_flag == 1,
                              np.random.choice([0, 1, 2, 3, 4], n, p=[0.25, 0.35, 0.25, 0.1, 0.05]),
                              np.random.choice([0, 1, 2, 3, 4], n, p=[0.1, 0.2, 0.35, 0.25, 0.1]))
    
    # Menstrual blood loss: 0-4 (heavy periods = higher anemia risk)
    menstrual_blood_loss = np.where(anemia_flag == 1,
                                    np.random.choice([0, 1, 2, 3, 4], n, p=[0.15, 0.25, 0.3, 0.2, 0.1]),
                                    np.random.choice([0, 1, 2, 3, 4], n, p=[0.35, 0.35, 0.22, 0.06, 0.02]))
    
    # Pregnancy count
    pregnancy_count = np.random.poisson(1.5, n).clip(0, 6)
    
    # Diet quality
    diet_quality = np.random.randint(0, 5, n)
    
    # Sleep
    sleep_hours = np.random.normal(6.5, 1.5, n).clip(4, 10)
    
    # Stress
    stress_level = np.random.randint(0, 5, n)
    
    # Create target
    risk_score = (0.35 * (12 - hemoglobin).clip(0, 6) + 0.2 * fatigue_level + 
                  0.1 * vegetarian_diet + 0.15 * (4 - iron_rich_food) + 
                  0.1 * menstrual_blood_loss + 0.05 * pregnancy_count -
                  0.05 * diet_quality)
    risk_score = (risk_score - risk_score.min()) / (risk_score.max() - risk_score.min() + 1e-8)
    anemia_target = (risk_score + np.random.normal(0, 0.12, n) > 0.5).astype(int)
    
    df = pd.DataFrame({
        "age": age, "hemoglobin": np.round(hemoglobin, 1), "fatigue_level": fatigue_level,
        "vegetarian_diet": vegetarian_diet, "iron_rich_food": iron_rich_food,
        "menstrual_blood_loss": menstrual_blood_loss, "pregnancy_count": pregnancy_count,
        "diet_quality": diet_quality, "sleep_hours": np.round(sleep_hours, 1),
        "stress_level": stress_level, "anemia_risk": anemia_target
    })
    
    return df


def main():
    """Generate and save datasets."""
    data_dir = Path(__file__).parent
    
    pcos_df = generate_pcos_data(2500)
    anemia_df = generate_anemia_data(2500)
    
    pcos_df.to_csv(data_dir / "pcos_training_data.csv", index=False)
    anemia_df.to_csv(data_dir / "anemia_training_data.csv", index=False)
    
    print(f"Generated PCOS data: {len(pcos_df)} samples, {pcos_df['pcos_risk'].sum()} positive")
    print(f"Generated Anemia data: {len(anemia_df)} samples, {anemia_df['anemia_risk'].sum()} positive")


if __name__ == "__main__":
    main()
