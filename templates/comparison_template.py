from typing import Dict
from src.models import Product, ComparisonPage
from src.agents.content_block_agent import compare_ingredients_block


def build_comparison_page(product_a: Product, product_b: Dict) -> ComparisonPage:
    comparison_points = compare_ingredients_block(product_a, product_b)
    return ComparisonPage(
        product_a={
            "name": product_a.product_name,
            "price_in_inr": product_a.price_in_inr,
            "key_ingredients": product_a.key_ingredients,
        },
        product_b=product_b,
        comparison_points=comparison_points,
    )
