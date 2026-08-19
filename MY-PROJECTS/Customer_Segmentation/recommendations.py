"""
Strategic Recommendations Knowledge Base
Contains empirical business recommendations grounded strictly in the validated K=5 cluster statistics.
"""

CLUSTER_STRATEGY_INFO = {
    0: {
        "name": "Moderate-Income Moderate Spenders",
        "short_name": "Cluster 0: Moderate/Moderate",
        "cluster_id": 0,
        "color": "#3B82F6",
        "income_cat": "Moderate Income ($39k - $76k, Mean: $55.3k)",
        "spending_cat": "Moderate Spending (34 - 61, Mean: 49.5)",
        "characteristics": "Represents the central baseline of the customer base. Demonstrates balanced spending habits proportional to earnings with broad age representation (18-70 yrs, Mean: 42.7 yrs).",
        "role": "Volume & Stability Anchor (Provides steady foot traffic and reliable baseline revenue).",
        "marketing_strategy": "Consistent broad-reach promotional campaigns, seasonal retail events, and family shopping weekend promotions.",
        "offer_strategy": "Mid-tier product assortments, bundled product discounts, and seasonal shopping incentives.",
        "retention_strategy": "Standard points-based loyalty tier with achievable redemption thresholds to maintain repeat visit frequency.",
        "objective": "Protect visit frequency and maintain stable recurring baseline revenue."
    },
    1: {
        "name": "High-Income High Spenders",
        "short_name": "Cluster 1: High/High",
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
        "short_name": "Cluster 2: Low/High",
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
        "short_name": "Cluster 3: High/Low",
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
        "short_name": "Cluster 4: Low/Low",
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

def get_recommendation_for_cluster(cluster_id: int):
    """Retrieves the strategic recommendation payload for a given cluster ID."""
    return CLUSTER_STRATEGY_INFO.get(cluster_id, CLUSTER_STRATEGY_INFO[0])
