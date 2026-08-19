"""
Customer Segmentation ML Project - Final Training Pipeline
-----------------------------------------------------------
Trains K-Means (K=5) on standardized Annual Income and Spending Score,
persists the model and scaler artifacts using joblib, and exports
the enriched segmented customer dataset.
"""

import os
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 1. Paths Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "Mall_Customers.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

MODEL_PATH = os.path.join(MODELS_DIR, "kmeans_model.pkl")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.pkl")
OUTPUT_CSV_PATH = os.path.join(OUTPUTS_DIR, "segmented_customers.csv")

# 2. Objective Segment Mapping
SEGMENT_NAMES = {
    0: "Moderate-Income Moderate Spenders",
    1: "High-Income High Spenders",
    2: "Low-Income High Spenders",
    3: "High-Income Low Spenders",
    4: "Low-Income Low Spenders"
}

def train_and_export():
    print("=" * 60)
    print("Customer Segmentation - Final ML Pipeline Training")
    print("=" * 60)

    # Ensure output directories exist
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    # 1. Load Dataset (Read-only, without modifying original file)
    print(f"\n[1/5] Loading original dataset from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    print(f"      Loaded {len(df)} rows and {len(df.columns)} columns.")

    # 2. Feature Selection
    feature_cols = ['Annual Income (k$)', 'Spending Score (1-100)']
    print(f"\n[2/5] Selected clustering features: {feature_cols}")
    X = df[feature_cols].copy()

    # 3. Preprocessing with StandardScaler
    print("\n[3/5] Fitting and applying StandardScaler...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 4. Train K-Means (K=5, random_state=42, n_init=10)
    print("\n[4/5] Training K-Means model (K=5, random_state=42, n_init=10)...")
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    df['Cluster'] = cluster_labels
    df['Segment Name'] = df['Cluster'].map(SEGMENT_NAMES)

    # 5. Export Model & Scaler Artifacts
    print("\n[5/5] Exporting artifacts...")
    joblib.dump(kmeans, MODEL_PATH)
    print(f"      - Saved KMeans model: {MODEL_PATH}")

    joblib.dump(scaler, SCALER_PATH)
    print(f"      - Saved StandardScaler: {SCALER_PATH}")

    # Export Segmented Dataset
    output_columns = [
        'CustomerID',
        'Gender',
        'Age',
        'Annual Income (k$)',
        'Spending Score (1-100)',
        'Cluster',
        'Segment Name'
    ]
    df_segmented = df[output_columns]
    df_segmented.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"      - Saved segmented customer data: {OUTPUT_CSV_PATH}")

    # Validation Summary
    print("\n" + "=" * 60)
    print("Verification & Validation Summary")
    print("=" * 60)
    print(f"Inertia (WCSS): {kmeans.inertia_:.4f}")
    print("\nCluster Distribution:")
    for cluster_id in sorted(df['Cluster'].unique()):
        sub = df[df['Cluster'] == cluster_id]
        name = SEGMENT_NAMES[cluster_id]
        print(f"  Cluster {cluster_id} ({name}):")
        print(f"    Count: {len(sub)} ({len(sub)/len(df)*100:.1f}%) | "
              f"Avg Income: ${sub['Annual Income (k$)'].mean():.1f}k | "
              f"Avg Spend: {sub['Spending Score (1-100)'].mean():.1f} | "
              f"Avg Age: {sub['Age'].mean():.1f} yrs")

    # Verify model reloading
    loaded_model = joblib.load(MODEL_PATH)
    loaded_scaler = joblib.load(SCALER_PATH)
    test_sample = pd.DataFrame([[80.0, 80.0]], columns=feature_cols)
    test_scaled = loaded_scaler.transform(test_sample)
    pred_cluster = int(loaded_model.predict(test_scaled)[0])
    pred_name = SEGMENT_NAMES[pred_cluster]
    print(f"\nArtifact Verification Test:")
    print(f"  Input: Income=$80k, Spend Score=80 -> Predicted: Cluster {pred_cluster} ({pred_name})")
    print("Pipeline execution completed successfully!\n")

if __name__ == "__main__":
    train_and_export()
