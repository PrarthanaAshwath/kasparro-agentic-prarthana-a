from typing import List
from src.models import Product, Question


def generate_questions(product: Product) -> List[Question]:
    q: List[Question] = []

    # informational
    q.append(Question(f"What is {product.product_name}?", "informational"))
    q.append(Question("What are the key ingredients in this serum?", "informational"))
    q.append(Question("Which skin types is this serum suitable for?", "informational"))

    # usage
    q.append(Question("How should I apply this serum in my routine?", "usage"))
    q.append(Question("Can I use this serum every day?", "usage"))
    q.append(Question("Should I use this in the morning or night?", "usage"))

    # safety
    q.append(Question("Are there any side effects I should know about?", "safety"))
    q.append(Question("Is this serum suitable for sensitive skin?", "safety"))
    q.append(Question("Can I use this serum with other active ingredients?", "safety"))

    # purchase
    q.append(Question("What is the price of this serum?", "purchase"))
    q.append(Question("Is this serum good for fading dark spots?", "purchase"))

    # comparison
    q.append(Question("How does this serum compare to another Vitamin C serum?", "comparison"))
    q.append(Question("Does this serum offer better hydration than Product B?", "comparison"))
    q.append(Question("Which serum is more affordable, this or Product B?", "comparison"))

    # extra to ensure >= 15
    q.append(Question("How long will one bottle last if used daily?", "usage"))

    return q
