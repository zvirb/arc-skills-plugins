---
name: gemini-web-search
description: Use Gemini CLI to perform web searches and fact-finding.
---

# Gemini Web Search

This skill directs the agent to utilize the Gemini CLI for sourcing up-to-date information from the web.

## Execution Directives
1. **Query Construction:** Formulate a specific, high-intent search query including names, dates, and required data points (e.g., "NVIDIA stock price change April 28 2026").
2. **Execute Search:** Run `~/.npm-global/bin/gemini -p "<query>"` using the `exec` tool.
   - **Optimization:** Use `pty: true` and set a timeout of 300s to prevent hangs.
3. **Parse Results:** Extract key facts, numeric data, and at least 2 source links from the output.
4. **Source Verification:** If the sources appear unreliable or conflicting, notify the user and suggest a secondary search with a narrower focus (e.g., "site:reuters.com").
5. **Synthesize Answer:** Present the findings in a concise, header-driven summary with cited links.

## Expected Output
A sourced summary of the search results with direct links to the information.
