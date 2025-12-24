import json
from pathlib import Path
from typing import List

from langchain_core.prompts import ChatPromptTemplate

from src.models import Product, ComparisonPoint, ComparisonPage
from src.llm_client import get_llm


comparison_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a skincare product comparison expert. "
                "Compare Product A and Product B using only the provided JSONs. "
                "You MUST respond with only valid JSON, no explanations.\n\n"
                "Return JSON with exactly these keys:\n"
                "- summary (string, 3-5 sentences)\n"
                "- points (list of objects with keys "
                "`dimension`, `product_a`, `product_b`, `verdict`)."
            ),
        ),
        (
            "user",
            (
                "Product A JSON:\n{product_a_json}\n\n"
                "Product B JSON:\n{product_b_json}"
            ),
        ),
    ]
)


def comparison_node(state: dict) -> dict:
    product_a: Product = state["product_a"]

    product_b_raw = json.loads(Path("data/product_b.json").read_text())
    product_b = Product(**product_b_raw)
    state["product_b"] = product_b

    llm = get_llm()
    chain = comparison_prompt | llm

    resp = chain.invoke(
        {
            "product_a_json": product_a.model_dump_json(),
            "product_b_json": product_b.model_dump_json(),
        }
    )
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
            raise RuntimeError(f"Comparison LLM returned non‑JSON: {raw}")

    points: List[ComparisonPoint] = [
        ComparisonPoint(**p) for p in data["points"]
    ]

    state["comparison_page"] = ComparisonPage(
        product_a_name=product_a.product_name,
        product_b_name=product_b.product_name,
        summary=data["summary"],
        points=points,
    )
    return state
