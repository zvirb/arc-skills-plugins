# Memory Context

This folder acts as the persistent storage layer for Open Claw agents. 

Expect this directory to hold:
- Vector database files (e.g., Chroma, FAISS)
- State JSON files or SQLite databases
- Long-term context logs

**Note:** The data files inside this directory are ignored by Git to prevent bloating the repository with local agent state.
