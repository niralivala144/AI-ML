import os
import pandas as pd
import numpy as np
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "kmeans_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")

# Validated Segment Names
CLUSTER_NAMES = {
    0: "Moderate-Income Moderate Spenders",
    1: "High-Income High Spenders",
    2: "Low-Income High Spenders",
    3: "High-Income Low Spenders",
    4: "Low-Income Low Spenders"
}

# Fixed Universal Color Mapping
CLUSTER_COLORS = {
    0: "#3B82F6",  # Blue
    1: "#10B981",  # Green
    2: "#F59E0B",  # Amber/Orange
    3: "#8B5CF6",  # Purple
    4: "#EF4444"   # Red
}

SEGMENT_NAME_TO_COLOR = {
    "Moderate-Income Moderate Spenders": "#3B82F6",
    "High-Income High Spenders": "#10B981",
    "Low-Income High Spenders": "#F59E0B",
    "High-Income Low Spenders": "#8B5CF6",
    "Low-Income Low Spenders": "#EF4444"
}

_cached_model = None
_cached_scaler = None

def get_ml_artifacts():
    """Loads and caches the fitted StandardScaler and trained K-Means model."""
    global _cached_model, _cached_scaler
    if _cached_model is None or _cached_scaler is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
            raise FileNotFoundError("Model or scaler artifact missing from models/ directory.")
        _cached_model = joblib.load(MODEL_PATH)
        _cached_scaler = joblib.load(SCALER_PATH)
    return _cached_model, _cached_scaler

def validate_customer_inputs(age, gender, annual_income, spending_score):
    """Validates customer profile inputs according to real-world business constraints."""
    errors = []
    
    if gender not in ["Male", "Female", "Other", "Prefer not to say"]:
        errors.append("Please select a valid gender option.")
        
    try:
        age = int(age)
        if age < 18 or age > 100:
            errors.append("Age must be between 18 and 100 years.")
    except (ValueError, TypeError):
        errors.append("Age must be a valid integer.")
        
    try:
        annual_income = float(annual_income)
        if annual_income <= 0 or annual_income > 300:
            errors.append("Annual Income must be positive (between $1k and $300k).")
    except (ValueError, TypeError):
        errors.append("Annual income must be a valid number.")
        
    try:
        spending_score = int(spending_score)
        if spending_score < 1 or spending_score > 100:
            errors.append("Spending Score must be an integer between 1 and 100.")
    except (ValueError, TypeError):
        errors.append("Spending score must be a valid integer.")
        
    if errors:
        return False, " | ".join(errors)
    return True, ""

def predict_segment(annual_income: float, spending_score: int):
    """
    Transforms inputs using the fitted StandardScaler and predicts cluster using K-Means (K=5).
    Does NOT refit scaler or retrain model.
    """
    model, scaler = get_ml_artifacts()
    
    # Feature columns matching training definition exactly
    feature_names = ['Annual Income (k$)', 'Spending Score (1-100)']
    input_df = pd.DataFrame([[float(annual_income), float(spending_score)]], columns=feature_names)
    
    # Transform using fitted scaler
    scaled_features = scaler.transform(input_df)
    
    # Predict with trained KMeans model
    cluster_id = int(model.predict(scaled_features)[0])
    segment_name = CLUSTER_NAMES.get(cluster_id, f"Cluster {cluster_id}")
    
    return cluster_id, segment_name
