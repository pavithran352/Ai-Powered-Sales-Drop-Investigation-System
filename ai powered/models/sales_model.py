import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from src.data_loader import load_data


def train_sales_model():

    print("📥 Loading data...")

    df = load_data()

    print("🧠 Preparing features...")

    features = [
        "month",
        "day",
        "inventory",
        "competitor_discount",
        "marketing_spend",
        "demand_score"
    ]

    X = df[features]
    y = df["sales"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    print("🤖 Training sales model...")

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    print(f"✅ Sales Model MAE: {mae:.2f}")

    return model