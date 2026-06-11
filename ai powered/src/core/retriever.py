def get_problem_context(
    df,
    region,
    product
):

    subset = df[
        (df["region"] == region)
        &
        (df["product"] == product)
    ]

    current_sales = int(
        subset["sales"].sum()
    )

    avg_inventory = round(
        subset["inventory"].mean(),
        2
    )

    avg_discount = round(
        subset[
            "competitor_discount"
        ].mean(),
        2
    )

    avg_marketing = round(
        subset[
            "marketing_spend"
        ].mean(),
        2
    )

    return {
        "current_sales": current_sales,
        "avg_inventory": avg_inventory,
        "avg_discount": avg_discount,
        "avg_marketing": avg_marketing
    }