"""
Data loading and preprocessing module for e-commerce EDA.

All I/O and initial data cleaning lives here so that analysis
notebooks stay focused on business logic.
"""

import pandas as pd
from pathlib import Path


_TIMESTAMP_COLS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


def load_orders(data_dir: str | Path) -> pd.DataFrame:
    """
    Load and parse the orders dataset.

    Converts all timestamp columns to datetime and extracts
    year and month from order_purchase_timestamp for grouping.

    Parameters
    ----------
    data_dir : str or Path
        Directory containing the raw CSV files.

    Returns
    -------
    pd.DataFrame
        Orders with parsed timestamps and year/month columns.
    """
    df = pd.read_csv(Path(data_dir) / "orders_dataset.csv")
    for col in _TIMESTAMP_COLS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    df["year"] = df["order_purchase_timestamp"].dt.year
    df["month"] = df["order_purchase_timestamp"].dt.month
    return df


def load_order_items(data_dir: str | Path) -> pd.DataFrame:
    """Load the order items dataset."""
    return pd.read_csv(Path(data_dir) / "order_items_dataset.csv")


def load_products(data_dir: str | Path) -> pd.DataFrame:
    """Load the products dataset."""
    return pd.read_csv(Path(data_dir) / "products_dataset.csv")


def load_customers(data_dir: str | Path) -> pd.DataFrame:
    """Load the customers dataset."""
    return pd.read_csv(Path(data_dir) / "customers_dataset.csv")


def load_reviews(data_dir: str | Path) -> pd.DataFrame:
    """Load the order reviews dataset."""
    return pd.read_csv(Path(data_dir) / "order_reviews_dataset.csv")


def load_all(data_dir: str | Path) -> dict[str, pd.DataFrame]:
    """
    Load all datasets and return as a dictionary.

    Parameters
    ----------
    data_dir : str or Path
        Directory containing the raw CSV files.

    Returns
    -------
    dict
        Keys: orders, order_items, products, customers, reviews.
    """
    return {
        "orders": load_orders(data_dir),
        "order_items": load_order_items(data_dir),
        "products": load_products(data_dir),
        "customers": load_customers(data_dir),
        "reviews": load_reviews(data_dir),
    }


def build_sales_data(orders: pd.DataFrame, order_items: pd.DataFrame) -> pd.DataFrame:
    """
    Merge order items with order metadata into a flat sales dataset.

    Parameters
    ----------
    orders : pd.DataFrame
        Output of load_orders().
    order_items : pd.DataFrame
        Output of load_order_items().

    Returns
    -------
    pd.DataFrame
        One row per order line item with order-level metadata attached.
    """
    return pd.merge(
        order_items[["order_id", "order_item_id", "product_id", "price", "freight_value"]],
        orders[[
            "order_id", "customer_id", "order_status",
            "order_purchase_timestamp", "order_delivered_customer_date",
            "year", "month",
        ]],
        on="order_id",
    )


def filter_delivered(sales_data: pd.DataFrame) -> pd.DataFrame:
    """Return only rows where the order status is delivered."""
    return sales_data[sales_data["order_status"] == "delivered"].copy()


def filter_by_period(
    sales_data: pd.DataFrame,
    year: int | None = None,
    month: int | None = None,
) -> pd.DataFrame:
    """
    Filter the sales dataset to a specific year and/or month.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with year and month columns.
    year : int, optional
        Calendar year to keep. If None, all years are included.
    month : int, optional
        Calendar month (1-12) to keep. If None, all months are included.

    Returns
    -------
    pd.DataFrame
        Filtered copy of the input.
    """
    result = sales_data
    if year is not None:
        result = result[result["year"] == year]
    if month is not None:
        result = result[result["month"] == month]
    return result.copy()


def compute_delivery_speed(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Add a delivery_speed column representing calendar days from purchase to delivery.

    Parameters
    ----------
    sales_data : pd.DataFrame
        Sales data with order_purchase_timestamp and
        order_delivered_customer_date columns.

    Returns
    -------
    pd.DataFrame
        Copy of input with delivery_speed (int) column added.
    """
    df = sales_data.copy()
    df["delivery_speed"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days
    return df
