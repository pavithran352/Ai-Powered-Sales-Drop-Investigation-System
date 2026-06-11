import pandas as pd
from .connection import get_engine


def save_to_sql(df, table_name):
    try:
        print("🔌 Connecting to MySQL...")

        engine = get_engine()

        print("✅ Connected to DB")
        print(f"📤 Uploading {len(df)} rows to '{table_name}'...")

        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False,
            chunksize=1000,   # inserts in batches
            method="multi"    # faster insertion
        )

        print("✅ Data saved successfully!")

    except Exception as e:
        print("❌ SQL Error:")
        print(e)