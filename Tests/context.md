# Tests Context

This folder contains the testing infrastructure. All validation must adhere to the **May 2026 Infrastructure Standards (v2026.5.x)** to ensure environment parity and prevent false positives.

## 1. The Alienware Protocol (MANDATORY)
*   **No WSL Testing:** Local WSL testing is strictly prohibited for E2E validation. All tests MUST execute via SSH on the **alienware** node.
*   **Log Observation:** Use `openclaw tui` or `openclaw logs --follow` during test execution to catch silent validation failures or PCIe timeouts.

## 2. State Verification Rules
*   **Observable State Only:** Verification tools MUST only observe the current state. They are strictly forbidden from "fixing" or completing the task (e.g., creating a missing Google Task during a test).
*   **Physical Verification:** For all Google Workspace mutations, use the `browser` tool to navigate to the relevant URL and confirm the change is visible to a human user.
*   **Clean Slate:** Ensure tests are stateless. Use `Memory/state/` cleanup scripts before and after test runs to prevent cross-session data bleeding.

## 3. Structure & Tooling
*   **Mocking:** Use local SQLite databases in `Memory/` for CRM/state mocking.
*   **Skill Integrity:** Markdown skills are validated via `Skill_Integrity_test.py`.
*   **Lobster Validation:** YAML/Lobster workflows must be validated using `openclaw check --workflow <path>` using absolute paths.

## 4. Hardware Constraints
Verify that tests do not trigger GPU OOM. If tests fail with CUDA errors, reduce `OLLAMA_NUM_CTX` to `4096` or `imageMaxDimensionPx` to `800`.
