"""Explore sample retail sales with NumPy, Pandas, Matplotlib, and Seaborn."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def create_sales_data(seed: int = 42) -> pd.DataFrame:
    """Build a reproducible sample dataset for the analysis."""
    rng = np.random.default_rng(seed)
    row_count = 480
    month_numbers = rng.integers(0, 12, size=row_count)
    categories = rng.choice(
        ["Books", "Clothing", "Electronics", "Home"], size=row_count
    )
    seasonal_factors = np.array(
        [0.85, 0.82, 0.9, 0.95, 1.0, 1.05, 1.1, 1.08, 1.0, 1.12, 1.25, 1.4]
    )
    units = np.maximum(
        1,
        np.rint(rng.integers(8, 45, size=row_count) * seasonal_factors[month_numbers]),
    ).astype(int)
    unit_prices = np.select(
        [
            categories == "Books",
            categories == "Clothing",
            categories == "Electronics",
        ],
        [18.0, 55.0, 240.0],
        default=42.0,
    )
    unit_costs = np.select(
        [
            categories == "Books",
            categories == "Clothing",
            categories == "Electronics",
        ],
        [7.0, 24.0, 155.0],
        default=17.0,
    )
    discounts = rng.uniform(0, 0.2, size=row_count).round(2)
    revenue = units * unit_prices * (1 - discounts)
    profit = revenue - units * unit_costs
    months = pd.date_range("2025-01-01", periods=12, freq="MS")

    return pd.DataFrame(
        {
            "date": months.take(month_numbers),
            "store": rng.choice(["North", "Central", "South"], size=row_count),
            "category": categories,
            "units": units,
            "unit_price": unit_prices,
            "discount": discounts,
            "revenue": revenue.round(2),
            "profit": profit.round(2),
        }
    ).sort_values("date", ignore_index=True)


def print_sales_summary(sales: pd.DataFrame) -> None:
    """Display descriptive statistics and grouped Pandas summaries."""
    print("Sales data preview")
    print(sales.head().to_string(index=False))

    print("\nDescriptive statistics")
    print(sales[["units", "unit_price", "discount", "revenue", "profit"]].describe().round(2))

    category_summary = (
        sales.groupby("category", as_index=False)
        .agg(
            transactions=("revenue", "size"),
            units_sold=("units", "sum"),
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            average_discount=("discount", "mean"),
        )
        .sort_values("revenue", ascending=False)
    )
    print("\nPerformance by category")
    print(category_summary.round(2).to_string(index=False))

    monthly_summary = sales.groupby("date", as_index=False).agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
    )
    best_month = monthly_summary.loc[monthly_summary["revenue"].idxmax()]
    revenue_90th_percentile = np.percentile(sales["revenue"], 90)
    print(
        "\nBest month: "
        f"{best_month['date']:%B} (${best_month['revenue']:,.2f} revenue)"
    )
    print(f"90th percentile transaction revenue: ${revenue_90th_percentile:,.2f}")


def plot_sales(sales: pd.DataFrame) -> None:
    """Plot monthly trends, category totals, correlations, and transactions."""
    monthly_summary = sales.groupby("date", as_index=False).agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
    )
    category_summary = (
        sales.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )
    numeric_columns = ["units", "unit_price", "discount", "revenue", "profit"]

    sns.set_theme(style="whitegrid", palette="deep")
    figure, axes = plt.subplots(2, 2, figsize=(13, 9))

    sns.lineplot(
        data=monthly_summary,
        x="date",
        y="revenue",
        marker="o",
        color="#315e66",
        ax=axes[0, 0],
    )
    axes[0, 0].set(title="Monthly Revenue", xlabel="Month", ylabel="Revenue ($)")
    axes[0, 0].tick_params(axis="x", rotation=30)

    sns.barplot(
        data=category_summary,
        x="category",
        y="revenue",
        color="#6c9a8b",
        ax=axes[0, 1],
    )
    axes[0, 1].set(title="Revenue by Category", xlabel="Category", ylabel="Revenue ($)")

    sns.heatmap(
        sales[numeric_columns].corr(),
        annot=True,
        fmt=".2f",
        cmap="vlag",
        center=0,
        ax=axes[1, 0],
    )
    axes[1, 0].set_title("Sales Metric Correlations")

    sns.scatterplot(
        data=sales,
        x="units",
        y="revenue",
        hue="category",
        size="discount",
        sizes=(20, 120),
        alpha=0.75,
        ax=axes[1, 1],
    )
    axes[1, 1].set(title="Transaction Revenue", xlabel="Units Sold", ylabel="Revenue ($)")

    figure.suptitle("Retail Sales Analysis", fontsize=16, fontweight="bold")
    figure.tight_layout()
    plt.show()


def main() -> None:
    sales = create_sales_data()
    sales["order_value_band"] = np.where(
        sales["revenue"] >= 500, "High value", "Standard"
    )
    print_sales_summary(sales)
    print("\nTransactions by order value")
    print(sales["order_value_band"].value_counts().to_string())
    plot_sales(sales)


if __name__ == "__main__":
    main()