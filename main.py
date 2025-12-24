from src.agents.orchestrator import run_pipeline


def build_product_b():
    return {
        "name": "HydraGlow Brightening Serum",
        "key_ingredients": ["Vitamin C", "Niacinamide", "Hyaluronic Acid"],
        "benefits": ["Intense hydration", "Brightening"],
        "price_in_inr": 899,
    }


if __name__ == "__main__":
    product_b = build_product_b()
    run_pipeline(
        input_path="data/product_input.json",
        output_dir="outputs",
        product_b=product_b,
    )

#Outputs are created under `outputs/` as `faq.json`, `product_page.json`, and `comparison_page.json`. [file:8]
