from typing import Dict, List
from src.models import Product, Question


def generate_benefits_block(product: Product) -> List[str]:
    return [f"Helps with {b.lower()}." for b in product.benefits]


def extract_usage_block(product: Product) -> List[str]:
    return [
        product.how_to_use,
        "Always follow up with sunscreen in the daytime.",
    ]


def compare_ingredients_block(product: Product, product_b: Dict) -> List[Dict[str, str]]:
    points: List[Dict[str, str]] = []
    points.append({
        "aspect": "Key ingredients",
        "product_a": ", ".join(product.key_ingredients),
        "product_b": ", ".join(product_b["key_ingredients"])
    })
    points.append({
        "aspect": "Price (INR)",
        "product_a": str(product.price_in_inr),
        "product_b": str(product_b["price_in_inr"])
    })
    return points


def map_questions_to_answers(product: Product, questions: List[Question]) -> List[Dict[str, str]]:
    faqs: List[Dict[str, str]] = []

    for q in questions:
        if q.category == "informational" and "What is" in q.text:
            ans = f"{product.product_name} is a Vitamin C serum designed to brighten skin and fade dark spots."
        elif "ingredients" in q.text:
            ans = f"It contains {', '.join(product.key_ingredients)}."
        elif "skin types" in q.text:
            ans = f"It is suitable for {', '.join(product.skin_type)} skin."
        elif "apply this serum" in q.text:
            ans = product.how_to_use
        elif "every day" in q.text:
            ans = "Yes, it is generally suitable for daily use if your skin tolerates Vitamin C."
        elif "morning or night" in q.text:
            ans = "You can use it in the morning before sunscreen; some users also use it at night."
        elif "side effects" in q.text:
            ans = product.side_effects
        elif "sensitive skin" in q.text:
            ans = "People with sensitive skin may experience mild tingling and should patch test first."
        elif "other active ingredients" in q.text:
            ans = "Avoid layering with very strong exfoliating acids in the same routine."
        elif "price of this serum" in q.text:
            ans = f"The price is ₹{product.price_in_inr}."
        elif "good for fading dark spots" in q.text:
            ans = "Yes, it is formulated to help fade dark spots over consistent use."
        elif "compare to another Vitamin C serum" in q.text:
            ans = "It offers a balanced 10% Vitamin C concentration suitable for oily and combination skin types."
        elif "better hydration than Product B" in q.text:
            ans = "This serum focuses on brightening with added hydration from hyaluronic acid; Product B may focus more on hydration intensity."
        elif "more affordable, this or Product B" in q.text:
            ans = "This serum is positioned as an affordable brightening option compared to many premium alternatives."
        elif "How long will one bottle last" in q.text:
            ans = "With 2–3 drops used once daily, a typical bottle should last several weeks."
        else:
            ans = "Information is based only on the provided product data."

        faqs.append({"question": q.text, "answer": ans})

    return faqs
