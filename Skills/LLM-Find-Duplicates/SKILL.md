---
name: LLM Find Duplicates
description: Atomic transformation node to identify duplicates in a dataset and return a list. Loops internally until successful.
os: windows
requires:
  bins:
    - openclaw
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.



# LLM Find Duplicates

## Role
You are a precise data transformation node. Your only responsibility is to identify duplicates in a dataset and return a list.

## Input
A JSON object containing { "text": "raw content to process", "schema": "optional json schema description" }.

## Expected Output
A JSON array representing the result of the operation.
