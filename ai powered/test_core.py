from src.data_loader import load_data

from src.core.drop_detector import (
    detect_sales_drop
)

from src.core.substitution_engine import (
    suggest_substitution
)

from src.core.retriever import (
    get_problem_context
)

from src.core.alert_system import (
    generate_alert
)


print("📥 Loading data")

df = load_data()

print("📉 Detecting drops")

drops = detect_sales_drop(df)

print(drops.head())

if len(drops) > 0:

    first_case = drops.iloc[0]

    region = first_case["region"]
    product = first_case["product"]

    print(
        f"\n🔍 Problem Product:"
        f" {product}"
    )

    context = get_problem_context(
        df,
        region,
        product
    )

    suggestion = suggest_substitution(
        df,
        product,
        region
    )

    alert = generate_alert(
        first_case[
            "drop_percentage"
        ]
    )

    print("\n🚨 ALERT:")
    print(alert)

    print("\n📊 CONTEXT:")
    print(context)

    print("\n🔁 SUGGESTION:")
    print(suggestion)