from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class Product:
    product_name: str
    concentration: str
    skin_type: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    how_to_use: str
    side_effects: str
    price_in_inr: int


@dataclass
class Question:
    text: str
    category: str  # e.g. "informational", "usage", "safety", "purchase", "comparison"


@dataclass
class FAQPage:
    product_name: str
    faqs: List[Dict[str, str]]  # {question, answer}


@dataclass
class ProductPage:
    product_name: str
    highlights: List[str]
    details: Dict[str, Any]


@dataclass
class ComparisonPage:
    product_a: Dict[str, Any]
    product_b: Dict[str, Any]
    comparison_points: List[Dict[str, str]]


def to_dict(obj):
    return asdict(obj)
