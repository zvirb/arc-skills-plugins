---
name: memu
description: >
  Persistent memory infrastructure for 24/7 agents (Local-First). Replaces flat-file memory
  with a three-layer architecture (Resource → Memory Item → Memory Category)
  that reduces token costs by 70-90% and enables proactive context retrieval.
  Built on NevaMind AI's open-source memU framework (v1.4.0).
version: 1.0.1
metadata:
  openclaw:
    requires:
      env: []
      bins:
        - python3
---

# memU: Persistent Memory for 24/7 Agents (Local-First)

This skill directs the agent to utilize the memU framework for long-term memory, optimized for local execution via Ollama.

## Execution Directives

1. **Initialize Service:**
   - Always use the local LLM profile for extraction and retrieval.
   - Profile: `provider: "ollama"`, `base_url: "http://localhost:11434/v1"`, `chat_model: "gemma4:latest"`.

2. **Memory Capture:**
   - Execute `memorize` for all high-intent user interactions.
   - Use `modality: "conversation"` for chat logs and `modality: "document"` for file ingestion.

3. **Proactive Retrieval:**
   - Before answering a complex query, execute `retrieve` with `method: "embedding"` to surface relevant historical context.

## Minimal Integration (Ollama)

```python
import asyncio
from memu import MemoryService

service = MemoryService(
    llm_profiles={
        "default": {
            "provider": "ollama",
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama-local",
            "chat_model": "gemma4:latest",
            "embed_model": "nomic-embed-text",
        }
    }
)
```

## Governance Rules
- **Data Locality:** Never send memory data to remote APIs.
- **Verification:** Ensure the local Postgres/pgvector container is running before attempting memory operations.

## Expected Output
A JSON result from the memU service confirming memory storage or a list of retrieved context items.
