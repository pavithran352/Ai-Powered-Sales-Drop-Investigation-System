import streamlit as st
import sys
import os
import traceback

# -----------------------------------
# ADD ROOT PATH
# -----------------------------------

ROOT_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if ROOT_PATH not in sys.path:
    sys.path.insert(0, ROOT_PATH)

# -----------------------------------
# IMPORTS
# -----------------------------------

from src.data_loader import load_data

from src.core.retriever import (
    get_problem_context
)

from src.core.substitution_engine import (
    suggest_substitution
)

from rag.rag_engine import (
    build_faiss_index
)

from rag.retriever import (
    retrieve_similar_cases
)

from ai.llm_gemini import (
    generate_ai_explanation
)

# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="AI Sales Investigation",
    layout="wide"
)

st.title(
    "🚀 AI Sales Drop Investigation System"
)

st.write(
    "Ask AI why sales dropped and get business recommendations."
)

# ----------------------------------
# LOAD DATA
# ----------------------------------

@st.cache_data
def get_data():
    return load_data()


df = get_data()

# ----------------------------------
# BUILD FAISS INDEX
# ----------------------------------

@st.cache_resource
def get_rag():

    st.write(
        "🔄 Building FAISS index..."
    )

    index, vectors = (
        build_faiss_index(df)
    )

    st.success(
        "✅ FAISS index ready"
    )

    return index


index = get_rag()

# ----------------------------------
# SIDEBAR FILTERS
# ----------------------------------

st.sidebar.header(
    "Filters"
)

regions = sorted(
    df["region"].dropna().unique()
)

products = sorted(
    df["product"].dropna().unique()
)

selected_region = (
    st.sidebar.selectbox(
        "Select Region",
        regions
    )
)

selected_product = (
    st.sidebar.selectbox(
        "Select Product",
        products
    )
)

# ----------------------------------
# USER INPUT
# ----------------------------------

user_prompt = st.text_area(
    "💬 Ask AI",
    placeholder=(
        "Example:\n"
        "Why did AUTOMOTIVE "
        "sales decrease?"
    )
)

# ----------------------------------
# ANALYZE BUTTON
# ----------------------------------

if st.button(
    "🔍 Analyze Sales"
):

    # --------------------------------
    # EMPTY CHECK
    # --------------------------------

    if not user_prompt.strip():

        st.warning(
            "Please enter a question."
        )

        st.stop()

    # --------------------------------
    # AI ANALYSIS
    # --------------------------------

    with st.spinner(
        "🤖 AI Investigating..."
    ):

        try:

            # --------------------------------
            # GET CONTEXT
            # --------------------------------

            context = (
                get_problem_context(
                    df,
                    selected_region,
                    selected_product
                )
            )

            # Validate context
            if not isinstance(
                context,
                dict
            ):
                st.error(
                    "Context generation failed."
                )
                st.stop()

            # --------------------------------
            # RECOMMENDATION
            # --------------------------------

            suggestion = (
                suggest_substitution(
                    df,
                    selected_product,
                    selected_region
                )
            )

            # --------------------------------
            # RAG RETRIEVAL
            # --------------------------------

            retrieved_cases = (
                retrieve_similar_cases(
                    index,
                    df,
                    context
                )
            )

            # --------------------------------
            # DEBUG
            # --------------------------------

            st.subheader(
                "🛠 Debug Information"
            )

            st.write(
                "### Context"
            )

            st.write(
                context
            )

            st.write(
                "### Retrieved Cases"
            )

            st.write(
                retrieved_cases
            )

            # --------------------------------
            # GEMINI LLM
            # --------------------------------

            ai_result = (
                generate_ai_explanation(
                    context,
                    suggestion,
                    retrieved_cases,
                    user_prompt
                )
            )

            st.success(
                "✅ Analysis Complete!"
            )

            # --------------------------------
            # OUTPUT COLUMNS
            # --------------------------------

            col1, col2 = st.columns(2)

            # --------------------------------
            # SALES CONTEXT
            # --------------------------------

            with col1:

                st.subheader(
                    "📉 Sales Context"
                )

                st.metric(
                    "Current Sales",
                    context.get(
                        "current_sales",
                        0
                    )
                )

                st.metric(
                    "Avg Inventory",
                    context.get(
                        "avg_inventory",
                        0
                    )
                )

                st.metric(
                    "Avg Discount",
                    context.get(
                        "avg_discount",
                        0
                    )
                )

                st.metric(
                    "Avg Marketing",
                    context.get(
                        "avg_marketing",
                        0
                    )
                )

            # --------------------------------
            # RECOMMENDATION
            # --------------------------------

            with col2:

                st.subheader(
                    "🔁 Recommendation"
                )

                if isinstance(
                    suggestion,
                    dict
                ):

                    st.write(
                        f"Replace "
                        f"**{suggestion.get('replace', 'N/A')}**"
                    )

                    st.write(
                        f"with "
                        f"**{suggestion.get('with', 'N/A')}**"
                    )

                    st.metric(
                        "Expected Sales",
                        suggestion.get(
                            "expected_sales",
                            0
                        )
                    )

                else:

                    st.warning(
                        "No recommendation found."
                    )

            # --------------------------------
            # AI OUTPUT
            # --------------------------------

            st.divider()

            st.subheader(
                "🤖 AI Investigation"
            )

            st.write(
                ai_result
            )

        except Exception as e:

            st.error(
                f"❌ Error: {str(e)}"
            )

            st.code(
                traceback.format_exc()
            )