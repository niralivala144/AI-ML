import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.prediction import CLUSTER_NAMES, CLUSTER_COLORS, SEGMENT_NAME_TO_COLOR

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORICAL_DATA_PATH = os.path.join(BASE_DIR, "outputs", "segmented_customers.csv")
ORIGINAL_DATA_PATH = os.path.join(BASE_DIR, "Mall_Customers.csv")

def load_benchmark_data():
    """Loads historical benchmark training dataset."""
    if os.path.exists(HISTORICAL_DATA_PATH):
        return pd.read_csv(HISTORICAL_DATA_PATH)
    elif os.path.exists(ORIGINAL_DATA_PATH):
        df = pd.read_csv(ORIGINAL_DATA_PATH)
        df['Cluster'] = 0
        df['Segment Name'] = CLUSTER_NAMES[0]
        return df
    return pd.DataFrame()

def calculate_cluster_summary(df):
    """Calculates cluster aggregation metrics dynamically."""
    if df.empty:
        return pd.DataFrame()
        
    summary = df.groupby(['Cluster', 'Segment Name']).agg(
        Customer_Count=('CustomerID' if 'CustomerID' in df.columns else 'id', 'count'),
        Mean_Income=('Annual Income (k$)' if 'Annual Income (k$)' in df.columns else 'annual_income', 'mean'),
        Median_Income=('Annual Income (k$)' if 'Annual Income (k$)' in df.columns else 'annual_income', 'median'),
        Min_Income=('Annual Income (k$)' if 'Annual Income (k$)' in df.columns else 'annual_income', 'min'),
        Max_Income=('Annual Income (k$)' if 'Annual Income (k$)' in df.columns else 'annual_income', 'max'),
        Mean_Spend=('Spending Score (1-100)' if 'Spending Score (1-100)' in df.columns else 'spending_score', 'mean'),
        Median_Spend=('Spending Score (1-100)' if 'Spending Score (1-100)' in df.columns else 'spending_score', 'median'),
        Min_Spend=('Spending Score (1-100)' if 'Spending Score (1-100)' in df.columns else 'spending_score', 'min'),
        Max_Spend=('Spending Score (1-100)' if 'Spending Score (1-100)' in df.columns else 'spending_score', 'max'),
        Mean_Age=('Age' if 'Age' in df.columns else 'age', 'mean'),
        Median_Age=('Age' if 'Age' in df.columns else 'age', 'median')
    ).reset_index()
    
    total = summary['Customer_Count'].sum()
    summary['Percentage'] = (summary['Customer_Count'] / total) * 100.0 if total > 0 else 0
    return summary.sort_values(by='Cluster')

def plot_segment_bar_chart(summary_df):
    """Plots interactive bar chart for customer headcount by segment."""
    bar_df = summary_df.sort_values(by='Customer_Count', ascending=False)
    fig = px.bar(
        bar_df,
        x='Segment Name',
        y='Customer_Count',
        color='Segment Name',
        color_discrete_map=SEGMENT_NAME_TO_COLOR,
        text=bar_df.apply(lambda r: f"{r['Customer_Count']} ({r['Percentage']:.1f}%)", axis=1),
        labels={'Customer_Count': 'Customer Count', 'Segment Name': 'Customer Segment'},
        title='Customer Headcount & Share by Segment'
    )
    fig.update_layout(
        showlegend=False,
        height=380,
        xaxis_tickangle=-20,
        margin=dict(l=20, r=20, t=40, b=60)
    )
    fig.update_traces(textposition='outside')
    return fig

def plot_segment_donut_chart(summary_df):
    """Plots clean donut chart without overlapping labels."""
    fig = px.pie(
        summary_df,
        names='Segment Name',
        values='Customer_Count',
        color='Segment Name',
        color_discrete_map=SEGMENT_NAME_TO_COLOR,
        hole=0.55,
        title='Segment Share (Hover for Details)'
    )
    fig.update_traces(
        textinfo='percent',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>',
        textfont_size=13
    )
    fig.update_layout(
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5, font=dict(size=10)),
        margin=dict(l=10, r=10, t=40, b=50)
    )
    return fig

