# Multi-Agent Content Generation System

## Problem Statement
Given a small, structured product dataset for a skincare product, automatically generate machine‑readable content pages (FAQ, product description, comparison) using a modular multi‑agent system built on top of an LLM framework. The system should focus on automation flow, reusable logic, and JSON output rather than UI.

## Solution Overview
The solution is a LangGraph‑based multi‑agent pipeline that uses Groq LLMs (via LangChain) to read product JSON data and generate three structured content pages: `FAQPage`, `ProductPage`, and `ComparisonPage`. Each agent has a single responsibility (parsing, question generation, answering, page drafting, comparison, serialization), and the orchestrator graph wires them into a deterministic end‑to‑end workflow that always produces JSON outputs in the `outputs/` folder.

## Scopes & Assumptions
- Input format is a single JSON object matching the provided GlowBoost dataset fields for Product A, plus a second JSON for Product B.
- No external web research or APIs are called; LLMs are constrained to the provided product JSONs.
- Output focuses on structured, concise content rather than long‑form marketing copy.
- The system is designed to generalize to any skincare product that follows the same JSON schema.

## System Design

### Agents

- **Parser Agent (`parse_product`)**  
  - Reads `data/product_input.json` and validates it into a `Product` Pydantic model.  
  - Injects `product_a` into the shared graph state.

- **Question Generation Agent (`generate_questions`)**  
  - LLM‑backed agent using Groq Llama‑3 via LangChain.  
  - Given `product_a`, generates ≥15 customer questions in JSON, covering informational, usage, safety, purchase, and comparison categories, and stores them as `Question` objects.

- **FAQ Agent (`faq`)**  
  - For each `Question`, calls the LLM with the full product JSON as context.  
  - Produces short, precise answers, enforcing “only use product JSON” and “say you don’t know” when data is missing.  
  - Aggregates them into a `FAQPage` model and stores it as `faq_page`.

- **Product Page Agent (`product_page`)**  
  - Uses the LLM to return a JSON object with `overview`, `key_benefits`, `how_to_use`, `who_is_it_for`, and `ingredients_section` for Product A.  
  - Wraps the result in a `ProductPage` model (`product_page` in state).

- **Comparison Agent (`comparison`)**  
  - Loads `data/product_b.json` into a second `Product` (`product_b`).  
  - Asks the LLM to generate a JSON summary and a list of structured comparison points (`dimension`, `product_a`, `product_b`, `verdict`) between Product A and B.  
  - Wraps this into a `ComparisonPage` model (`comparison_page` in state).

- **Output Agent (`write_outputs`)**  
  - Serializes `faq_page`, `product_page`, and `comparison_page` to `faq.json`, `product_page.json`, and `comparison_page.json` under `outputs/`.

### Automation Flow

The multi‑agent workflow is modeled as a LangGraph `StateGraph`:

1. `parse_product` → loads `Product` A into state as `product_a`.  
2. `generate_questions` → uses LLM to produce categorized `questions`.  
3. `faq` → uses LLM to create `faq_page` from `product_a` and `questions`.  
4. `product_page` → uses LLM to produce `product_page` sections from `product_a`.  
5. `comparison` → loads `product_b`, uses LLM to generate `comparison_page`.  
6. `write_outputs` → writes all three page models to JSON in `outputs/`.

Each node reads from and writes to a typed `GraphState`, and LangGraph handles execution, retries, and passing state between nodes.

### Reusable Logic & Templates

- Reusable **data models** (`Product`, `Question`, `FAQPage`, `ProductPage`, `ComparisonPage`) define a consistent schema for all pages.
- Prompts are written so that multiple agents can share the same product JSON and still produce different views (questions, answers, product copy, comparisons).
- Because the orchestration is done via LangGraph, additional agents (for example, a review‑summarization agent or a pricing‑strategy agent) can be added by plugging new nodes into the same graph without changing existing ones.
