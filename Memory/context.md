# Memory Context

This folder is the persistent storage layer for OpenClaw. All state management must adhere to the **May 2026 Infrastructure Standards (v2026.5.x)** to prevent context window exhaustion.

## 1. Zero-Context State Management
*   **Avoid Context Bloat:** Do NOT store large datasets (OCR results, file lists) in the LLM's working context. This triggers PCIe bottlenecking and OOM.
*   **State Primers:** Use `state.get` and `state.set` for persistence across sessions.
*   **Memory-Core:** Revert to the native `memory-core` system for semantically-indexed retrieval rather than using custom scratchpad hacks.

## 2. Heavy Payload Storage
*   **PluginArtifacts:** Use the `PluginArtifact` schema for structured data that exceeds the 10KB JSON-RPC limit.
*   **Blob Storage:** Large binary or text objects should be stored as files and referenced via the `lobster://` URI protocol.

## 3. Persistent Hierarchy
*   `Memory/state/`: JSON/SQLite files for atomic task state.
*   `Memory/vector/`: Vector database files for long-term RAG.

## 4. Note
The data files in this directory are ignored by Git. They represent the unique, non-replicable experience of the local agent swarm.
