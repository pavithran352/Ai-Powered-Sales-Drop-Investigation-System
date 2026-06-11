def build_prompt(
    context,
    suggestion,
    retrieved_cases,
    user_prompt
):

    return f"""
You are an expert retail
business analyst.

User Question:
{user_prompt}

Current Situation:

Current Sales:
{context['current_sales']}

Inventory:
{context['avg_inventory']}

Competitor Discount:
{context['avg_discount']}

Suggested Product:
{suggestion['with']}

Historical Similar Cases:
{retrieved_cases}

Answer professionally.

Explain:
1. WHY sales dropped
2. Root cause
3. Product impact
4. Business recommendation
5. Recovery strategy
"""