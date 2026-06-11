import numpy as np


def retrieve_similar_cases(
    index,
    data,
    context,
    top_k=5
):
    """
    Retrieve similar historical sales cases
    using FAISS similarity search.
    """

    # -----------------------------------
    # CREATE QUERY VECTOR
    # -----------------------------------

    query_vector = np.array([
        [
            context["current_sales"],
            context["avg_inventory"],
            context["avg_discount"],
            context["avg_marketing"]
        ]
    ]).astype("float32")

    # -----------------------------------
    # SEARCH IN FAISS
    # -----------------------------------

    distances, indices = index.search(
        query_vector,
        top_k
    )

    # -----------------------------------
    # FETCH ACTUAL ROWS
    # -----------------------------------

    similar_cases = []

    for idx in indices[0]:

        # Avoid invalid index
        if idx < len(data):

            case = data.iloc[idx].to_dict()

            similar_cases.append(case)

    return similar_cases