# Multi-Agent Content Generation System

## Problem Statement
Given a small, structured product dataset for a skincare product, automatically generate machine-readable content pages (FAQ, product description, comparison) using a modular multi-agent system. The system should focus on automation flow, reusable logic, and JSON output rather than UI or prompt engineering.

## Solution Overview
The solution is a fully rule-based Python pipeline composed of multiple agents. Each agent has a single responsibility: parsing the product data, generating categorized questions, transforming data into reusable content blocks, and rendering structured pages using simple templates. The orchestrator agent coordinates these agents and writes three JSON files: `faq.json`, `product_page.json`, and `comparison_page.json`. 

## Scopes & Assumptions
- Input format is a single JSON object matching the provided GlowBoost dataset fields.  
- No external product research or dynamic API calls are performed; all logic is rule-based on the given fields.  
- Output focuses on structure and clarity, not marketing-style copy length.  
- A fictional Product B is defined in code only for comparison purposes. 

## System Design
### Agents
- **Parser Agent**: Reads `data/product_input.json`, validates keys, and converts to a `Product` model.  
- **Question Generation Agent**: Generates ≥15 user questions grouped into informational, usage, safety, purchase, and comparison categories.  
- **Content Block Agent**: Implements reusable logic blocks such as `generate_benefits_block`, `extract_usage_block`, `compare_ingredients_block`, and maps questions to answers.  
- **Template Agent**: Wraps template functions and turns blocks into page models (`FAQPage`, `ProductPage`, `ComparisonPage`).  
- **Orchestrator Agent**: Defines the end-to-end flow: parse → questions → content blocks → templates → JSON files. 

### Automation Flow
The system behaves like a simple DAG:
1. `parse_product` → `Product` model.  
2. `generate_questions(Product)` → list of categorized questions.  
3. `map_questions_to_answers(Product, questions)` → FAQ entries.  
4. Template agent builds `FAQPage`, `ProductPage`, `ComparisonPage`.  
5. Orchestrator serializes the page models to JSON in `outputs/`. 

### Reusable Logic & Templates
- Logic blocks are plain Python functions that can be reused across pages, such as generating benefits and usage sections or ingredient/price comparison points.  
- Templates define which fields and logic blocks populate each page type, so new page types can be added by composing existing blocks. 
