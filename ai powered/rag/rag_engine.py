import faiss
import numpy as np


def build_faiss_index(df):

    print("🔍 Building FAISS index...")

    vectors = df[
        [
            "sales",
            "inventory",
            "competitor_discount",
            "marketing_spend"
        ]
    ].values.astype("float32")

    index = faiss.IndexFlatL2(
        vectors.shape[1]
    )

    index.add(vectors)

    print("✅ FAISS index ready")

    return index, vectors