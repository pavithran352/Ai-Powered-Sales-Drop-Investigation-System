import pandas as pd


def detect_sales_drop(df):

    print("📉 Detecting sales drop...")

    monthly_sales = (
        df.groupby(
            ["region", "product", "month"]
        )["sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["prev_sales"] = (
        monthly_sales
        .groupby(["region", "product"])["sales"]
        .shift(1)
    )

    monthly_sales["drop_percentage"] = (
        (
            monthly_sales["prev_sales"]
            -
            monthly_sales["sales"]
        )
        /
        monthly_sales["prev_sales"]
    ) * 100

    drops = monthly_sales[
        monthly_sales["drop_percentage"] > 20
    ]

    return drops