def plot_behavioral_scatter(df, live_df=None):
    """Plots 2D Income vs Spending scatter plot with centroids and optional live customer points."""
    income_col = 'Annual Income (k$)' if 'Annual Income (k$)' in df.columns else 'annual_income'
    spend_col = 'Spending Score (1-100)' if 'Spending Score (1-100)' in df.columns else 'spending_score'
    
    centroids_df = df.groupby(['Cluster', 'Segment Name'])[[income_col, spend_col]].mean().reset_index()
    
    fig = px.scatter(
        df,
        x=income_col,
        y=spend_col,
        color='Segment Name',
        color_discrete_map=SEGMENT_NAME_TO_COLOR,
        hover_data=['CustomerID', 'Gender', 'Age', income_col, spend_col, 'Cluster', 'Segment Name'] if 'CustomerID' in df.columns else [income_col, spend_col, 'Segment Name'],
        title='Customer Behavioral Clusters (Income vs. Spending Propensity)',
        labels={income_col: 'Annual Income (k$)', spend_col: 'Spending Score (1-100)'}
    )
    
    # Overlay Centroid X markers
    fig.add_trace(
        go.Scatter(
            x=centroids_df[income_col],
            y=centroids_df[spend_col],
            mode='markers+text',
            marker=dict(symbol='x', size=16, color='white', line=dict(width=2, color='black')),
            text=centroids_df['Cluster'].apply(lambda c: f"Centroid {c}"),
            textposition="top center",
            name='Cluster Centroids',
            hovertemplate='<b>Centroid %{text}</b><br>Income: $%{x:.1f}k<br>Spending: %{y:.1f}<extra></extra>'
        )
    )
    
    # If live registered customers exist, overlay them as glowing stars
    if live_df is not None and not live_df.empty:
        fig.add_trace(
            go.Scatter(
                x=live_df['annual_income'],
                y=live_df['spending_score'],
                mode='markers',
                marker=dict(symbol='star', size=14, color='#F43F5E', line=dict(width=1.5, color='white')),
                name='Live App Customers',
                text=live_df['name'],
                hovertemplate='<b>Live Customer: %{text}</b><br>Income: $%{x}k<br>Spending: %{y}<extra></extra>'
            )
        )
        
    fig.update_traces(marker=dict(size=10, opacity=0.88, line=dict(width=0.5, color='#1F2937')), selector=dict(mode='markers'))
    fig.update_layout(
        height=550,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=50, b=90)
    )
    return fig

def plot_centroids_standalone(df):
    """Plots standalone centroid map."""
    income_col = 'Annual Income (k$)' if 'Annual Income (k$)' in df.columns else 'annual_income'
    spend_col = 'Spending Score (1-100)' if 'Spending Score (1-100)' in df.columns else 'spending_score'
    centroids_df = df.groupby(['Cluster', 'Segment Name'])[[income_col, spend_col]].mean().reset_index()
    
    fig = go.Figure()
    for idx, row in centroids_df.iterrows():
        c_name = row['Segment Name']
        c_color = SEGMENT_NAME_TO_COLOR.get(c_name, '#3B82F6')
        c_id = int(row['Cluster'])
        
        fig.add_trace(go.Scatter(
            x=[row[income_col]],
            y=[row[spend_col]],
            mode='markers+text',
            marker=dict(size=22, color=c_color, line=dict(width=2, color='white')),
            name=f"Cluster {c_id}: {c_name}",
            text=[f"Cluster {c_id}<br>(${row[income_col]:.1f}k, {row[spend_col]:.1f})"],
            textposition="top center",
            hovertemplate=f"<b>Cluster {c_id}: {c_name}</b><br>Mean Income: ${row[income_col]:.1f}k<br>Mean Spending: {row[spend_col]:.1f}<extra></extra>"
        ))
        
    fig.update_layout(
        title='Cluster Centroid Coordinates (Mean Income vs. Mean Spending)',
        xaxis=dict(title='Annual Income (k$)', range=[10, 110]),
        yaxis=dict(title='Spending Score (1-100)', range=[0, 105]),
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=50, b=80)
    )
    return fig

def plot_boxplots(df):
    """Plots Income and Spending boxplots by cluster."""
    income_col = 'Annual Income (k$)' if 'Annual Income (k$)' in df.columns else 'annual_income'
    spend_col = 'Spending Score (1-100)' if 'Spending Score (1-100)' in df.columns else 'spending_score'
    
    mean_inc = df[income_col].mean()
    mean_spd = df[spend_col].mean()
    
    fig_inc = px.box(
        df,
        x='Segment Name',
        y=income_col,
        color='Segment Name',
        color_discrete_map=SEGMENT_NAME_TO_COLOR,
        title='Annual Income Boxplot by Segment',
        labels={income_col: 'Annual Income (k$)', 'Segment Name': 'Segment'}
    )
    fig_inc.add_hline(y=mean_inc, line_dash="dash", line_color="#F87171", annotation_text=f"Mean (${mean_inc:.1f}k)")
    fig_inc.update_layout(showlegend=False, xaxis_tickangle=-25, height=400)
    
    fig_spd = px.box(
        df,
        x='Segment Name',
        y=spend_col,
        color='Segment Name',
        color_discrete_map=SEGMENT_NAME_TO_COLOR,
        title='Spending Score Boxplot by Segment',
        labels={spend_col: 'Spending Score (1-100)', 'Segment Name': 'Segment'}
    )
    fig_spd.add_hline(y=mean_spd, line_dash="dash", line_color="#F87171", annotation_text=f"Mean ({mean_spd:.1f})")
    fig_spd.update_layout(showlegend=False, xaxis_tickangle=-25, height=400)
    
    return fig_inc, fig_spd
