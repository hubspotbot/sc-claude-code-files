# E-Commerce Sales Analysis

Exploratory data analysis of e-commerce transaction data covering orders, products, customers, and reviews.

## Project Structure

```
lesson7_files/
├── EDA_Refactored.ipynb   # Main analysis notebook
├── data_loader.py          # Data loading and preprocessing functions
├── business_metrics.py     # Business metric calculation functions
├── requirements.txt        # Python dependencies
└── ecommerce_data/         # Raw CSV datasets
    ├── orders_dataset.csv
    ├── order_items_dataset.csv
    ├── products_dataset.csv
    ├── customers_dataset.csv
    └── order_reviews_dataset.csv
```

## Setup

```bash
pip install -r requirements.txt
```

## Running the Analysis

Open `EDA_Refactored.ipynb` in Jupyter and run all cells.

To analyze a different time period, edit the configuration at the top of the notebook:

```python
ANALYSIS_YEAR   = 2023   # Primary year of analysis
COMPARISON_YEAR = 2022   # Baseline year for year-over-year comparisons
ANALYSIS_MONTH  = None   # Set to 1-12 for a single month, or None for the full year
```

Re-run all cells after changing these values. All metrics, charts, and labels will update automatically.

## Modules

### `data_loader.py`

Handles all I/O and initial preprocessing. Key functions:

| Function | Description |
|----------|-------------|
| `load_all(data_dir)` | Load all five datasets and return as a dict |
| `build_sales_data(orders, order_items)` | Merge order items with order metadata |
| `filter_delivered(sales_data)` | Keep only delivered orders |
| `filter_by_period(sales_data, year, month)` | Filter to a specific year and/or month |
| `compute_delivery_speed(sales_data)` | Add delivery_speed column (days) |

### `business_metrics.py`

Stateless calculation functions. Key functions:

| Function | Description |
|----------|-------------|
| `total_revenue(sales_data)` | Sum of item prices |
| `revenue_growth_rate(current, prior)` | Percentage change as a decimal |
| `monthly_revenue(sales_data)` | Revenue aggregated by month |
| `monthly_growth_rate(sales_data)` | Month-over-month growth rates |
| `average_order_value(sales_data)` | Mean revenue per order |
| `total_orders(sales_data)` | Count of distinct orders |
| `revenue_by_category(sales_data, products)` | Revenue per product category |
| `revenue_by_state(sales_data, orders, customers)` | Revenue per customer state |
| `delivery_stats(sales_data)` | Mean, median, std of delivery days |
| `review_score_by_delivery_bucket(sales_data, reviews)` | Avg review score by delivery speed |
| `review_score_distribution(sales_data, reviews)` | Normalized review score frequencies |
| `order_status_distribution(orders, year)` | Proportion of orders by status |

## Analyses Included

1. **Revenue Metrics** - Total revenue, order count, and average order value vs. prior period
2. **Monthly Trend** - Monthly revenue bars and month-over-month growth rates
3. **Product Analysis** - Revenue breakdown by product category
4. **Geographic Analysis** - Revenue by customer state (choropleth map)
5. **Delivery Performance** - Mean and median delivery time
6. **Customer Satisfaction** - Review scores by delivery speed bucket and overall distribution
7. **Order Status** - Proportion of orders by fulfillment status
