import pandas as pd


def predict_sales(df, model):

    features = [
        "month",
        "day",
        "inventory",
        "competitor_discount",
        "marketing_spend",
        "demand_score"
    ]

    df["predicted_sales"] = model.predict(
        df[features]
    )

    return df


def predict_drop(df, model):

    features = [
        "month",
        "inventory",
        "competitor_discount",
        "marketing_spend",
        "demand_score"
    ]

    df["drop_prediction"] = model.predict(
        df[features]
    )

    return df