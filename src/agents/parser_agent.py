import json
from pathlib import Path
from src.models import Product


def parse_product(input_path: str) -> Product:
    data = json.loads(Path(input_path).read_text(encoding="utf-8"))
    return Product(
        product_name=data["product_name"],
        concentration=data["concentration"],
        skin_type=data["skin_type"],
        key_ingredients=data["key_ingredients"],
        benefits=data["benefits"],
        how_to_use=data["how_to_use"],
        side_effects=data["side_effects"],
        price_in_inr=data["price_in_inr"],
    )
