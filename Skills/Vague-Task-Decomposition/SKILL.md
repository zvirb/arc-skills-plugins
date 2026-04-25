---
name: Vague Task Decomposition
description: Combine existing Linear skill logic with a custom prompt tailored specifically for Google Tasks API manipulation via Composio.
os: windows
requires:
  bins:
    - python
  env:
    - COMPOSIO_API_KEY
---

# Vague Task Decomposition Skill

This skill uses an LLM prompt to decompose a vague task string into actionable, distinct subtasks and then dispatches them to Google Tasks using Composio.

## Instructions
1. Accept a vague task description.
2. Formulate a prompt requesting a JSON array of actionable subtasks.
3. Call a local LLM or API to get the decomposition.
4. Iterate over the subtasks and use Composio's Google Tasks integration to create entries.

## Installation & Persistent WSL Setup
Since this skill relies on the `composio` Python SDK, you must install it in a virtual environment within WSL. To ensure OpenClaw and your scripts have persistent access to this environment, follow these steps:

1. **Create the Virtual Environment:**
   Run this inside your OpenClaw repository (or your home directory):
   `python3 -m venv .venv`

2. **Install Composio:**
   Activate the environment and install the required packages:
   `source .venv/bin/activate`
   `pip install composio-core composio`

3. **Allow Persistent Access (Auto-Activation):**
   To ensure the virtual environment is always active when you open a WSL terminal (and when OpenClaw runs shell commands), add the activation script to your `~/.bashrc` or `~/.zshrc`:
   `echo 'source /mnt/d/openClaw/.venv/bin/activate' >> ~/.bashrc`
   `source ~/.bashrc`

Now, whenever you or OpenClaw run `python`, it will automatically use the environment where `composio` is installed!
