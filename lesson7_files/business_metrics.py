"""
Business metrics calculation module for e-commerce EDA.

All functions are stateless: they accept DataFrames and return either
scalar values or DataFrames ready for display or plotting.
"""

import pandas as pd


def total_revenue(sales_data: pd.DataFrame) -> float:
    """Sum of the price column across all rows."""
    return sales_data["price"].sum()


def revenue_growth_rate(current: float, prior: float) -> float | None:
    """
    Percentage change from prior to current period as a decimal fraction.

    Returns None when prior is zero to avoid division by zero.
    """
    if prior == 0:
        return None
    return (current - prior) / prior


def monthly_revenue(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate revenue by month.

    Returns
    -------
    pd.DataFrame
        Columns: month (int), revenue (float).
    """
    return (
        sales_data.groupby("month")["price"]
        .sum()
        .reset_index(name="revenue")
    )


def monthly_growth_rate(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Month-over-month revenue growth rate.

    Returns
    -------
    pd.DataFrame
        Columns: month (int), mom_growth (float, decimal fraction).
        First month is NaN by definition.
    """
    return (
        sales_data.groupby("month")["price"]
        .sum()
        .pct_change()
        .reset_index(name="mom_growth")
    )


def average_order_value(sales_data: pd.DataFrame) -> float:
    """
    Average revenue per order.

    Sums item prices within each order, then averages across orders.
    """
    return sales_data.groupby("order_id")["price"].sum().mean()


def total_orders(sales_data: pd.DataFrame) -> int:
    """Count of distinct orders."""
    return sales_data["order_id"].nunique()


def revenue_by_category(
    sales_data: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    """
    Revenue broken down by product category, sorted descending.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with product_id and price columns.
    products : pd.DataFrame
        Products dataset with product_id and product_category_name.

    Returns
    -------
    pd.DataFrame
        Columns: product_category_name, revenue. Sorted descending by revenue.
    """
    merged = pd.merge(
        products[["product_id", "product_category_name"]],
        sales_data[["product_id", "price"]],
        on="product_id",
    )
    return (
        merged.groupby("product_category_name")["price"]
        .sum()
        .sort_values(ascending=False)
        .reset_index(name="revenue")
    )


def revenue_by_state(
    sales_data: pd.DataFrame,
    orders: pd.DataFrame,
    customers: pd.DataFrame,
) -> pd.DataFrame:
    """
    Revenue broken down by customer state, sorted descending.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with order_id and price columns.
    orders : pd.DataFrame
        Orders dataset with order_id and customer_id.
    customers : pd.DataFrame
        Customers dataset with customer_id and customer_state.

    Returns
    -------
    pd.DataFrame
        Columns: customer_state, revenue. Sorted descending by revenue.
    """
    with_customer = pd.merge(
        sales_data[["order_id", "price"]],
        orders[["order_id", "customer_id"]],
        on="order_id",
    )
    with_state = pd.merge(
        with_customer,
        customers[["customer_id", "customer_state"]],
        on="customer_id",
    )
    return (
        with_state.groupby("customer_state")["price"]
        .sum()
        .sort_values(ascending=False)
        .reset_index(name="revenue")
    )


def delivery_stats(sales_data: pd.DataFrame) -> dict:
    """
    Summary statistics for delivery speed.

    Returns
    -------
    dict
        Keys: mean_days, median_days, std_days (all floats).
    """
    speed = sales_data["delivery_speed"].dropna()
    return {
        "mean_days": speed.mean(),
        "median_days": speed.median(),
        "std_days": speed.std(),
    }


def _delivery_bucket(days: int) -> str:
    """Map delivery days to a named time bucket."""
    if days <= 3:
        return "1-3 days"
    if days <= 7:
        return "4-7 days"
    return "8+ days"


def review_score_by_delivery_bucket(
    sales_data: pd.DataFrame,
    reviews: pd.DataFrame,
) -> pd.DataFrame:
    """
    Average review score grouped by delivery speed bucket.

    Buckets: 1-3 days, 4-7 days, 8+ days.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with order_id and delivery_speed columns.
    reviews : pd.DataFrame
        Reviews dataset with order_id and review_score.

    Returns
    -------
    pd.DataFrame
        Columns: delivery_time, review_score. Ordered by delivery bucket.
    """
    merged = pd.merge(
        sales_data[["order_id", "delivery_speed"]].drop_duplicates("order_id"),
        reviews[["order_id", "review_score"]],
        on="order_id",
    )
    merged["delivery_time"] = merged["delivery_speed"].apply(_delivery_bucket)
    return (
        merged.groupby("delivery_time")["review_score"]
        .mean()
        .reindex(["1-3 days", "4-7 days", "8+ days"])
        .reset_index()
    )


def review_score_distribution(
    sales_data: pd.DataFrame,
    reviews: pd.DataFrame,
) -> pd.Series:
    """
    Normalized frequency of each review score (1-5) for orders in sales_data.

    Returns
    -------
    pd.Series
        Index: review_score (1-5), values: proportion (0-1).
    """
    merged = pd.merge(
        sales_data[["order_id"]].drop_duplicates(),
        reviews[["order_id", "review_score"]],
        on="order_id",
    )
    return merged["review_score"].value_counts(normalize=True).sort_index()


def average_review_score(sales_data: pd.DataFrame, reviews: pd.DataFrame) -> float:
    """Overall average review score for orders in the sales dataset."""
    merged = pd.merge(
        sales_data[["order_id"]].drop_duplicates(),
        reviews[["order_id", "review_score"]],
        on="order_id",
    )
    return merged["review_score"].mean()


def order_status_distribution(orders: pd.DataFrame, year: int | None = None) -> pd.Series:
    """
    Proportion of orders by status, optionally filtered by year.

    Parameters
    ----------
    orders : pd.DataFrame
        Full orders dataset with order_status and year columns.
    year : int, optional
        If provided, restrict to orders from this year only.

    Returns
    -------
    pd.Series
        Index: order_status, values: proportion (0-1). Sorted descending.
    """
    if year is not None:
        orders = orders[orders["year"] == year]
    return orders["order_status"].value_counts(normalize=True)
