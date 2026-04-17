import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import json
import numpy as np

# Import existing backend logic
from database.db import init_db, save_assessment, get_assessment_stats, get_all_assessments
from models.predict import predict_pcos, predict_anemia, get_shap_explanation
from utils.pdf_generator import generate_report

app = FastAPI(title="PCOS & Anemia Risk API")

# Setup CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

# Pydantic Schemas for validation
class PcosInput(BaseModel):
    age: int
    bmi: float
    menstrual_regularity: int
    cycle_length_days: int
    irregular_periods: int
    hirsutism: int
    acne: int
    hair_loss: int
    weight_gain: int
    stress_level: int
    exercise_frequency: int
    fast_food_frequency: int
    diet_quality: int
    sleep_hours: float

class AnemiaInput(BaseModel):
    age: int
    hemoglobin: float
    fatigue_level: int
    vegetarian_diet: int
    iron_rich_food: int
    menstrual_blood_loss: int
    pregnancy_count: int
    diet_quality: int
    sleep_hours: float
    stress_level: int

class ChatInput(BaseModel):
    message: str
    history: List[Dict[str, str]] = []

def get_gemini_api_key():
    import os
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        return env_key
        
    try:
        with open(".streamlit/secrets.toml", "r") as f:
            for line in f:
                if "GEMINI_API_KEY" in line:
                    return line.split("=")[1].strip().strip('"').strip("'")
        return ""
    except Exception:
        return ""

@app.post("/api/chat")
async def api_chat(data: ChatInput):
    import google.generativeai as genai
    api_key = get_gemini_api_key()
    if not api_key or api_key == "paste_your_api_key_here":
        raise HTTPException(status_code=400, detail="Gemini API Key missing")
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Convert history format
        formatted_history = []
        for msg in data.history:
            formatted_history.append({"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]})
            
        chat_session = model.start_chat(history=formatted_history)
        
        # Send system prompt if history is empty
        if not data.history:
            chat_session.send_message(
                "You are a helpful, empathetic, and knowledgeable health educator focusing on Indian women's health, specifically PCOS and Anemia. "
                "You must clarify that you are an AI prototype and NEVER provide clinical diagnoses. "
                "Give practical, evidence-based lifestyle and dietary advice. Keep answers under 3 paragraphs."
            )
            
        response = chat_session.send_message(data.message)
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def parse_shap_values(shap_values):
    """Convert SHAP objects into serializable dicts for React recharts"""
    try:
        # shap_values[0] is typically an Explanation object for one instance
        exp = shap_values[0]
        
        # Safely extract arrays, handling potential lists or numpy arrays
        values = exp.values.tolist() if hasattr(exp.values, "tolist") else list(exp.values)
        data = exp.data.tolist() if hasattr(exp.data, "tolist") else list(exp.data)
        feature_names = exp.feature_names if hasattr(exp, "feature_names") else [f"Feature {i}" for i in range(len(values))]
        base_value = float(exp.base_values) if hasattr(exp, "base_values") else 0.0
        
        features = []
        for i in range(len(values)):
            features.append({
                "name": feature_names[i],
                "value": float(values[i]),
                "data": float(data[i]) if str(data[i]) not in ['nan', 'NaN'] else 0.0
            })
            
        # Sort by absolute SHAP value for better visualization
        features.sort(key=lambda x: abs(x["value"]), reverse=True)
        return {"base_value": base_value, "features": features}
    except Exception as e:
        print(f"SHAP Parsing error: {e}")
        return {"base_value": 0, "features": []}

@app.post("/api/predict/pcos")
async def api_predict_pcos(data: PcosInput):
    inputs = data.model_dump()
    try:
        proba, level = predict_pcos(inputs)
        save_assessment("pcos", inputs, proba, level)
        
        # Explainable AI
        explainer, shap_values, X = get_shap_explanation("pcos", inputs)
        shap_data = parse_shap_values(shap_values)
        
        return {
            "probability": proba,
            "level": level,
            "shap_data": shap_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/predict/anemia")
async def api_predict_anemia(data: AnemiaInput):
    inputs = data.model_dump()
    try:
        proba, level = predict_anemia(inputs)
        save_assessment("anemia", inputs, proba, level)
        
        # Explainable AI
        explainer, shap_values, X = get_shap_explanation("anemia", inputs)
        shap_data = parse_shap_values(shap_values)
        
        return {
            "probability": proba,
            "level": level,
            "shap_data": shap_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/stats")
async def api_admin_stats():
    stats = get_assessment_stats()
    all_assessments = get_all_assessments()
    
    # Aggregating distribution
    risk_distribution = {"Low": 0, "Moderate": 0, "Elevated": 0}
    condition_distribution = {"pcos": 0, "anemia": 0}
    
    for a in all_assessments:
        r_level = a.get("risk_level", "Unknown")
        c_type = a.get("condition_type", "Unknown")
        if r_level in risk_distribution:
            risk_distribution[r_level] += 1
        if c_type in condition_distribution:
            condition_distribution[c_type] += 1
            
    return {
        "summary": stats,
        "total_assessments": len(all_assessments),
        "risk_distribution": [{"name": k, "value": v} for k, v in risk_distribution.items()],
        "condition_distribution": [{"name": k, "value": v} for k, v in condition_distribution.items()],
        "recent_logs": all_assessments[-20:]
    }

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
