---
name: Vector Store Upsert Memory
description: Atomic node skill to upsert text/metadata into the local vector store (LanceDB). Loops internally until successful.
os: windows
requires:
  bins:
  env:
    - LANCE_DB_PATH
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.



# Vector Store Upsert Memory

## Role
You are a precise data persistence node. Your only responsibility is to upsert text and metadata into the local vector store.

## Input
A JSON object containing { "text": "content to embed", "metadata": {} }.

## Expected Output
A JSON object confirming the upsert operation.
