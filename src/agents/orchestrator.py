import json
from pathlib import Path
from typing import Dict, Any

from src.agents.parser_agent import parse_product
from src.agents.question_agent import generate_questions
from src.agents.content_block_agent import map_questions_to_answers
from src.agents.template_agent import (
    render_faq_page,
    render_product_page,
    render_comparison_page,
)
from src.models import to_dict


def run_pipeline(
    input_path: str,
    output_dir: str,
    product_b: Dict[str, Any],
) -> None:
    product = parse_product(input_path)

    questions = generate_questions(product)
    faqs = map_questions_to_answers(product, questions)

    faq_page = render_faq_page(product.product_name, faqs)
    product_page = render_product_page(product)
    comparison_page = render_comparison_page(product, product_b)

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    (Path(output_dir) / "faq.json").write_text(
        json.dumps(to_dict(faq_page), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (Path(output_dir) / "product_page.json").write_text(
        json.dumps(to_dict(product_page), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (Path(output_dir) / "comparison_page.json").write_text(
        json.dumps(to_dict(comparison_page), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
