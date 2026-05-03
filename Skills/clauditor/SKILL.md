---
name: kebab-case-auto-fix
description: Tamper-resistant audit watchdog for Clawdbot agents. Detects and logs suspicious filesystem activity with HMAC-chained evidence.
homepage: https://github.com/apollostreetcompany/clauditor
metadata: {"clawdbot":{"emoji":"🛡️","requires":{"bins":["cargo","systemctl"],"os":"linux"}}}
---

# Clauditor

Security watchdog that monitors filesystem activity and creates tamper-evident logs.

## Installation & Configuration Directives

1. **Verify Binary Status:** Execute `./target/release/clauditor wizard status` to determine the current installation progress.
2. **Retrieve Next Instruction:** Execute `./target/release/clauditor wizard next` to identify the specific configuration step required (e.g., User Creation, Directory Setup).
3. **Request Human Approval:** Present the exact command provided by the wizard (e.g., `sudo useradd ...`) to the user. Do NOT execute `sudo` or destructive system commands without explicit "Approved" feedback.
4. **Execute Step:** After receiving approval, run the command using the `exec` tool.
5. **Confirm Completion:** Execute `./target/release/clauditor wizard verify` to validate the step was successful.
6. **Iterate:** Repeat steps 1-5 until `wizard status` returns `complete: true`.

## Maintenance Directives

1. **Check Systemd Status:** Periodically execute `systemctl status clauditor` (or the specific service name) to ensure the watchdog is active.
2. **Generate Security Digest:** Execute the `digest` command using the configured log and key paths to produce a markdown-formatted evidence report.
   - Command: `./target/release/clauditor digest --log /var/lib/.sysd/.audit/events.log --key /etc/sysaudit/key --format markdown`

## Governance Rules
- **Approval Gate:** Every command involving `sudo`, `systemctl`, or `cargo build` MUST be presented to the user for approval.
- **Evidence Protection:** Do not modify files in `/var/lib/.sysd/.audit/` or `/etc/sysaudit/` unless explicitly directed by the audit wizard.
