"""
Real E-Commerce Dataset (Transactional Data)
Author: Aditya Dubey
"""

import pandas as pd
from datetime import timedelta

print("="*80)
print("SQL-ANALYSIS  (REAL DATA)")
print("="*80)

# ------------------------------------------------------------------
# Load REAL datasets
# ------------------------------------------------------------------
transactions = pd.read_csv('transactions_clean.csv')
segments = pd.read_csv('customer_segments.csv')

transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])

print("\n" + "="*80)
print("COMMON QUESTIONS WITH PANDAS SOLUTIONS")
print("="*80)

# ===================================================================
# Q1: Top 10 customers by total revenue
# ===================================================================
print("\nQ1: Top 10 customers by total revenue")

print("""
SQL:
SELECT customer_id,
       SUM(revenue) AS total_revenue,
       COUNT(DISTINCT Invoice) AS total_orders
FROM transactions
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 10;
""")

top_customers = (
    transactions.groupby('customer_id')
    .agg(
        total_revenue=('revenue', 'sum'),
        total_orders=('Invoice', 'nunique')
    )
    .sort_values('total_revenue', ascending=False)
    .head(10)
)

print(top_customers)

# ===================================================================
# Q2: Month-over-month revenue growth
# ===================================================================
print("\nQ2: Month-over-Month revenue growth")

monthly_rev = (
    transactions
    .groupby(transactions['transaction_date'].dt.to_period('M'))['revenue']
    .sum()
    .reset_index()
)

monthly_rev.columns = ['month', 'revenue']
monthly_rev['prev_month_revenue'] = monthly_rev['revenue'].shift(1)
monthly_rev['growth_rate_%'] = (
    (monthly_rev['revenue'] - monthly_rev['prev_month_revenue']) /
    monthly_rev['prev_month_revenue'] * 100
).round(2)

print(monthly_rev.tail(6))

# ===================================================================
# Q3: Customer activity by quarter (cohort-style without signup date)
# ===================================================================
print("\nQ3: Customer activity trend by quarter")

transactions['quarter'] = transactions['transaction_date'].dt.to_period('Q')

quarterly_activity = (
    transactions.groupby('quarter')['customer_id']
    .nunique()
    .reset_index(name='active_customers')
)

print(quarterly_activity.tail())

# ===================================================================
# Q4: Frequently co-purchased products (market basket logic)
# ===================================================================
print("\nQ4: Products frequently purchased together")

# Products per invoice
invoice_products = (
    transactions.groupby('Invoice')['Description']
    .apply(list)
)

pairs = []
for products in invoice_products:
    unique_products = list(set(products))
    if len(unique_products) > 1:
        for i in range(len(unique_products)):
            for j in range(i + 1, len(unique_products)):
                pairs.append(tuple(sorted([unique_products[i], unique_products[j]])))

pair_counts = pd.Series(pairs).value_counts().head(10)

print("\nTop Product Pairs:")
for (p1, p2), count in pair_counts.items():
    print(f"{p1} + {p2}: {count} orders")

# ===================================================================
# Q5: Customers at risk of churn (no purchase in last 90 days)
# ===================================================================
print("\nQ5: Customers at risk of churn (>90 days inactivity)")

analysis_date = transactions['transaction_date'].max() + timedelta(days=1)

last_purchase = (
    transactions.groupby('customer_id')
    .agg(
        last_purchase_date=('transaction_date', 'max'),
        total_orders=('Invoice', 'nunique'),
        lifetime_value=('revenue', 'sum')
    )
    .reset_index()
)

last_purchase['days_since_purchase'] = (
    analysis_date - last_purchase['last_purchase_date']
).dt.days

at_risk_customers = last_purchase[last_purchase['days_since_purchase'] > 90] \
    .sort_values('lifetime_value', ascending=False)

print(f"Customers at risk: {len(at_risk_customers)}")
print(at_risk_customers.head(10))

# ===================================================================
# Q6: Average order value by customer segment
# ===================================================================
print("\nQ6: AOV by customer segment")

trans_with_segment = transactions.merge(
    segments[['customer_id', 'segment']],
    on='customer_id',
    how='left'
)

segment_kpis = (
    trans_with_segment.groupby('segment')
    .agg(
        customer_count=('customer_id', 'nunique'),
        total_orders=('Invoice', 'nunique'),
        avg_order_value=('revenue', 'mean'),
        total_revenue=('revenue', 'sum')
    )
    .round(2)
)

segment_kpis['revenue_per_customer'] = (
    segment_kpis['total_revenue'] / segment_kpis['customer_count']
).round(2)

print(segment_kpis.sort_values('revenue_per_customer', ascending=False))

# ===================================================================
# Q7: Running total revenue (window function)
# ===================================================================
print("\nQ7: Running total revenue by month")

monthly_running = monthly_rev[['month', 'revenue']].copy()
monthly_running['running_total'] = monthly_running['revenue'].cumsum()

print(monthly_running.tail(12))

# ===================================================================
# SUMMARY
# ===================================================================
print("\n" + "="*80)
print("SQL CONCEPTS DEMONSTRATED")
print("="*80)

print("""
 GROUP BY, SUM, COUNT, AVG
  DISTINCT counts
  Date-based aggregation (MONTH, QUARTER)
  Window functions (LAG, RUNNING TOTAL)
  Cohort-style analysis
  Market basket logic
  JOINs (transactions + segments)
  Churn detection logic
  Revenue ranking & sorting

""")

print("\nANALYSIS COMPLETE ")
print("="*80)
