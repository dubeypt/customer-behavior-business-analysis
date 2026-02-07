"""
Data Visualization for Real E-Commerce Customer Analysis
Author: Aditya Dubey
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Load REAL data
transactions = pd.read_csv('transactions_clean.csv')
segments = pd.read_csv('customer_segments.csv')

transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])

# =================================================================
# DASHBOARD 1: BUSINESS OVERVIEW
# =================================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# 1. Monthly Revenue Trend
transactions['year_month'] = transactions['transaction_date'].dt.to_period('M')
monthly_revenue = transactions.groupby('year_month')['revenue'].sum()
monthly_revenue.index = monthly_revenue.index.to_timestamp()

axes[0, 0].plot(monthly_revenue.index, monthly_revenue.values, marker='o')
axes[0, 0].set_title('Monthly Revenue Trend')
axes[0, 0].set_xlabel('Month')
axes[0, 0].set_ylabel('Revenue')
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. Revenue by Country
country_revenue = transactions.groupby('Country')['revenue'].sum().sort_values(ascending=False).head(10)
axes[0, 1].barh(country_revenue.index, country_revenue.values)
axes[0, 1].set_title('Top 10 Countries by Revenue')
axes[0, 1].set_xlabel('Revenue')

# 3. Customer Segment Distribution
segment_counts = segments['segment'].value_counts()
axes[1, 0].bar(segment_counts.index, segment_counts.values)
axes[1, 0].set_title('Customer Segmentation (RFM)')
axes[1, 0].tick_params(axis='x', rotation=30)

# 4. CLV by Segment
segment_clv = segments.groupby('segment')['monetary'].mean().sort_values()
axes[1, 1].barh(segment_clv.index, segment_clv.values)
axes[1, 1].set_title('Average Customer Value by Segment')

plt.suptitle('E-Commerce Business Dashboard', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('customer_analysis_dashboard.png', dpi=300)
plt.close()

print("✓ Saved: customer_analysis_dashboard.png")

# =================================================================
# DASHBOARD 2: RFM DEEP DIVE
# =================================================================
fig2, axes2 = plt.subplots(2, 2, figsize=(16, 10))

rfm_metrics = segments.groupby('segment').agg({
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': 'mean',
    'customer_id': 'count'
}).round(2)

axes2[0, 0].bar(rfm_metrics.index, rfm_metrics['recency'])
axes2[0, 0].set_title('Avg Recency (Lower is Better)')
axes2[0, 0].tick_params(axis='x', rotation=30)

axes2[0, 1].bar(rfm_metrics.index, rfm_metrics['frequency'])
axes2[0, 1].set_title('Avg Frequency')
axes2[0, 1].tick_params(axis='x', rotation=30)

axes2[1, 0].bar(rfm_metrics.index, rfm_metrics['monetary'])
axes2[1, 0].set_title('Avg Monetary Value')
axes2[1, 0].tick_params(axis='x', rotation=30)

axes2[1, 1].scatter(
    rfm_metrics['customer_id'],
    rfm_metrics['monetary'],
    s=200
)
for seg in rfm_metrics.index:
    axes2[1, 1].annotate(
        seg,
        (rfm_metrics.loc[seg, 'customer_id'], rfm_metrics.loc[seg, 'monetary'])
    )

axes2[1, 1].set_title('Segment Size vs Value')
axes2[1, 1].set_xlabel('Customer Count')
axes2[1, 1].set_ylabel('Total Revenue')

plt.suptitle('Customer Segmentation Deep Dive', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('segment_analysis.png', dpi=300)
plt.close()

print("Saved: segment_analysis.png")
print(" All REAL-DATA visualizations created successfully!")
