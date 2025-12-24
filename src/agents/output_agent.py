import json
from pathlib import Path
from src.models import FAQPage, ProductPage, ComparisonPage

def write_outputs_node(state: dict) -> dict:
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)

    faq_page: FAQPage = state["faq_page"]
    product_page: ProductPage = state["product_page"]
    comparison_page: ComparisonPage = state["comparison_page"]

    (outputs_dir / "faq.json").write_text(faq_page.model_dump_json(indent=2))
    (outputs_dir / "product_page.json").write_text(product_page.model_dump_json(indent=2))
    (outputs_dir / "comparison_page.json").write_text(comparison_page.model_dump_json(indent=2))

    return state
