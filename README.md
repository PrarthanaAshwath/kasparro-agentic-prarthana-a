# Kasparro – Agentic Content Generation System

This project implements a LangGraph-based multi‑agent pipeline in Python that reads a skincare product dataset and uses an LLM to generate three machine‑readable content pages in JSON: FAQ, product page, and comparison page.

## Tech Stack

- Python 3.11
- LangChain + LangGraph
- Groq LLMs (via `langchain-groq`, default model: `llama-3.1-8b-instant`)
- Pydantic for typed models
- JSON I/O for all inputs and outputs

## Project Structure

- `data/product_input.json` – Product A (GlowBoost) input.
- `data/product_b.json` – Product B used for comparison.
- `outputs/faq.json` – Generated FAQ page.
- `outputs/product_page.json` – Generated product description page.
- `outputs/comparison_page.json` – Generated comparison page.
- `src/models.py` – Pydantic models (`Product`, `Question`, `FAQPage`, `ProductPage`, `ComparisonPage`, etc.).
- `src/llm_client.py` – Groq LLM client (`ChatGroq`) and configuration.
- `src/graph.py` – LangGraph `StateGraph` wiring all agents.
- `src/agents/parser_agent.py` – Parses product JSON into a `Product` model.
- `src/agents/question_agent.py` – LLM agent that generates ≥15 categorized questions from the product JSON.
- `src/agents/faq_agent.py` – LLM agent that answers each question using only the product JSON and builds a `FAQPage`.
- `src/agents/product_page_agent.py` – LLM agent that drafts structured sections for the product page.
- `src/agents/comparison_agent.py` – LLM agent that compares Product A and B and builds a `ComparisonPage`.
- `src/agents/output_agent.py` – Serializes all page models to JSON files in `outputs/`.

## Agentic Architecture & Flow

The system is implemented as a LangGraph `StateGraph` with the following nodes:

1. **parse_product**  
   - Deterministically loads `data/product_input.json` into a typed `Product` object.

2. **generate_questions** (LLM agent)  
   - Uses Groq Llama‑3 via LangChain to generate a JSON list of diverse customer questions.  
   - Each question is tagged with a category: `informational`, `usage`, `safety`, `purchase`, or `comparison`.

3. **faq** (LLM agent)  
   - For each `Question`, calls the LLM with the product JSON as context.  
   - Answers strictly from the JSON and constructs a `FAQPage` model.

4. **product_page** (LLM agent)  
   - Asks the LLM to return a JSON object with `overview`, `key_benefits`, `how_to_use`, `who_is_it_for`, and `ingredients_section` for the product page.

5. **comparison** (LLM agent)  
   - Loads `data/product_b.json` into a second `Product`.  
   - Asks the LLM to produce a JSON summary and comparison points across key dimensions, building a `ComparisonPage`.

6. **write_outputs**  
   - Writes `faq.json`, `product_page.json`, and `comparison_page.json` under `outputs/`.

The graph entry point is `parse_product`, and execution flows linearly through the above nodes until all outputs are written.

## Setup & Usage

1. Create a virtual environment and install dependencies:


2. Create a `.env` file in the project root with your Groq API key:


3. Run the multi‑agent pipeline:


4. Inspect the generated JSON files under `outputs/` for the FAQ, product page, and comparison page.

## Assumptions & Constraints

- All content is generated from the provided product JSONs only (no external web search).
- The system assumes the product JSONs follow the same schema as `product_input.json`.
- Outputs are optimized for structure and clarity rather than long marketing copy.
