import json
from pathlib import Path
from src.models import Product

def parse_product_node(state: dict) -> dict:
    data_path = Path("data/product_input.json")
    raw = json.loads(data_path.read_text())
    product = Product(**raw)
    state["product_a"] = product
    return state
