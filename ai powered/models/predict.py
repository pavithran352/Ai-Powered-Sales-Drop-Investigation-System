import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from src.data_loader import load_data


def train_drop_model():

    print("📥 Loading data...")

    df = load_data()

    print("📉 Creating drop labels...")

    df["prev_sales"] = (
        df.groupby(
            ["region", "product"]
        )["sales"]
        .shift(1)
    )

    df["drop_flag"] = (
        df["sales"]
        <
        df["prev_sales"] * 0.8
    ).astype(int)

    df.dropna(inplace=True)

    features = [
        "month",
        "inventory",
        "competitor_discount",
        "marketing_spend",
        "demand_score"
    ]

    X = df[features]
    y = df["drop_flag"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    print("🤖 Training drop model...")

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print(f"✅ Drop Model Accuracy: {accuracy:.2f}")

    return model