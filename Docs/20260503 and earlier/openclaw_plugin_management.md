# OpenClaw Plugin Management Guide

This document details the proper commands and workflows for managing plugins in the OpenClaw CLI based on online research.

## Installing Plugins

Plugins can be installed from the npm registry, local directories, or marketplace URLs.

- **Standard Installation:**
  `openclaw plugins install <package-name-or-path>`
  Examples: 
  - `openclaw plugins install @openclaw/voice-call`
  - `openclaw plugins install ./my-plugin`

- **Forced Installation:**
  If overwriting an existing local plugin or forcing an update:
  `openclaw plugins install <package> --force`

- **Marketplace Installation:**
  `openclaw plugins install <plugin> --marketplace <name-or-url>`

## Removing (Uninstalling) Plugins

To remove a plugin from the active system:
- **Standard Uninstall:**
  `openclaw plugins uninstall <id>`
  *Note: This removes configuration records and deletes the installed directory.*
  
- **Uninstall but Keep Files:**
  `openclaw plugins uninstall <id> --keep-files`

## Post-Installation Lifecycle

After any installation, enabling, disabling, or uninstallation of a plugin, the gateway must be restarted for changes to take effect:
`openclaw gateway restart`

## Troubleshooting and Maintenance

- **List Plugins:** `openclaw plugins list`
- **Enable/Disable:** `openclaw plugins enable <id>` or `openclaw plugins disable <id>`
- **Inspect Status:** `openclaw plugins inspect <id>`
- **Corrupted Registry / Hanging Commands:** 
  If commands like `openclaw plugins list` hang or fail due to legacy configuration records, run the doctor tool to clean the `plugins/installs.json` ledger:
  `openclaw doctor --fix`
