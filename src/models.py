from pydantic import BaseModel
from typing import List, Literal, Dict, Any

QuestionCategory = Literal["informational", "usage", "safety", "purchase", "comparison"]


class Product(BaseModel):
    # Match exactly the keys in data/product_input.json
    product_name: str
    skin_type: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    how_to_use: str
    side_effects: str
    price_in_inr: float

class Question(BaseModel):
    text: str
    category: QuestionCategory

class FAQEntry(BaseModel):
    question: str
    answer: str
    category: QuestionCategory

class FAQPage(BaseModel):
    product_name: str
    faqs: List[FAQEntry]

class ProductPage(BaseModel):
    product_name: str
    overview: str
    key_benefits: List[str]
    how_to_use: str
    who_is_it_for: str
    ingredients_section: str

class ComparisonPoint(BaseModel):
    dimension: str
    product_a: str
    product_b: str
    verdict: str

class ComparisonPage(BaseModel):
    product_a_name: str
    product_b_name: str
    summary: str
    points: List[ComparisonPoint]
