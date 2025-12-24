from typing import Dict, List
from src.models import Product, ProductPage
from src.agents.content_block_agent import generate_benefits_block, extract_usage_block


def build_product_page(product: Product) -> ProductPage:
    highlights: List[str] = generate_benefits_block(product)
    details: Dict[str, object] = {
        "concentration": product.concentration,
        "skin_type": product.skin_type,
        "key_ingredients": product.key_ingredients,
        "how_to_use": extract_usage_block(product),
        "side_effects": product.side_effects,
        "price_in_inr": product.price_in_inr,
    }
    return ProductPage(product_name=product.product_name, highlights=highlights, details=details)
