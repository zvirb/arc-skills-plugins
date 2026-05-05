---
name: llm-plan-time-blocks
description: "Atomic planning node to generate a 1-day schedule from calendar and task data."
---

# LLM Plan Time Blocks

This skill directs the agent to function as a professional executive assistant, mapping a task backlog onto a calendar schedule.

## Execution Directives
1. **Analyze Constraints**: Review the provided calendar events (`events`) and identify empty time slots.
2. **Prioritize Tasks**: Rank the provided tasks (`tasks`) by urgency and importance.
3. **Draft Blocks**: Assign tasks to empty slots, ensuring:
   - 30-minute buffers between all items.
   - High-energy tasks (Complex) are in the morning.
   - Low-energy tasks (Admin) are in the afternoon.
4. **Format Output**: Return ONLY a JSON object matching the schema below. No conversational filler.

## Input Schema (JSON)
```json
{
  "events": [],
  "tasks": [],
  "weather": "string"
}
```

## Output Schema (JSON)
```json
{
  "proposed_blocks": [
    {
      "summary": "Focus: Task Title",
      "start": "ISO-8601",
      "end": "ISO-8601",
      "original_task_id": "string"
    }
  ],
  "rationale": "Brief explanation of the plan."
}
```
