# Open Claw Progress Tracker

This document tracks the status of Skills and Plugins across the ecosystem. 

## 📝 Not Started

### Communication & Triage
*(Moved to In Progress)*

### Task Management
*(Moved to In Progress)*

### Executive Planning
*(Moved to In Progress)*

### Human Optimization
*(Moved to In Progress)*

---

## ⏳ In Progress
*(Move items here when development begins)*
- **Node-based Atomic Skills (Google Workspace):** Decomposed into 29 strictly atomic, testable sub-nodes (24 API executors and 5 LLM-Transformers for discrete data mutation loops). Monolithic workflows are delegated to standard orchestration.

---

## ✅ Completed
*(Move items here when fully tested and deployed)*
- [x] **Vague Task Decomposition:** Combine existing Linear skill logic with a custom prompt tailored specifically for Google Tasks API manipulation via Composio.
- [x] **CRM Entity Extraction:** Build an OpenProse pipeline to bridge Gmail data extraction logic to Google Sheets or Google Contacts via Composio. *(Refactored to pure orchestration workflow chaining LLM JSON extraction and Sheets Append).*
- [x] **Capture Classification:** Build a semantic router skill utilizing the urgency heuristics to classify audio transcripts into Google Tasks or LanceDB.
- [x] **Backlog Grooming:** Construct a custom chron-triggered `SKILL.md` to evaluate old items and groom Google Tasks.
- [x] **Calendar Guard:** Engineer a custom script that injects "Recovery Block" events to protect the schedule dynamically via Google Calendar.
- [x] **Flow State Monitoring:** Build a custom logic layer to analyze `CatchMe` application-switching frequencies and sync "In Flow" status to Google Workspace.
- [x] **Micro-Suck Generation:** Write a custom `SKILL.md` that utilizes a randomized task matrix to issue minor resilience challenges to Google Tasks or Chat UI.
- [x] **LLM Refine Tool Use:** Create an atomic transformation node to refine task descriptions into strict, optimized tool usage strategies, filtering out anti-patterns like using cat/grep inside bash commands.

## 🚀 Lean Retrofit (Kaizen)
*Tracking the transition of all extensions to the Lead System Architect's Lean Standards (Jidoka/Andon loops).*

- [x] **LLM-Summarize-Text**: Retrofitted with Jidoka Andon loop and standardized config.
- [x] **LLM-Extract-JSON**: Retrofitted with Jidoka Andon loop and standardized config.
- [x] **Google-Sheets-Append-Row**: Retrofitted with Jidoka evaluator for API response verification.
- [x] **Workflow Normalization**: Refactored `crm_entity_extraction.py` into a standardized Runner.
