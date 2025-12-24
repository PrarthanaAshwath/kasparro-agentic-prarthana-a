import json

from langchain_core.prompts import ChatPromptTemplate

from src.models import Product, ProductPage
from src.llm_client import get_llm


product_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a D2C skincare copywriter. "
                "Write structured content sections for a product page "
                "using ONLY the JSON fields provided. "
                "You MUST respond with only valid JSON, no extra text."
            ),
        ),
        (
            "user",
            (
                "Product JSON:\n{product_json}\n\n"
                "Return JSON with exactly these keys:\n"
                "- overview (string, 2-3 sentences)\n"
                "- key_benefits (list of 3-6 short bullet strings)\n"
                "- how_to_use (string, 2-4 sentences)\n"
                "- who_is_it_for (string, 2-3 sentences)\n"
                "- ingredients_section (string, 2-4 sentences)\n"
            ),
        ),
    ]
)


def product_page_node(state: dict) -> dict:
    product: Product = state["product_a"]

    llm = get_llm()
    chain = product_prompt | llm

    resp = chain.invoke({"product_json": product.model_dump_json()})
    raw = resp.content.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: extract JSON between first '{' and last '}'
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            data = json.loads(raw[start : end + 1])
        else:
            raise RuntimeError(f"Product page LLM returned non‑JSON: {raw}")

    state["product_page"] = ProductPage(
        product_name=product.product_name,
        overview=data["overview"],
        key_benefits=data["key_benefits"],
        how_to_use=data["how_to_use"],
        who_is_it_for=data["who_is_it_for"],
        ingredients_section=data["ingredients_section"],
    )
    return state
