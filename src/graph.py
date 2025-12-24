from langgraph.graph import StateGraph, END


from typing import TypedDict, List
from src.models import Product, Question, FAQPage, ProductPage, ComparisonPage
from src.agents.parser_agent import parse_product_node
from src.agents.question_agent import generate_questions_node
from src.agents.faq_agent import faq_node
from src.agents.product_page_agent import product_page_node
from src.agents.comparison_agent import comparison_node
from src.agents.output_agent import write_outputs_node

class GraphState(TypedDict, total=False):
    product_a: Product
    product_b: Product
    questions: List[Question]
    faq_page: FAQPage
    product_page: ProductPage
    comparison_page: ComparisonPage

def build_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("parse_product", parse_product_node)
    workflow.add_node("generate_questions", generate_questions_node)
    workflow.add_node("faq", faq_node)
    workflow.add_node("product_page", product_page_node)
    workflow.add_node("comparison", comparison_node)
    workflow.add_node("write_outputs", write_outputs_node)

    workflow.set_entry_point("parse_product")
    workflow.add_edge("parse_product", "generate_questions")
    workflow.add_edge("generate_questions", "faq")
    workflow.add_edge("faq", "product_page")
    workflow.add_edge("product_page", "comparison")
    workflow.add_edge("comparison", "write_outputs")
    workflow.add_edge("write_outputs", END)

    return workflow.compile()
