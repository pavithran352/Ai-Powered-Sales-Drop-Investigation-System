import pandas as pd
import numpy as np

from config.config import *
from db.queries import save_to_sql


def preprocess_data():

    print("📥 Loading Kaggle dataset...")

    train_df = pd.read_csv(RAW_DATA_PATH)
    stores_df = pd.read_csv(STORES_PATH)

    print("🔗 Merging store info...")

    df = train_df.merge(
        stores_df,
        on="store_nbr",
        how="left"
    )

    # Rename columns
    df.rename(columns={
        "store_nbr": "region",
        "family": "product"
    }, inplace=True)

    # Convert date
    df["date"] = pd.to_datetime(df["date"])

    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["day"] = df["date"].dt.day
    df["weekday"] = df["date"].dt.day_name()

    print("🧠 Creating synthetic features...")

    # inventory
    df["inventory"] = np.random.randint(
        50, 200, len(df)
    )

    # competitor discount
    df["competitor_discount"] = np.random.choice(
        [0, 10, 20, 30],
        len(df)
    )

    # marketing spend
    df["marketing_spend"] = np.random.randint(
        1000,
        10000,
        len(df)
    )

    # demand score
    df["demand_score"] = np.random.uniform(
        0.5,
        1.5,
        len(df)
    )

    print("📉 Injecting demo sales drop...")

    drop_condition = (
        (df["month"] == 6)
        & (df["region"] == 1)
        & (df["product"] == "AUTOMOTIVE")
    )

    df.loc[drop_condition, "sales"] *= 0.4

    print("💾 Saving processed dataset...")

    df.to_csv(
        PROCESSED_DATA_PATH,
        index=False
    )

    print("🗄 Saving to SQL...")
    df = df.head(1000)

    save_to_sql(df, "sales_data")

    print("✅ Preprocessing completed!")


if __name__ == "__main__":
    preprocess_data()