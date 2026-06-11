import google.generativeai as genai

from config.config import (
    GEMINI_API_KEY
)

from ai.prompt_templates import (
    build_prompt
)

# ------------------------------------
# GEMINI CONFIG
# ------------------------------------

genai.configure(
    api_key=GEMINI_API_KEY
)

# ------------------------------------
# MODEL
# ------------------------------------

MODEL_NAME = (
    "models/gemini-2.5-flash"
)

model = genai.GenerativeModel(
    MODEL_NAME
)

# ------------------------------------
# SAFE CONVERTER
# ------------------------------------

def safe_to_text(data):

    try:

        # ------------------------
        # NONE
        # ------------------------

        if data is None:

            return (
                "No data available."
            )

        # ------------------------
        # DICTIONARY
        # ------------------------

        if isinstance(data, dict):

            return "\n".join(
                [
                    f"{k}: {v}"
                    for k, v in data.items()
                ]
            )

        # ------------------------
        # LIST
        # ------------------------

        elif isinstance(data, list):

            if len(data) == 0:

                return (
                    "No retrieved cases."
                )

            cleaned_items = []

            for item in data:

                if isinstance(
                    item,
                    dict
                ):

                    cleaned_items.append(
                        " | ".join(
                            [
                                f"{k}: {v}"
                                for k, v in item.items()
                            ]
                        )
                    )

                else:

                    cleaned_items.append(
                        str(item)
                    )

            return "\n".join(
                cleaned_items
            )

        # ------------------------
        # STRING
        # ------------------------

        elif isinstance(data, str):

            return data

        # ------------------------
        # OTHER TYPES
        # ------------------------

        return str(data)

    except Exception as e:

        print(
            "safe_to_text error:",
            str(e)
        )

        return (
            "Data conversion failed."
        )


# ------------------------------------
# MAIN GEMINI FUNCTION
# ------------------------------------

def generate_ai_explanation(
    context,
    suggestion,
    retrieved_cases,
    user_prompt
):

    try:

        print(
            "\n========== DEBUG =========="
        )

        print(
            "Context:",
            context
        )

        print(
            "Suggestion:",
            suggestion
        )

        print(
            "Retrieved Cases:",
            retrieved_cases
        )

        print(
            "User Prompt:",
            user_prompt
        )

        print(
            "===========================\n"
        )

        # ------------------------
        # SAFE TEXT CONVERSION
        # ------------------------

        context_text = (
            safe_to_text(
                context
            )
        )

        suggestion_text = (
            safe_to_text(
                suggestion
            )
        )

        retrieved_text = (
            safe_to_text(
                retrieved_cases
            )
        )

        # ------------------------
        # BUILD PROMPT
        # ------------------------

        try:

            prompt = (
                build_prompt(
                    context_text,
                    suggestion_text,
                    retrieved_text,
                    user_prompt
                )
            )

        except Exception:

            prompt = f"""
You are an AI Sales Investigation Assistant.

USER QUESTION:
{user_prompt}

SALES CONTEXT:
{context_text}

RECOMMENDATION:
{suggestion_text}

SIMILAR CASES:
{retrieved_text}

Provide:

1. Why sales dropped
2. Main business causes
3. Data insights
4. Recommendations
5. Improvement strategy
"""

        print(
            "\n===== FINAL PROMPT ====="
        )

        print(prompt)

        print(
            "========================\n"
        )

        # ------------------------
        # GEMINI CALL
        # ------------------------

        response = (
            model.generate_content(
                prompt
            )
        )

        # ------------------------
        # RESPONSE HANDLING
        # ------------------------

        if hasattr(
            response,
            "text"
        ) and response.text:

            return (
                response.text
            )

        try:

            return (
                response.candidates[0]
                .content.parts[0]
                .text
            )

        except Exception:

            return (
                "AI generated response "
                "but no readable text found."
            )

    except Exception as e:

        error_message = str(e)

        print(
            "\n❌ GEMINI ERROR:"
        )

        print(
            error_message
        )

        if "404" in error_message:

            return (
                "❌ Gemini model not found."
            )

        elif "429" in error_message:

            return (
                "⚠️ Gemini API quota exceeded."
            )

        elif "API key" in error_message:

            return (
                "❌ Invalid Gemini API key."
            )

        return (
            f"❌ AI Analysis Failed:\n"
            f"{error_message}"
        )