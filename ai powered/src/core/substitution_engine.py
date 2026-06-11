def suggest_substitution(
    df,
    problem_product,
    region
):

    region_df = df[
        df["region"] == region
    ]

    product_sales = (
        region_df
        .groupby("product")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    # Remove weak product
    product_sales = product_sales.drop(
        problem_product,
        errors="ignore"
    )

    best_product = product_sales.index[0]

    expected_sales = int(
        product_sales.iloc[0]
    )

    return {
        "replace": problem_product,
        "with": best_product,
        "expected_sales": expected_sales
    }