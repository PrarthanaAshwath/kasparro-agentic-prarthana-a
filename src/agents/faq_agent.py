from typing import List

from langchain_core.prompts import ChatPromptTemplate

from src.models import Product, Question, FAQEntry, FAQPage
from src.llm_client import get_llm


answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a precise skincare support bot. "
                "Answer the customer's question ONLY using the provided product JSON. "
                "If the information is not present in the JSON, reply with "
                "\"I don't know based on the available product data.\" "
                "Keep answers short and clear (1–3 sentences)."
            ),
        ),
        (
            "user",
            "Product JSON:\n{product_json}\n\nQuestion: {question}",
        ),
    ]
)


def faq_node(state: dict) -> dict:
    product: Product = state["product_a"]
    questions: List[Question] = state["questions"]

    llm = get_llm()
    chain = answer_prompt | llm

    faqs: List[FAQEntry] = []

    for q in questions:
        resp = chain.invoke(
            {
                "product_json": product.model_dump_json(),
                "question": q.text,
            }
        )
        answer_text = resp.content.strip()

        faqs.append(
            FAQEntry(
                question=q.text,
                answer=answer_text,
                category=q.category,
            )
        )

    state["faq_page"] = FAQPage(
        product_name=product.product_name,
        faqs=faqs,
    )
    return state
