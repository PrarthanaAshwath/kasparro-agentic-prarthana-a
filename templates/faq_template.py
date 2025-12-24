from typing import List, Dict
from src.models import FAQPage


def build_faq_page(product_name: str, faqs: List[Dict[str, str]]) -> FAQPage:
    return FAQPage(product_name=product_name, faqs=faqs)
