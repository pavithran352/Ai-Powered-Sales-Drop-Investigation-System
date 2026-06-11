import pandas as pd

from src.data_loader import load_data

# CORE
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

# ML
from models.sales_model import (
    train_sales_model
)

from models.drop_model import (
    train_drop_model
)

from models.predict import ( train_drop_model
)

# RAG
from rag.rag_engine import (
    build_faiss_index
)

from rag.retriever import (
    retrieve_similar_cases
)

# AI (Gemini)
from ai.llm_gemini import (
    generate_ai_explanation
)

# SQL
from db.queries import (
    save_to_sql
)

# CONFIG
from config.config import (
    OUTPUT_PATH
)


def run_pipeline():

    print("=" * 50)
    print("🚀 AI SALES SYSTEM STARTED")
    print("=" * 50)

    # --------------------------------
    # LOAD DATA
    # --------------------------------
    print("\n📥 Loading data...")

    df = load_data()

    # --------------------------------
    # TRAIN MODELS
    # --------------------------------
    print("\n🤖 Training ML models...")

    sales_model = train_sales_model()
    drop_model = train_drop_model()

    # --------------------------------
    # PREDICTIONS
    # --------------------------------
    print("\n🔮 Running predictions...")

    df = predict_sales(
        df,
        sales_model
    )

    df = predict_drop(
        df,
        drop_model
    )

    # --------------------------------
    # DETECT SALES DROPS
    # --------------------------------
    print("\n📉 Detecting drops...")

    drop_cases = detect_sales_drop(df)

    # --------------------------------
    # BUILD FAISS INDEX
    # --------------------------------
    print("\n🔍 Building RAG...")

    index, vectors = (
        build_faiss_index(df)
    )

    results = []

    print("\n🧠 Generating insights...")

    # --------------------------------
    # LOOP THROUGH DROP CASES
    # --------------------------------
    for _, row in drop_cases.iterrows():

        region = row["region"]
        product = row["product"]

        print(
            f"\n⚠️ Investigating:"
            f" {product}"
        )

        # Context
        context = (
            get_problem_context(
                df,
                region,
                product
            )
        )

        # Recommendation
        suggestion = (
            suggest_substitution(
                df,
                product,
                region
            )
        )

        # Similar cases (RAG)
        retrieved_cases = (
            retrieve_similar_cases(
                index,
                vectors,
                context
            )
        )

        # AI Explanation
        ai_insight = (
            generate_ai_explanation(
                context,
                suggestion,
                retrieved_cases
            )
        )

        # Alert
        alert = generate_alert(
            row["drop_percentage"]
        )

        # Predicted sales
        predicted_sales = int(
            df[
                (
                    df["region"]
                    == region
                )
                &
                (
                    df["product"]
                    == product
                )
            ][
                "predicted_sales"
            ].mean()
        )

        results.append({
            "region": region,
            "problem_product": product,
            "suggested_product":
                suggestion["with"],

            "current_sales":
                context[
                    "current_sales"
                ],

            "predicted_sales":
                predicted_sales,

            "expected_sales":
                suggestion[
                    "expected_sales"
                ],

            "avg_inventory":
                context[
                    "avg_inventory"
                ],

            "drop_percentage":
                round(
                    row[
                        "drop_percentage"
                    ],
                    2
                ),

            "alert":
                alert,

            "ai_insight":
                ai_insight
        })

    # --------------------------------
    # CREATE OUTPUT
    # --------------------------------
    print("\n📊 Creating output...")

    output_df = pd.DataFrame(
        results
    )

    # Save CSV
    output_df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"✅ CSV saved:"
        f" {OUTPUT_PATH}"
    )

    # Save SQL
    save_to_sql(
        output_df,
        "sales_insights"
    )

    print(
        "✅ SQL saved:"
        " sales_insights"
    )

    print("\n🎉 PIPELINE COMPLETE")


if __name__ == "__main__":
    run_pipeline()