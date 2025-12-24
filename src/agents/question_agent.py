from typing import List

import json
from langchain_core.prompts import ChatPromptTemplate

from src.models import Product, Question
from src.llm_client import get_llm


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a senior skincare marketer and support agent. "
                "Given a product JSON, generate diverse customer questions "
                "about it. Cover informational, usage, safety, purchase, and "
                "comparison aspects. "
                "You MUST respond with only valid JSON (no explanations). "
                "Format: a list of objects, each like "
                '{{"text": "...", "category": "informational|usage|safety|purchase|comparison"}}. '
                "Generate at least 15 questions."
            ),
        ),
        (
            "user",
            "Product JSON:\n{product_json}",
        ),
    ]
)


def generate_questions_node(state: dict) -> dict:
    product: Product = state["product_a"]
    llm = get_llm()
    chain = prompt | llm

    resp = chain.invoke({"product_json": product.model_dump_json()})
    raw = resp.content.strip()

    try:
        raw_list = json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: try to extract JSON between first '[' and last ']'
        start = raw.find("[")
        end = raw.rfind("]")
        if start != -1 and end != -1 and end > start:
            raw_list = json.loads(raw[start : end + 1])
        else:
            raise RuntimeError(f"Question LLM returned non‑JSON: {raw}")

    questions: List[Question] = [Question(**q) for q in raw_list]
    state["questions"] = questions
    return state
