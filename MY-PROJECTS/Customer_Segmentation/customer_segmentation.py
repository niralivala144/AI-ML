"""
==========================================================================
 CUSTOMER SEGMENTATION — Mall Customers Dataset
 K-Means Clustering on Age, Annual Income & Spending Score
==========================================================================
Pipeline:
 1. Load data (data/Mall_Customers.csv)
 2. Clean & explore (EDA)
 3. Feature scaling
 4. Optimal cluster selection (Elbow + Silhouette)
 5. K-Means clustering
 6. PCA visualization
 7. Cluster profiling & persona naming
 8. Export results (outputs/)
==========================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from scipy.optimize import linear_sum_assignment
import os

np.random.seed(42)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
DATA_PATH = os.path.join(BASE, "data", "Mall_Customers.csv")
OUT_DIR = os.path.join(BASE, "outputs")
CHART_DIR = os.path.join(OUT_DIR, "charts")
os.makedirs(CHART_DIR, exist_ok=True)

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 130
COLORS = ["#6C5CE7", "#00B894", "#FDCB6E", "#E17055", "#0984E3", "#D63031"]

# --------------------------------------------------------------------
# 1. LOAD DATA
# --------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)
df.columns = [c.strip() for c in df.columns]
df.rename(columns={
    "Annual Income (k$)": "Annual_Income",
    "Spending Score (1-100)": "Spending_Score"
}, inplace=True)

print("Dataset shape:", df.shape)
print(df.head())
print("\nMissing values:\n", df.isnull().sum())
df.drop_duplicates(inplace=True)

# --------------------------------------------------------------------
# 2. EDA
# --------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
for ax, col in zip(axes, ["Age", "Annual_Income", "Spending_Score"]):
    sns.histplot(df[col], kde=True, ax=ax, color="#6C5CE7")
    ax.set_title(col.replace("_", " "), fontsize=12, fontweight="bold")
plt.suptitle("Exploratory Data Analysis — Feature Distributions", fontsize=15, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/01_eda_distributions.png", bbox_inches="tight")
plt.close()

plt.figure(figsize=(6, 5))
sns.heatmap(df[["Age", "Annual_Income", "Spending_Score"]].corr(), annot=True, fmt=".2f",
            cmap="RdPu", linewidths=0.5)
plt.title("Feature Correlation Heatmap", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/02_correlation_heatmap.png", bbox_inches="tight")
plt.close()

plt.figure(figsize=(6, 5))
sns.countplot(data=df, x="Gender", palette=["#E17055", "#6C5CE7"])
plt.title("Gender Distribution", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/02b_gender_distribution.png", bbox_inches="tight")
plt.close()

# --------------------------------------------------------------------
# 3. FEATURE SCALING
# --------------------------------------------------------------------
cluster_features = ["Age", "Annual_Income", "Spending_Score"]
X = df[cluster_features].copy()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --------------------------------------------------------------------
# 4. OPTIMAL K — Elbow + Silhouette
# --------------------------------------------------------------------
inertias, sil_scores = [], []
K_range = range(2, 10)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    sil_scores.append(silhouette_score(X_scaled, labels))

fig, ax1 = plt.subplots(figsize=(9, 5.5))
ax2 = ax1.twinx()
ax1.plot(list(K_range), inertias, "o-", color="#6C5CE7", linewidth=2.5, label="Inertia (Elbow)")
ax2.plot(list(K_range), sil_scores, "s-", color="#E17055", linewidth=2.5, label="Silhouette Score")
ax1.set_xlabel("Number of Clusters (k)")
ax1.set_ylabel("Inertia", color="#6C5CE7")
ax2.set_ylabel("Silhouette Score", color="#E17055")
plt.title("Optimal K Selection", fontsize=13, fontweight="bold")
fig.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=2)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/03_optimal_k.png", bbox_inches="tight")
plt.close()

best_k = list(K_range)[int(np.argmax(sil_scores))]
print(f"\nBest K by silhouette score: {best_k}")
FINAL_K = 5  # classic 5-segment mall customer split (income x spending grid)

# --------------------------------------------------------------------
# 5. FINAL K-MEANS
# --------------------------------------------------------------------
kmeans = KMeans(n_clusters=FINAL_K, random_state=42, n_init=25)
df["Cluster"] = kmeans.fit_predict(X_scaled)
sil = silhouette_score(X_scaled, df["Cluster"])
print(f"Final Silhouette Score (k={FINAL_K}): {sil:.3f}")

# --------------------------------------------------------------------
# 6. PCA VISUALIZATION
# --------------------------------------------------------------------
pca = PCA(n_components=2, random_state=42)
pcs = pca.fit_transform(X_scaled)
df["PC1"], df["PC2"] = pcs[:, 0], pcs[:, 1]

plt.figure(figsize=(9, 7))
for i in range(FINAL_K):
    sub = df[df["Cluster"] == i]
    plt.scatter(sub["PC1"], sub["PC2"], s=40, alpha=0.7, color=COLORS[i], label=f"Cluster {i}")
centers_pca = pca.transform(kmeans.cluster_centers_)
plt.scatter(centers_pca[:, 0], centers_pca[:, 1], marker="X", s=300, c="black", label="Centroids", edgecolor="white")
plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)")
plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)")
plt.title("Customer Segments — PCA Projection", fontsize=13, fontweight="bold")
plt.legend()
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/04_pca_clusters.png", bbox_inches="tight")
plt.close()

# Direct Income vs Spending Score view (very interpretable for mall data)
plt.figure(figsize=(9, 7))
for i in range(FINAL_K):
    sub = df[df["Cluster"] == i]
    plt.scatter(sub["Annual_Income"], sub["Spending_Score"], s=45, alpha=0.75, color=COLORS[i], label=f"Cluster {i}")
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score (1-100)")
plt.title("Customer Segments — Income vs Spending Score", fontsize=13, fontweight="bold")
plt.legend()
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/04b_income_vs_spending.png", bbox_inches="tight")
plt.close()

# --------------------------------------------------------------------
# 7. CLUSTER PROFILING + PERSONA NAMING (Hungarian optimal matching)
# --------------------------------------------------------------------
profile = df.groupby("Cluster")[cluster_features].mean().round(1)
profile["Count"] = df["Cluster"].value_counts().sort_index()
profile["Pct"] = (profile["Count"] / len(df) * 100).round(1)
print("\nCluster Profile:\n", profile)

persona_targets = {
    "Premium Big Spenders":   {"Age": -0.3, "Annual_Income": 1.5, "Spending_Score": 1.5},
    "Careful Affluent":       {"Age": 0.5, "Annual_Income": 1.5, "Spending_Score": -1.5},
    "Standard / Average":     {"Age": 0.0, "Annual_Income": 0.0, "Spending_Score": 0.0},
    "Young Impulsive Spenders": {"Age": -1.3, "Annual_Income": -1.0, "Spending_Score": 1.5},
    "Budget Conscious":       {"Age": 0.3, "Annual_Income": -1.5, "Spending_Score": -1.3},
}

pf_z = (profile[cluster_features] - profile[cluster_features].mean()) / (profile[cluster_features].std() + 1e-9)
persona_names = list(persona_targets.keys())
cost = np.zeros((len(profile.index), len(persona_names)))
for i, cl in enumerate(profile.index):
    for j, pname in enumerate(persona_names):
        target_vec = np.array([persona_targets[pname][f] for f in cluster_features])
        cost[i, j] = np.linalg.norm(pf_z.loc[cl].values - target_vec)
row_ind, col_ind = linear_sum_assignment(cost)
persona_map = {profile.index[r]: persona_names[c] for r, c in zip(row_ind, col_ind)}

df["Persona"] = df["Cluster"].map(persona_map)
profile["Persona"] = profile.index.map(persona_map)
print("\nPersona mapping:", persona_map)

# --------------------------------------------------------------------
# Segment size + income-vs-spending re-plot with persona labels
# --------------------------------------------------------------------
plt.figure(figsize=(9, 5.5))
order = profile.sort_values("Count", ascending=False)
bars = plt.bar(order["Persona"], order["Count"], color=COLORS[:FINAL_K])
for b in bars:
    plt.text(b.get_x() + b.get_width()/2, b.get_height() + 2, str(int(b.get_height())), ha="center", fontweight="bold")
plt.xticks(rotation=20, ha="right")
plt.ylabel("Number of Customers")
plt.title("Segment Sizes", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/05_segment_sizes.png", bbox_inches="tight")
plt.close()

# Radar chart
radar_feats = cluster_features
norm_profile = (profile[radar_feats] - profile[radar_feats].min()) / (profile[radar_feats].max() - profile[radar_feats].min() + 1e-9)
angles = np.linspace(0, 2*np.pi, len(radar_feats), endpoint=False).tolist()
angles += angles[:1]
fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
for i in profile.index:
    values = norm_profile.loc[i].tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=2, label=profile.loc[i, "Persona"], color=COLORS[i])
    ax.fill(angles, values, alpha=0.08, color=COLORS[i])
ax.set_xticks(angles[:-1])
ax.set_xticklabels([f.replace("_", " ") for f in radar_feats], fontsize=10)
ax.set_yticklabels([])
plt.title("Segment Profiles (Normalized)", fontsize=13, fontweight="bold", y=1.08)
plt.legend(loc="upper right", bbox_to_anchor=(1.4, 1.1), fontsize=9)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/06_radar_profiles.png", bbox_inches="tight")
plt.close()

# --------------------------------------------------------------------
# 8. EXPORT
# --------------------------------------------------------------------
df.to_csv(f"{OUT_DIR}/segmented_customers.csv", index=False)
profile.to_csv(f"{OUT_DIR}/cluster_profile_summary.csv")

print("\n✅ Pipeline complete. Files saved in outputs/")
