# Tests Context

This folder contains all testing infrastructure for the repository.

## Structure
- You may mirror the `Skills/` and `Plugins/` folder structure here (e.g., `Tests/Skills/MySkill_test.py`).
- Keep fixtures and mock data in a dedicated `Tests/fixtures/` sub-folder.

## Lessons Learned
- **Relative Imports:** When writing Python unit tests directly inside the `Tests/` root directory, remember that importing a sibling directory requires a single step back (`../Skills/Name`) rather than two steps back, since `__file__` resolves to `Tests/`.
- **Architectural Shift (No Heavy External CRMs):** Notion is not a lightweight or fully open-source CRM. Instead of bridging to heavy external dependencies, we use local `SQLite` databases stored in the `Memory/` folder, paired with lightweight open-source viewers like `Datasette` or `NocoDB`.
