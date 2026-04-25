---
name: Procedural Skill Generation & Validation
description: Automate the creation of directory-based capabilities that rely on LLM reasoning and existing tools.
---

# Procedural Skill Generation & Validation

This workflow enforces the structural constraints for new OpenClaw Skills to ensure they do not bleed into runtime plugins.

## Steps

1. **Scaffold Skill Directory:** Create the designated sub-folder within the `Skills/` directory.
2. **Generate SKILL.md:** Create a compliant `SKILL.md` file within the new sub-folder.
3. **Parse Directives:** Automatically parse required operational directives and explicitly define the `metadata` block in the YAML frontmatter.
4. **Validation Gate (Requirements):** Verify that `requires.bins`, `requires.env`, and `os` filters are correctly mapped in the YAML frontmatter. 
5. **Validation Gate (Security):** Run a shell injection vulnerability check to ensure no raw string concatenation is present if the `exec` tool is utilized.
6. **Final Check:** Request execution of `openclaw skills check <skill-name>` to verify syntax and dependency eligibility.
