# SDLC Domain 4: Verification

## Purpose
The Verification domain focuses on "Jidoka" (Autonomation)—ensuring that every component functions exactly as designed and that errors are caught and corrected autonomously. This phase moves beyond simple unit testing into independent state confirmation.

## Documents
- **[4.1 Deterministic Evaluation](./4.1_Deterministic_Evaluation.md)**: Defining the "Master Success Criteria" for every node.
- **[4.2 Jidoka Loop Verification](./4.2_Jidoka_Verification.md)**: Testing the self-healing and error-correction loops.
- **[4.3 Stateless Verification Protocol](./4.3_Stateless_Verification.md)**: Ensuring nodes can be verified without session pollution.
- **[4.4 Independent State Confirmation](./4.4_Independent_Confirmation.md)**: Using external tools (e.g., browser) to verify state changes.

## Workflows
- `verify-node`: Execute the Jidoka validation loop for an atomic node.
- `verify-e2e`: End-to-end testing with independent state confirmation.
- `verify-security`: Automated audit for leaked secrets and permission violations.

## Jidoka Gate
The Verification phase is considered complete only when the **Independent Auditor** (a separate sub-agent) confirms that the physical state of the environment (filesystem, Google Workspace, etc.) matches the intended result.
