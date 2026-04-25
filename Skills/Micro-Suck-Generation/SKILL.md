---
name: micro-suck-generation
description: Workflow-driven skill that issues minor resilience challenges to build task-initiation momentum.
os: windows
requires:
  bins:
    - python
  env:
    - COMPOSIO_API_KEY
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.



# Micro-Suck Generation

This skill orchestrates a workflow to select a random minor task (a "micro-suck") and inject it into your Google Tasks list to kickstart executive function.

## Workflow Orchestration
This skill delegates its execution to `d:\openClaw\Workflows\micro_suck_generation.py`, which chains the following atomic nodes:
1. **LLM-Select-Random-Item**: Randomly selects a task from a predefined resilience matrix.
2. **Google-Tasks-Create-Task**: Injects the selected task into Google Tasks with high priority.

## Role
You are a coach. When you detect the user is stuck or procrastinating, you should trigger this workflow to help them build momentum.

## Input
None (Triggered by energy lull detection or schedule).

## Expected Output
A confirmation of the injected micro-task.
