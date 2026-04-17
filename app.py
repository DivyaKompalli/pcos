"""
AI-based PCOS & Anemia Early Risk Detector
Streamlit Web Application - Research Prototype

Polycystic Ovary Syndrome (PCOS) and Anemia are among the most prevalent yet
underdiagnosed health conditions affecting women in India. This system provides
non-diagnostic risk assessment and health awareness support.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import PCOS_FEATURES, ANEMIA_FEATURES
from database.db import init_db, save_assessment, get_assessment_stats

# Page config - must be first Streamlit command
st.set_page_config(
    page_title="PCOS & Anemia Risk Detector",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for distinctive, professional design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #e2e8f0 100%);
    }
    
    .main-header {
        background: linear-gradient(90deg, #0f766e 0%, #14b8a6 50%, #2dd4bf 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(15, 118, 110, 0.25);
        text-align: center;
    }
    
    .main-header h1 {
        color: white !important;
        font-family: 'DM Sans', sans-serif;
        font-weight: 700;
        font-size: 2.2rem;
        margin: 0;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95) !important;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    .disclaimer-box {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem 1.5rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1.5rem;
    }
    
    .risk-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    .risk-low { border-left: 4px solid #22c55e; }
    .risk-moderate { border-left: 4px solid #eab308; }
    .risk-elevated { border-left: 4px solid #ef4444; }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #0f766e;
    }
    
    .info-section {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    @media (prefers-color-scheme: dark) {
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        }
        .main-header {
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        }
        .disclaimer-box {
            background: #451a03;
            border-left: 4px solid #d97706;
            color: #fef3c7;
        }
        .risk-card {
            background: #1e293b;
            border-color: #334155;
            color: #f8fafc;
            box-shadow: 0 2px 12px rgba(0,0,0,0.2);
        }
        .metric-value {
            color: #2dd4bf;
        }
        .info-section {
            background: #1e293b;
            border-color: #334155;
            color: #f8fafc;
        }
    }

/* Stitched UI Enhancements */
button[data-baseweb="tab"] {
    border-radius: 8px 8px 0 0 !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)


def ensure_models_trained():
    """Check if models exist, offer to train if not."""
    models_dir = Path(__file__).parent / "models"
    required = ["pcos_logistic.joblib", "pcos_xgboost.joblib", "anemia_logistic.joblib", "anemia_xgboost.joblib"]
    
    if all((models_dir / f).exists() for f in required):
        return True
    
    if st.button("🔄 Train ML Models (First-time setup)"):
        with st.spinner("Generating data and training models..."):
            from data.generate_data import main as gen_main
            from models.train_models import train_pcos_models, train_anemia_models
            
            gen_main()
            train_pcos_models()
            train_anemia_models()
            st.success("Models trained! Please refresh the page.")
            st.rerun()
    return False


def render_pcos_form():
    """Render PCOS risk assessment form."""
    st.markdown("### 📋 PCOS Risk Assessment")
    st.write("Fill out the details below for a personalized AI assessment.")
    
    with st.container(border=True):
        st.markdown("#### 👤 Basic Vitals & Menstrual History")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age (years)", min_value=18, max_value=50, value=25)
            bmi = st.number_input("BMI", min_value=15.0, max_value=45.0, value=23.0, step=0.5)
            menstrual_regularity = st.selectbox(
                "Menstrual cycle regularity",
                [("Regular", 0), ("Irregular", 1)],
                format_func=lambda x: x[0]
            )[1]
        with col2:
            cycle_length_days = st.number_input("Average cycle length (days)", min_value=15, max_value=60, value=28)
            irregular_periods = st.slider("Frequency of irregular periods (0=never, 4=always)", 0, 4, 0)
    
    with st.container(border=True):
        st.markdown("#### 🩺 Clinical Symptoms")
        col3, col4 = st.columns(2)
        with col3:
            hirsutism = st.slider("Excessive hair growth / hirsutism (0=none, 4=severe)", 0, 4, 0)
            acne = st.slider("Acne or pimples (0=none, 4=severe)", 0, 4, 0)
        with col4:
            hair_loss = st.slider("Hair loss or thinning (0=none, 4=severe)", 0, 4, 0)
            weight_gain = st.slider("Tendency to gain weight (0=no, 4=yes)", 0, 4, 0)
    
    with st.container(border=True):
        st.markdown("#### 🥗 Lifestyle & Diet")
        col5, col6 = st.columns(2)
        with col5:
            stress_level = st.slider("Stress level (0=low, 4=high)", 0, 4, 1)
            exercise_frequency = st.slider("Exercise frequency (0=never, 4=daily)", 0, 4, 2)
            fast_food_frequency = st.slider("Fast food consumption (0=never, 4=daily)", 0, 4, 1)
        with col6:
            diet_quality = st.slider("Overall diet quality (0=poor, 4=excellent)", 0, 4, 2)
            sleep_hours = st.slider("Average sleep (hours)", 4.0, 10.0, 6.5, 0.5)
    
    return {
        "age": age, "bmi": bmi, "menstrual_regularity": menstrual_regularity,
        "cycle_length_days": cycle_length_days, "irregular_periods": irregular_periods,
        "hirsutism": hirsutism, "acne": acne, "hair_loss": hair_loss, "weight_gain": weight_gain,
        "stress_level": stress_level, "exercise_frequency": exercise_frequency,
        "fast_food_frequency": fast_food_frequency, "diet_quality": diet_quality,
        "sleep_hours": sleep_hours
    }


def render_anemia_form():
    """Render Anemia risk assessment form."""
    st.markdown("### 📋 Anemia Risk Assessment")
    st.write("Fill out the details below for a personalized AI assessment.")
    
    with st.container(border=True):
        st.markdown("#### 👤 Basic Vitals & Dietary Habits")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age (years)", min_value=18, max_value=50, value=28, key="anemia_age")
            hemoglobin = st.number_input(
                "Hemoglobin level (g/dL) - leave 0 if unknown",
                min_value=0.0, max_value=18.0, value=12.0, step=0.5, key="anemia_hb"
            )
            if hemoglobin == 0:
                hemoglobin = 12.0  # Default for unknown
            vegetarian_diet = st.selectbox("Vegetarian diet?", [("No", 0), ("Yes", 1)], format_func=lambda x: x[0], key="anemia_veg")[1]
        with col2:
            fatigue_level = st.slider("Fatigue / tiredness level (0=none, 4=severe)", 0, 4, 1, key="anemia_fatigue")
            iron_rich_food = st.slider("Iron-rich food consumption (0=rarely, 4=daily)", 0, 4, 2, key="anemia_iron")
            diet_quality = st.slider("Overall diet quality (0=poor, 4=excellent)", 0, 4, 2, key="anemia_diet")
    
    with st.container(border=True):
        st.markdown("#### 🩺 Clinical & Lifestyle Factors")
        col3, col4 = st.columns(2)
        with col3:
            menstrual_blood_loss = st.slider("Menstrual flow (0=light, 4=very heavy)", 0, 4, 1, key="anemia_flow")
            pregnancy_count = st.number_input("Number of pregnancies", min_value=0, max_value=8, value=0, key="anemia_preg")
        with col4:
            sleep_hours = st.slider("Average sleep (hours)", 4.0, 10.0, 6.5, 0.5, key="anemia_sleep")
            stress_level = st.slider("Stress level (0=low, 4=high)", 0, 4, 1, key="anemia_stress")
    
    return {
        "age": age, "hemoglobin": hemoglobin, "fatigue_level": fatigue_level,
        "vegetarian_diet": vegetarian_diet, "iron_rich_food": iron_rich_food,
        "menstrual_blood_loss": menstrual_blood_loss, "pregnancy_count": pregnancy_count,
        "diet_quality": diet_quality, "sleep_hours": sleep_hours, "stress_level": stress_level
    }


def show_risk_result(condition: str, proba: float, level: str):
    """Display risk result with appropriate styling."""
    pct = proba * 100
    level_lower = level.lower()
    risk_class = f"risk-{level_lower}" if level_lower in ["low", "moderate", "elevated"] else "risk-moderate"
    
    st.markdown(f"""
    <div class="risk-card {risk_class}">
        <h4>Risk Probability: {pct:.1f}%</h4>
        <p class="metric-value">{level} Risk</p>
        <p><strong>Disclaimer:</strong> This is a non-diagnostic risk assessment. 
        Please consult a healthcare provider for proper diagnosis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if level == "Elevated":
        if condition == "pcos":
            st.info("""
            **Recommendation:** Consider consulting a gynecologist or endocrinologist. 
            PCOS is manageable with lifestyle changes and medical guidance. 
            Early detection supports better outcomes.
            """)
        else:
            st.info("""
            **Recommendation:** Consider a complete blood count (CBC) and consultation 
            with a physician. Iron supplementation and dietary changes may help. 
            Anemia is highly prevalent in Indian women and is often treatable.
            """)


