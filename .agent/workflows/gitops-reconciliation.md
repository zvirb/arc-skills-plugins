---
name: GitOps Reconciliation Preparation
description: Package the developed extensions for automated, declarative deployment via Flux CD.
---

# GitOps Reconciliation Preparation

This workflow prepares and validates extensions for production deployment using GitOps principles.

## Steps

1. **Local Verification:** Confirm that the target Skill or Plugin has passed all local tests (`openclaw skills check` or `openclaw plugins list --verbose`).
2. **Manifest Mapping:** Map the target dependency to the `spec.skills` or `spec.plugins` fields of the target cluster's `OpenClawInstance` CRD.
3. **Validation Gate (Immutability):** Enforce immutability by pinning exact semantic versions for plugins, or precise commit hashes using the `pack:` prefix for repository-sourced skills.
4. **State Persistence Configuration:** Ensure that `mergeMode` is explicitly set to `merge` when modifying the `spec.config` to prevent wiping out the agent's runtime environmental state during pod restarts.
