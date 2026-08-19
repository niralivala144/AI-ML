import os
import pandas as pd
import numpy as np
import joblib
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Database operations
from src.database import init_db, save_new_customer, get_all_app_customers

# Initialize SQLite database
init_db()

# ---------------------------------------------------------
# Page Configuration & Dark Professional Theme
# ---------------------------------------------------------
st.set_page_config(
    page_title="Customer Segmentation Intelligence Platform",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished dark professional styling
st.markdown("""
<style>
    /* Global Container Spacing */
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1320px;
    }
    
    /* Header Styling */
    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.2rem;
    }
    .app-subtitle {
        font-size: 1.02rem;
        color: #9CA3AF;
        margin-bottom: 1.6rem;
    }
    
    /* KPI Metric Cards */
    .kpi-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.1rem 1rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
    }
    .kpi-val {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.15rem;
    }
    .kpi-lbl {
        font-size: 0.78rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Segment Info Card */
    .segment-card {
        background: rgba(30, 41, 59, 0.6);
        border-left: 6px solid #3B82F6;
        border-radius: 8px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .segment-badge {
        display: inline-block;
        padding: 0.25rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# File Paths & Data Loading
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "outputs", "segmented_customers.csv")
ORIGINAL_DATA_PATH = os.path.join(BASE_DIR, "Mall_Customers.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "kmeans_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")

# ---------------------------------------------------------
# Fixed Universal Palette & Cluster Knowledge Base
# (Strictly consistent across all charts, cards, and tables)
# ---------------------------------------------------------
SEGMENT_COLORS = {
    "Moderate-Income Moderate Spenders": "#3B82F6",  # Blue (Cluster 0)
    "High-Income High Spenders": "#10B981",          # Emerald Green (Cluster 1)
    "Low-Income High Spenders": "#F59E0B",           # Amber/Orange (Cluster 2)
    "High-Income Low Spenders": "#8B5CF6",           # Purple (Cluster 3)
    "Low-Income Low Spenders": "#EF4444"             # Red (Cluster 4)
}

CLUSTER_TO_NAME = {
    0: "Moderate-Income Moderate Spenders",
    1: "High-Income High Spenders",
    2: "Low-Income High Spenders",
    3: "High-Income Low Spenders",
    4: "Low-Income Low Spenders"
}

# Empirical Knowledge Base grounded ONLY in validated statistics
CLUSTER_STRATEGY_INFO = {
    0: {
        "name": "Moderate-Income Moderate Spenders",
        "short_name": "Cluster 0: Moderate Income & Spend",
        "cluster_id": 0,
        "color": "#3B82F6",
        "income_cat": "Moderate Income ($39k - $76k, Mean: $55.3k)",
        "spending_cat": "Moderate Spending (34 - 61, Mean: 49.5)",
        "characteristics": "Represents the central baseline of the customer base. Balanced spending habits proportional to earnings, with broad demographic age representation (18-70 yrs, Mean: 42.7 yrs).",
        "role": "Volume & Stability Anchor (Provides steady foot traffic and reliable baseline revenue for general retail).",
        "marketing_strategy": "Consistent broad-reach promotional campaigns, seasonal retail events, and family shopping weekend promotions.",
        "offer_strategy": "Mid-tier product assortments, bundled product discounts, and seasonal shopping incentives.",
        "retention_strategy": "Standard points-based loyalty tier with achievable redemption thresholds to maintain repeat visit frequency.",
        "objective": "Protect visit frequency and maintain stable recurring baseline revenue."
    },
    1: {
        "name": "High-Income High Spenders",
        "short_name": "Cluster 1: High Income & Spend",
        "cluster_id": 1,
        "color": "#10B981",
        "income_cat": "High Income ($69k - $137k, Mean: $86.5k)",
        "spending_cat": "High Spending (63 - 97, Mean: 82.1)",
        "characteristics": "High purchasing power combined with high spending score. Younger-to-mid adulthood profile (27-40 yrs, Mean: 32.7 yrs). Highest revenue contributor per customer.",
        "role": "Primary High-Margin Growth Engine (Top gross revenue and high transaction capacity).",
        "marketing_strategy": "Direct relationship marketing, private product showcases, bespoke previews, and personalized communication.",
        "offer_strategy": "Premium product lines, latest product releases, and priority reservation services.",
        "retention_strategy": "Exclusive VIP loyalty privileges, dedicated shopping amenities, and priority access.",
        "objective": "Maximize customer retention and preserve top-tier engagement."
    },
    2: {
        "name": "Low-Income High Spenders",
        "short_name": "Cluster 2: Low Income & High Spend",
        "cluster_id": 2,
        "color": "#F59E0B",
        "income_cat": "Low Income ($15k - $39k, Mean: $25.7k)",
        "spending_cat": "High Spending (61 - 99, Mean: 79.4)",
        "characteristics": "High spending score despite lower income bracket. Youngest demographic in the customer portfolio (18-35 yrs, Mean: 25.3 yrs). High responsiveness to active campaigns.",
        "role": "High-Velocity Retail Driver (Fast-moving retail velocity in accessible price categories).",
        "marketing_strategy": "High-frequency promotional announcements, limited-time alerts, and interactive event-driven marketing.",
        "offer_strategy": "Accessible entry-level pricing, combo promotional deals, and packaged retail offerings.",
        "retention_strategy": "Instant gratification reward mechanics, punch-card rewards, and check-in incentives.",
        "objective": "Capture high spending inclination while maintaining accessible price points."
    },
    3: {
        "name": "High-Income Low Spenders",
        "short_name": "Cluster 3: High Income & Low Spend",
        "cluster_id": 3,
        "color": "#8B5CF6",
        "income_cat": "High Income ($70k - $137k, Mean: $88.2k)",
        "spending_cat": "Low Spending (1 - 39, Mean: 17.1)",
        "characteristics": "Highest average income among all segments, but lowest spending score. Mature customer cohort (19-59 yrs, Mean: 41.1 yrs, 54.3% Male). High capacity with cautious spending.",
        "role": "Highest Untapped Growth Opportunity (Substantial disposable income currently uncaptured).",
        "marketing_strategy": "Value-justification, reliability, and trust-centered messaging highlighting quality and utility.",
        "offer_strategy": "High-durability merchandise, electronics, home improvement, and premium specialized personal services.",
        "retention_strategy": "Extended warranties, satisfaction assurances, and tailored consultation assistance.",
        "objective": "Convert high purchasing capacity into higher mall expenditure by addressing category relevance."
    },
    4: {
        "name": "Low-Income Low Spenders",
        "short_name": "Cluster 4: Low Income & Low Spend",
        "cluster_id": 4,
        "color": "#EF4444",
        "income_cat": "Low Income ($15k - $39k, Mean: $26.3k)",
        "spending_cat": "Low Spending (3 - 40, Mean: 20.9)",
        "characteristics": "Low income combined with low spending score. Oldest customer cohort on average (19-67 yrs, Mean: 45.2 yrs). Highly price-conscious with cautious shopping patterns.",
        "role": "Essential Foot-Traffic Driver (Consistent demand for staple goods and clearance inventory).",
        "marketing_strategy": "Direct price-point advertising, value circulars, and clearance sale notifications.",
        "offer_strategy": "Everyday staple goods, clearance racks, and multi-buy budget promotions.",
        "retention_strategy": "Cashback rewards on everyday essentials and seasonal coupon booklets.",
        "objective": "Serve price-conscious demand efficiently with minimal marketing overhead."
    }
}

# ---------------------------------------------------------
# Loaders for Data & Machine Learning Models
# ---------------------------------------------------------
@st.cache_data
def load_dataset():
    if os.path.exists(DATA_PATH):
        data = pd.read_csv(DATA_PATH)
    elif os.path.exists(ORIGINAL_DATA_PATH):
        data = pd.read_csv(ORIGINAL_DATA_PATH)
        data['Cluster'] = 0
        data['Segment Name'] = CLUSTER_TO_NAME[0]
    else:
        st.error("Error: Dataset could not be located.")
        st.stop()
    return data

@st.cache_resource
def load_ml_pipeline():
    loaded_model = None
    loaded_scaler = None
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        loaded_model = joblib.load(MODEL_PATH)
        loaded_scaler = joblib.load(SCALER_PATH)
    return loaded_model, loaded_scaler

df = load_dataset()
model, scaler = load_ml_pipeline()

# ---------------------------------------------------------
# Dynamic Aggregations from Actual Dataset
# ---------------------------------------------------------
total_customers = len(df)
total_clusters = int(df['Cluster'].nunique()) if 'Cluster' in df.columns else 5
mean_income_dataset = df['Annual Income (k$)'].mean()
median_income_dataset = df['Annual Income (k$)'].median()
mean_spend_dataset = df['Spending Score (1-100)'].mean()
median_spend_dataset = df['Spending Score (1-100)'].median()
mean_age_dataset = df['Age'].mean()
median_age_dataset = df['Age'].median()

# Dynamic Segment Summary Table
summary_stats = df.groupby(['Cluster', 'Segment Name']).agg(
    Customer_Count=('CustomerID', 'count'),
    Mean_Income=('Annual Income (k$)', 'mean'),
    Median_Income=('Annual Income (k$)', 'median'),
    Min_Income=('Annual Income (k$)', 'min'),
    Max_Income=('Annual Income (k$)', 'max'),
    Mean_Spend=('Spending Score (1-100)', 'mean'),
    Median_Spend=('Spending Score (1-100)', 'median'),
    Min_Spend=('Spending Score (1-100)', 'min'),
    Max_Spend=('Spending Score (1-100)', 'max'),
    Mean_Age=('Age', 'mean'),
    Median_Age=('Age', 'median')
).reset_index()

summary_stats['Percentage'] = (summary_stats['Customer_Count'] / total_customers) * 100.0
summary_stats = summary_stats.sort_values(by='Cluster', ascending=True)

# ---------------------------------------------------------
# Sidebar Navigation (Exact UI & Structure Preserved)
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shopping-mall.png", width=70)
    st.title("Navigation")
    
    app_mode = st.radio(
        "Select Section:",
        [
            "📊 Executive Dashboard",
            "🎯 Customer Segmentation Plot",
            "📋 Segment Profiles",
            "🔍 Customer Lookup & Predictor",
            "💡 Strategic Business Insights",
            "📥 Export & Raw Data"
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 🎨 Segment Color Key")
    for c_id in sorted(CLUSTER_STRATEGY_INFO.keys()):
        c_info = CLUSTER_STRATEGY_INFO[c_id]
        st.markdown(
            f'<div style="display:flex; align-items:center; margin-bottom:6px;">'
            f'<span style="display:inline-block; width:12px; height:12px; background-color:{c_info["color"]}; border-radius:3px; margin-right:8px;"></span>'
            f'<span style="font-size:0.85rem;"><strong>Cluster {c_id}:</strong> {c_info["name"]}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    st.markdown("### 📌 Model Configuration")
    st.info(
        "**Algorithm:** K-Means (K=5)\n"
        "**Features:** Annual Income, Spending Score\n"
        "**Preprocessing:** StandardScaler\n"
        "**Database:** SQLite Active\n"
        "**Status:** Production Ready"
    )
    
    st.caption("Customer Segmentation Intelligence Platform © 2026")

# ---------------------------------------------------------
# Main Page Header
# ---------------------------------------------------------
st.markdown('<div class="app-title">🛍️ Customer Segmentation Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Data-driven behavioral clustering & targeted marketing optimization engine</div>', unsafe_allow_html=True)

# =========================================================
# SECTION 1: 📊 EXECUTIVE DASHBOARD
# =========================================================
if app_mode == "📊 Executive Dashboard":
    st.markdown('<div class="section-header">1. Dashboard Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-val" style="color: #60A5FA;">{total_customers}</div>
            <div class="kpi-lbl">Total Customers</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-val" style="color: #34D399;">{total_clusters}</div>
            <div class="kpi-lbl">Customer Segments</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-val" style="color: #FBBF24;">${mean_income_dataset:.1f}k</div>
            <div class="kpi-lbl">Avg. Annual Income</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-val" style="color: #A78BFA;">{mean_spend_dataset:.1f} / 100</div>
            <div class="kpi-lbl">Avg. Spending Score</div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-val" style="color: #F87171;">{mean_age_dataset:.1f} yrs</div>
            <div class="kpi-lbl">Avg. Customer Age</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">2. Customer Segment Distribution</div>', unsafe_allow_html=True)
    
    col_bar, col_donut = st.columns([3, 2])
    
    with col_bar:
        # Segment Headcount Bar Chart
        bar_df = summary_stats.sort_values(by='Customer_Count', ascending=False)
        fig_bar = px.bar(
            bar_df,
            x='Segment Name',
            y='Customer_Count',
            color='Segment Name',
            color_discrete_map=SEGMENT_COLORS,
            text=bar_df.apply(lambda r: f"{r['Customer_Count']} ({r['Percentage']:.1f}%)", axis=1),
            labels={'Customer_Count': 'Number of Customers', 'Segment Name': 'Customer Segment'},
            title='Customer Headcount & Share by Segment'
        )
        fig_bar.update_layout(
            showlegend=False,
            height=390,
            xaxis_tickangle=-20,
            margin=dict(l=20, r=20, t=40, b=60)
        )
        fig_bar.update_traces(textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col_donut:
        # Improved Donut Chart with Short Clean Labels & Full Legend
        donut_df = summary_stats.copy()
        donut_df['Short Label'] = donut_df['Cluster'].map(lambda c: f"Cluster {c}")
        
        fig_donut = px.pie(
            donut_df,
            names='Segment Name',
            values='Customer_Count',
            color='Segment Name',
            color_discrete_map=SEGMENT_COLORS,
            hole=0.55,
            title='Customer Share Distribution'
        )
        fig_donut.update_traces(
            textinfo='percent',
            hovertemplate='<b>%{label}</b><br>Customer Count: %{value}<br>Share: %{percent}<extra></extra>',
            textfont_size=13
        )
        fig_donut.update_layout(
            height=390,
            legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5, font=dict(size=10)),
            margin=dict(l=10, r=10, t=40, b=50)
        )
        st.plotly_chart(fig_donut, use_container_width=True)

# =========================================================
# SECTION 2: 🎯 CUSTOMER SEGMENTATION PLOT
# =========================================================
elif app_mode == "🎯 Customer Segmentation Plot":
    st.markdown('<div class="section-header">3. Customer Segmentation Visualization</div>', unsafe_allow_html=True)
    st.markdown(
        "Interactive 2D visualization of customers mapped across **Annual Income** vs **Spending Score**. "
        "Hover over individual data points to view Customer ID, Age, Gender, and assigned behavioral segment."
    )
    
    # Calculate Centroids in original scale
    centroids_df = df.groupby(['Cluster', 'Segment Name'])[['Annual Income (k$)', 'Spending Score (1-100)']].mean().reset_index()
    
    fig_scatter = px.scatter(
        df,
        x='Annual Income (k$)',
        y='Spending Score (1-100)',
        color='Segment Name',
        color_discrete_map=SEGMENT_COLORS,
        hover_data=['CustomerID', 'Gender', 'Age', 'Annual Income (k$)', 'Spending Score (1-100)', 'Cluster', 'Segment Name'],
        title='Customer Behavioral Clusters (Income vs. Spending Propensity)',
        labels={'Annual Income (k$)': 'Annual Income ($k)', 'Spending Score (1-100)': 'Spending Score (1-100)'}
    )
    
    # Add Centroid markers
    fig_scatter.add_trace(
        go.Scatter(
            x=centroids_df['Annual Income (k$)'],
            y=centroids_df['Spending Score (1-100)'],
            mode='markers+text',
            marker=dict(symbol='x', size=16, color='white', line=dict(width=2, color='black')),
            text=centroids_df['Cluster'].apply(lambda c: f"Centroid {c}"),
            textposition="top center",
            name='Cluster Centroids',
            hovertemplate='<b>Centroid %{text}</b><br>Income: $%{x:.1f}k<br>Spending: %{y:.1f}<extra></extra>'
        )
    )
    
    fig_scatter.update_traces(marker=dict(size=10, opacity=0.88, line=dict(width=0.5, color='#1F2937')), selector=dict(mode='markers'))
    fig_scatter.update_layout(
        height=580,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=50, b=90)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    with st.expander("🔍 View Centroids Map & Boxplot Diagnostics"):
        tab_c1, tab_c2 = st.tabs(["📍 Centroid Coordinates", "📦 Feature Distribution Boxplots"])
        with tab_c1:
            fig_cent = go.Figure()
            for idx, row in centroids_df.iterrows():
                c_name = row['Segment Name']
                c_color = SEGMENT_COLORS.get(c_name, '#3B82F6')
                c_id = int(row['Cluster'])
                fig_cent.add_trace(go.Scatter(
                    x=[row['Annual Income (k$)']],
                    y=[row['Spending Score (1-100)']],
                    mode='markers+text',
                    marker=dict(size=22, color=c_color, line=dict(width=2, color='white')),
                    name=f"Cluster {c_id}: {c_name}",
                    text=[f"Cluster {c_id}<br>(${row['Annual Income (k$)']:.1f}k, {row['Spending Score (1-100)']:.1f})"],
                    textposition="top center"
                ))
            fig_cent.update_layout(
                title='Cluster Centroids in Original Space',
                xaxis=dict(title='Annual Income (k$)', range=[10, 110]),
                yaxis=dict(title='Spending Score (1-100)', range=[0, 105]),
                height=450
            )
            st.plotly_chart(fig_cent, use_container_width=True)
            
        with tab_c2:
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                fig_b1 = px.box(df, x='Segment Name', y='Annual Income (k$)', color='Segment Name', color_discrete_map=SEGMENT_COLORS, title='Annual Income by Segment')
                fig_b1.add_hline(y=mean_income_dataset, line_dash="dash", line_color="#F87171")
                fig_b1.update_layout(showlegend=False, xaxis_tickangle=-25, height=380)
                st.plotly_chart(fig_b1, use_container_width=True)
            with col_b2:
                fig_b2 = px.box(df, x='Segment Name', y='Spending Score (1-100)', color='Segment Name', color_discrete_map=SEGMENT_COLORS, title='Spending Score by Segment')
                fig_b2.add_hline(y=mean_spend_dataset, line_dash="dash", line_color="#F87171")
                fig_b2.update_layout(showlegend=False, xaxis_tickangle=-25, height=380)
                st.plotly_chart(fig_b2, use_container_width=True)

# =========================================================
# SECTION 3: 📋 SEGMENT PROFILES
# =========================================================
elif app_mode == "📋 Segment Profiles":
    st.markdown('<div class="section-header">4. Quantitative Segment Profiles</div>', unsafe_allow_html=True)
    st.markdown(
        "Detailed breakdown of statistical benchmarks, customer counts, and averages calculated dynamically "
        "from the 200 customer dataset records. No values are hardcoded."
    )
    
    profile_table = pd.DataFrame({
        "Cluster": summary_stats['Cluster'],
        "Segment Name": summary_stats['Segment Name'],
        "Customer Count": summary_stats['Customer_Count'],
        "Percentage": summary_stats['Percentage'].map("{:.1f}%".format),
        "Mean Income": summary_stats['Mean_Income'].map("${:.2f}k".format),
        "Median Income": summary_stats['Median_Income'].map("${:.2f}k".format),
        "Minimum Income": summary_stats['Min_Income'].map("${:.0f}k".format),
        "Maximum Income": summary_stats['Max_Income'].map("${:.0f}k".format),
        "Mean Spending Score": summary_stats['Mean_Spend'].map("{:.2f}".format),
        "Median Spending Score": summary_stats['Median_Spend'].map("{:.2f}".format),
        "Minimum Spending Score": summary_stats['Min_Spend'].map("{:.0f}".format),
        "Maximum Spending Score": summary_stats['Max_Spend'].map("{:.0f}".format),
        "Mean Age": summary_stats['Mean_Age'].map("{:.2f} yrs".format),
        "Median Age": summary_stats['Median_Age'].map("{:.1f} yrs".format)
    })
    
    st.dataframe(profile_table, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("#### 🌐 Overall Dataset Benchmark Comparison")
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Total Customers", f"{total_customers}")
    b2.metric("Dataset Mean Income", f"${mean_income_dataset:.2f}k")
    b3.metric("Dataset Mean Spending", f"{mean_spend_dataset:.2f} / 100")
    b4.metric("Dataset Mean Age", f"{mean_age_dataset:.2f} yrs")

# =========================================================
# SECTION 4: 🔍 CUSTOMER LOOKUP & PREDICTOR (REAL APP ADDITIONS)
# =========================================================
elif app_mode == "🔍 Customer Lookup & Predictor":
    st.markdown('<div class="section-header">5. Customer Lookup & Predictor</div>', unsafe_allow_html=True)
    
    # Sub-tabs for Existing Customer vs Add New Customer
    tab_lookup, tab_add_new = st.tabs(["🔍 Existing Customer (Lookup)", "➕ Add New Customer (Predict & Save)"])
    
    # --- SUB-TAB 1: EXISTING CUSTOMER LOOKUP ---
    with tab_lookup:
        st.markdown("#### Search Historical Customer by ID")
        all_cust_ids = sorted(df['CustomerID'].dropna().astype(int).unique().tolist())
        
        selected_cust_id = st.selectbox(
            "Select Customer ID (1 to 200):",
            options=all_cust_ids,
            index=0
        )
        
        cust_match = df[df['CustomerID'] == selected_cust_id]
        
        if not cust_match.empty:
            c_row = cust_match.iloc[0]
            c_cluster = int(c_row['Cluster'])
            c_segment = c_row['Segment Name']
            c_color = SEGMENT_COLORS.get(c_segment, '#3B82F6')
            
            st.markdown(
                f'<div class="segment-card" style="border-left-color: {c_color};">'
                f'<span class="segment-badge" style="background-color: {c_color}; color: white;">'
                f'Cluster {c_cluster}: {c_segment}'
                f'</span>'
                f'<h3 style="margin-top:0; margin-bottom: 0.5rem;">Customer #{selected_cust_id} Overview</h3>'
                f'</div>',
                unsafe_allow_html=True
            )
            
            d1, d2, d3, d4 = st.columns(4)
            d1.metric("Gender", f"{c_row['Gender']}")
            d2.metric("Age", f"{c_row['Age']} years")
            d3.metric("Annual Income", f"${c_row['Annual Income (k$)']}k")
            d4.metric("Spending Score", f"{c_row['Spending Score (1-100)']} / 100")
            
            # Segment calculated profile
            seg_stats = summary_stats[summary_stats['Cluster'] == c_cluster].iloc[0]
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 📊 Segment's Calculated Benchmark Profile")
            
            cmp1, cmp2, cmp3, cmp4 = st.columns(4)
            cmp1.metric("Segment Size", f"{int(seg_stats['Customer_Count'])} customers ({seg_stats['Percentage']:.1f}%)")
            cmp2.metric("Segment Avg Income", f"${seg_stats['Mean_Income']:.1f}k")
            cmp3.metric("Segment Avg Spend", f"{seg_stats['Mean_Spend']:.1f} / 100")
            cmp4.metric("Segment Avg Age", f"{seg_stats['Mean_Age']:.1f} yrs")
            
            strat_info = CLUSTER_STRATEGY_INFO[c_cluster]
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                f'<div class="segment-card" style="border-left-color: {c_color};">'
                f'<h4 style="margin-top:0; color: #E2E8F0;">Behavioral Context & Strategy: {c_segment}</h4>'
                f'<p><strong>Behavioral Profile:</strong> {strat_info["characteristics"]}</p>'
                f'<p><strong>Business Role:</strong> {strat_info["role"]}</p>'
                f'<p><strong>Recommended Strategy:</strong> {strat_info["marketing_strategy"]}</p>'
                f'<p><strong>Primary Objective:</strong> {strat_info["objective"]}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            
    # --- SUB-TAB 2: ADD NEW CUSTOMER (PREDICTION & SQLITE SAVE) ---
    with tab_add_new:
        st.markdown("#### Add New Customer Information")
        st.markdown("Enter customer details to run real-time K-Means (K=5) segmentation and permanently save their record to the database.")
        
        with st.form("new_customer_form"):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                new_name = st.text_input("Customer Full Name:", placeholder="e.g. Sarah Jenkins")
                new_gender = st.selectbox("Gender:", options=["Female", "Male", "Other"])
                new_age = st.number_input("Age (Years):", min_value=18, max_value=100, value=30, step=1)
                
            with f_col2:
                new_income = st.number_input("Annual Income (k$):", min_value=10.0, max_value=200.0, value=65.0, step=1.0, help="Annual income in thousands of dollars.")
                new_spend = st.slider("Spending Score (1-100):", min_value=1, max_value=100, value=50, step=1, help="Spending propensity score (1 to 100).")
                
            analyze_btn = st.form_submit_button("🚀 Analyze Customer", type="primary", use_container_width=True)
            
        if analyze_btn:
            if not new_name or len(new_name.strip()) < 2:
                st.error("Please enter a valid customer name (at least 2 characters).")
            elif model is None or scaler is None:
                st.error("Model artifacts not loaded. Please ensure models/ directory exists.")
            else:
                # Preprocess with saved scaler & predict with saved K-Means (K=5)
                feature_names = ['Annual Income (k$)', 'Spending Score (1-100)']
                input_df = pd.DataFrame([[new_income, new_spend]], columns=feature_names)
                scaled_input = scaler.transform(input_df)
                pred_cluster = int(model.predict(scaled_input)[0])
                pred_segment = CLUSTER_TO_NAME.get(pred_cluster, f"Cluster {pred_cluster}")
                
                # Cache analysis results in session state
                st.session_state['latest_analysis'] = {
                    'name': new_name.strip(),
                    'gender': new_gender,
                    'age': int(new_age),
                    'annual_income': float(new_income),
                    'spending_score': int(new_spend),
                    'cluster': pred_cluster,
                    'segment_name': pred_segment
                }
                
        # Display prediction results if available in session state
        if 'latest_analysis' in st.session_state:
            res = st.session_state['latest_analysis']
            res_cluster = res['cluster']
            res_segment = res['segment_name']
            res_color = SEGMENT_COLORS.get(res_segment, '#3B82F6')
            res_info = CLUSTER_STRATEGY_INFO[res_cluster]
            res_stats = summary_stats[summary_stats['Cluster'] == res_cluster].iloc[0]
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🎯 Analysis Result")
            
            # Customer Information & Segment Cards
            customer_card_html = (
                f'<div class="segment-card" style="border-left-color: {res_color}; background: rgba(30, 41, 59, 0.85);">'
                f'<span class="segment-badge" style="background-color: {res_color}; color: white; font-size: 0.95rem; padding: 0.35rem 1rem;">'
                f'Predicted: Cluster {res_cluster} • {res_segment}'
                f'</span>'
                f'<h2 style="margin-top: 0.4rem; margin-bottom: 0.4rem; color: #F8FAFC;">'
                f'{res["name"]} ➔ {res_segment}'
                f'</h2>'
                f'<hr style="border-color: rgba(255,255,255,0.1); margin: 0.8rem 0;">'
                f'<div style="font-size: 1.05rem; color: #E2E8F0; margin-bottom: 6px;">'
                f'<strong>Gender:</strong> {res["gender"]} &nbsp;|&nbsp; <strong>Age:</strong> {res["age"]} yrs'
                f'</div>'
                f'<div style="font-size: 1.05rem; color: #E2E8F0;">'
                f'<strong>Annual Income:</strong> ${res["annual_income"]:.1f}k &nbsp;|&nbsp; <strong>Spending Score:</strong> {res["spending_score"]} / 100'
                f'</div>'
                f'</div>'
            )
            st.markdown(customer_card_html, unsafe_allow_html=True)
            
            # Segment Calculated Statistics
            st.markdown("#### 📊 Segment Information & Statistics")
            res_c1, res_c2, res_c3, res_c4 = st.columns(4)
            res_c1.metric("Segment Share", f"{int(res_stats['Customer_Count'])} shoppers ({res_stats['Percentage']:.1f}%)")
            res_c2.metric("Segment Avg Income", f"${res_stats['Mean_Income']:.1f}k")
            res_c3.metric("Segment Avg Spend", f"{res_stats['Mean_Spend']:.1f} / 100")
            res_c4.metric("Segment Avg Age", f"{res_stats['Mean_Age']:.1f} yrs")
            
            # Behavioral Profile & Business Strategy
            st.markdown(
                f'<div class="segment-card" style="border-left-color: {res_color};">'
                f'<h4 style="margin-top:0; color: #93C5FD;">Strategic Playbook for {res_segment}</h4>'
                f'<p><strong>Behavioral Description:</strong> {res_info["characteristics"]}</p>'
                f'<p><strong>Business Opportunity / Role:</strong> {res_info["role"]}</p>'
                f'<p><strong>Recommended Marketing Strategy:</strong> {res_info["marketing_strategy"]}</p>'
                f'<p><strong>Product & Offer Focus:</strong> {res_info["offer_strategy"]}</p>'
                f'<p><strong>Primary Objective:</strong> {res_info["objective"]}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            
            # Save Customer Button
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Save Customer to Database", type="primary", use_container_width=True):
                saved_id, msg = save_new_customer(
                    name=res['name'],
                    gender=res['gender'],
                    age=res['age'],
                    annual_income=res['annual_income'],
                    spending_score=res['spending_score'],
                    cluster=res['cluster'],
                    segment_name=res['segment_name']
                )
                if saved_id:
                    st.success(f"✅ {msg} (Record ID #{saved_id})")
                    st.info("You can view and export this customer record under the 'Export & Raw Data' -> 'Application Customers' tab.")
                else:
                    st.error(f"Failed to save customer: {msg}")

# =========================================================
# SECTION 5: 💡 STRATEGIC BUSINESS INSIGHTS
# =========================================================
elif app_mode == "💡 Strategic Business Insights":
    st.markdown('<div class="section-header">6. Strategic Business Insights & Marketing Playbooks</div>', unsafe_allow_html=True)
    st.markdown(
        "Segment-specific marketing playbooks and strategic business opportunities derived directly from "
        "the empirical cluster profiles."
    )
    
    selected_c_id = st.selectbox(
        "Select Customer Segment to view Playbook:",
        options=list(CLUSTER_STRATEGY_INFO.keys()),
        format_func=lambda cid: f"Cluster {cid}: {CLUSTER_STRATEGY_INFO[cid]['name']}",
        index=0
    )
    
    c_strat = CLUSTER_STRATEGY_INFO[selected_c_id]
    c_color = c_strat['color']
    c_stats = summary_stats[summary_stats['Cluster'] == selected_c_id].iloc[0]
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Segment Size", f"{int(c_stats['Customer_Count'])} customers ({c_stats['Percentage']:.1f}%)")
    m2.metric("Average Income", f"${c_stats['Mean_Income']:.1f}k")
    m3.metric("Average Spending Score", f"{c_stats['Mean_Spend']:.1f} / 100")
    m4.metric("Average Age", f"{c_stats['Mean_Age']:.1f} years")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<div class="segment-card" style="border-left-color: {c_color};">'
        f'<span class="segment-badge" style="background-color: {c_color}; color: white;">'
        f'Cluster {selected_c_id} Strategy Playbook'
        f'</span>'
        f'<h2 style="margin-top:0.2rem; color: #F8FAFC;">{c_strat["name"]}</h2>'
        f'<hr style="border-color: rgba(255,255,255,0.1); margin: 0.8rem 0;">'
        f'<p><strong>📊 Behavioral Interpretation:</strong><br>{c_strat["characteristics"]}</p>'
        f'<p><strong>🎯 Business Opportunity / Role:</strong><br>{c_strat["role"]}</p>'
        f'<p><strong>📢 Recommended Marketing Strategy:</strong><br>{c_strat["marketing_strategy"]}</p>'
        f'<p><strong>🎁 Recommended Product & Offer Strategy:</strong><br>{c_strat["offer_strategy"]}</p>'
        f'<p><strong>🔒 Customer Retention Strategy:</strong><br>{c_strat["retention_strategy"]}</p>'
        f'<p><strong>🏆 Primary Business Objective:</strong><br>{c_strat["objective"]}</p>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📋 Executive Strategy Comparison Matrix")
    
    matrix_rows = []
    for c_id in sorted(CLUSTER_STRATEGY_INFO.keys()):
        info_c = CLUSTER_STRATEGY_INFO[c_id]
        stats_c = summary_stats[summary_stats['Cluster'] == c_id].iloc[0]
        matrix_rows.append({
            "Cluster": c_id,
            "Segment Name": info_c['name'],
            "Share (%)": f"{stats_c['Percentage']:.1f}% ({int(stats_c['Customer_Count'])})",
            "Avg Income": f"${stats_c['Mean_Income']:.1f}k",
            "Avg Spend": f"{stats_c['Mean_Spend']:.1f}",
            "Primary Business Role": info_c['role'].split('(')[0].strip(),
            "Core Objective": info_c['objective']
        })
    st.dataframe(pd.DataFrame(matrix_rows), use_container_width=True, hide_index=True)

# =========================================================
# SECTION 6: 📥 EXPORT & RAW DATA
# =========================================================
elif app_mode == "📥 Export & Raw Data":
    st.markdown('<div class="section-header">7. Segmented Customer Dataset & Export</div>', unsafe_allow_html=True)
    st.markdown("Search, filter, inspect, and export customer records.")
    
    tab_historical, tab_app_db = st.tabs(["📁 Historical Benchmark Dataset (Mall_Customers.csv)", "💾 Application Customers (Database)"])
    
    # TAB 1: HISTORICAL DATASET
    with tab_historical:
        st.markdown(f"Displaying **{len(df)}** historical benchmark training records:")
        
        all_segs = ["All Segments"] + sorted(df['Segment Name'].unique().tolist())
        seg_filter = st.selectbox("Filter Historical Data by Segment:", options=all_segs)
        
        if seg_filter != "All Segments":
            filtered_df = df[df['Segment Name'] == seg_filter]
        else:
            filtered_df = df
            
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Historical Segmented CSV",
            data=csv_bytes,
            file_name="segmented_customers_benchmark.csv",
            mime="text/csv",
            type="primary"
        )
        
    # TAB 2: APPLICATION CUSTOMERS FROM SQLITE
    with tab_app_db:
        app_customers = get_all_app_customers()
        if not app_customers:
            st.info("No new application customers have been saved to the SQLite database yet. Use 'Customer Lookup & Predictor' ➔ 'Add New Customer' to add records.")
        else:
            app_df = pd.DataFrame(app_customers)
            st.markdown(f"Displaying **{len(app_df)}** registered application customer records from `customer_segmentation.db`:")
            
            disp_cols = ['id', 'name', 'gender', 'age', 'annual_income', 'spending_score', 'cluster', 'segment_name', 'created_at']
            st.dataframe(app_df[disp_cols], use_container_width=True, hide_index=True)
            
            csv_app_bytes = app_df[disp_cols].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Application Customers CSV",
                data=csv_app_bytes,
                file_name="application_customers_database.csv",
                mime="text/csv",
                type="primary"
            )