def render_admin_dashboard():
    """Render Admin Dashboard aligned with Stitched Layout."""
    st.markdown("### 📊 Admin Analytics Dashboard")
    st.write("Overview of all risk assessments performed on this kiosk.")
    
    from database.db import get_all_assessments
    import plotly.express as px
    
    data = get_all_assessments()
    if not data:
        st.info("No assessments recorded yet.")
        return
        
    df = pd.DataFrame(data)
    
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Assessments", len(df))
        with col2:
            high_risk = len(df[df['risk_level'] == 'Elevated'])
            st.metric("Total Elevated Risk Cases", high_risk)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            fig_risk = px.pie(df, names='risk_level', title="Risk Level Distribution", color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        with st.container(border=True):
            fig_cond = px.pie(df, names='condition_type', title="Assessments by Condition", color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig_cond, use_container_width=True)
            
    st.subheader("Recent Assessment Logs")
    st.dataframe(df[['created_at', 'condition_type', 'risk_probability', 'risk_level']].head(20), use_container_width=True)


def main():
    # Initialize database
    init_db()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 AI-based PCOS & Anemia Early Risk Detector</h1>
        <p>Non-diagnostic risk assessment for Indian women | Research Prototype</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="disclaimer-box">
        <strong>⚠️ Important:</strong> This tool provides a <em>risk probability estimate</em> only. 
        It is NOT a medical diagnosis. Always consult a qualified healthcare provider for 
        proper evaluation and treatment. Designed for preventive awareness and early consultation encouragement.
    </div>
    """, unsafe_allow_html=True)
    
    # Check models
    if not ensure_models_trained():
        st.warning("Please train the ML models first using the button above.")
        return
    
    # Navigation Sidebar
    st.sidebar.title("🏥 Health Hub Menu")
    selected_tab = st.sidebar.radio(
        "Navigation",
        ["🩺 PCOS Assessment", "🩸 Anemia Assessment", "🤖 AI Health Assistant", "📊 Admin Dashboard"]
    )
    
    st.sidebar.markdown("---")
    
    st.sidebar.info("""
    This system uses **Logistic Regression** and **XGBoost** models trained on 
    synthetic data reflecting Indian population parameters. 
    
    Designed for research and health awareness.
    """)
    
    # Footer - research stats moved up in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Research Statistics")
    try:
        stats = get_assessment_stats()
        for s in stats:
            st.sidebar.metric(f"{s['condition_type'].title()} assessments", s['count'])
    except Exception:
        pass

    # Render Selected Page
    if selected_tab == "🩺 PCOS Assessment":
        pcos_inputs = render_pcos_form()
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Assess PCOS Risk", type="primary", use_container_width=True, key="pcos_btn"):
            from models.predict import predict_pcos, get_shap_explanation
            proba, level = predict_pcos(pcos_inputs)
            show_risk_result("pcos", proba, level)
            save_assessment("pcos", pcos_inputs, proba, level)
            
            with st.expander("🔍 View AI Decision Reasoning (Explainable AI)", expanded=(level == "Elevated")):
                st.write("This waterfall chart shows exactly which of your inputs increased or decreased the risk probability calculated by our XGBoost model.")
                import shap
                from streamlit_shap import st_shap
                explainer, shap_values, X = get_shap_explanation("pcos", pcos_inputs)
                st_shap(shap.plots.waterfall(shap_values[0], show=False), height=400)
            
            from utils.pdf_generator import generate_report
            pdf_path = generate_report("pcos", pcos_inputs, proba, level)
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📄 Download Assessment Report (PDF)",
                    data=pdf_file,
                    file_name="PCOS_Assessment_Report.pdf",
                    mime="application/pdf"
                )
        
    elif selected_tab == "🩸 Anemia Assessment":
        anemia_inputs = render_anemia_form()
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Assess Anemia Risk", type="primary", use_container_width=True, key="anemia_btn"):
            from models.predict import predict_anemia, get_shap_explanation
            proba, level = predict_anemia(anemia_inputs)
            show_risk_result("anemia", proba, level)
            save_assessment("anemia", anemia_inputs, proba, level)
            
            with st.expander("🔍 View AI Decision Reasoning (Explainable AI)", expanded=(level == "Elevated")):
                st.write("This waterfall chart shows exactly which of your inputs increased or decreased the risk probability calculated by our XGBoost model.")
                import shap
                from streamlit_shap import st_shap
                explainer, shap_values, X = get_shap_explanation("anemia", anemia_inputs)
                st_shap(shap.plots.waterfall(shap_values[0], show=False), height=400)
                
            from utils.pdf_generator import generate_report
            pdf_path = generate_report("anemia", anemia_inputs, proba, level)
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📄 Download Assessment Report (PDF)",
                    data=pdf_file,
                    file_name="Anemia_Assessment_Report.pdf",
                    mime="application/pdf"
                )
                
    elif selected_tab == "🤖 AI Health Assistant":
        from utils.chatbot import render_chatbot
        render_chatbot()
    
    elif selected_tab == "📊 Admin Dashboard":
        render_admin_dashboard()


if __name__ == "__main__":
    main()
