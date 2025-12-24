from typing import Dict, Any, List
from src.models import FAQPage, ProductPage, ComparisonPage
from templates.faq_template import build_faq_page
from templates.product_template import build_product_page
from templates.comparison_template import build_comparison_page


def render_faq_page(product_name: str, faqs: List[Dict[str, str]]) -> FAQPage:
    return build_faq_page(product_name, faqs)


def render_product_page(product) -> ProductPage:
    return build_product_page(product)


def render_comparison_page(product_a, product_b: Dict[str, Any]) -> ComparisonPage:
    return build_comparison_page(product_a, product_b)
