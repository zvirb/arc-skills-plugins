#!/bin/bash
set -e

echo "Installing skills and binding to agents on local WSL..."
python3 /mnt/d/openClaw/deploy_skills.py /mnt/d/openClaw/Skills/

echo "Copying skills, plugins, and deployment script to Alienware..."
scp -r /mnt/d/openClaw/Skills alienware:/tmp/skills_sync
scp -r /mnt/d/openClaw/Plugins alienware:/tmp/plugins_sync
scp /mnt/d/openClaw/deploy_skills.py alienware:/tmp/deploy_skills.py

echo "Installing skills and binding to agents on Alienware..."
ssh alienware 'python3 /tmp/deploy_skills.py /tmp/skills_sync'

echo "Installing plugins on Alienware..."
ssh alienware 'openclaw plugins install /tmp/plugins_sync/GoogleWorkspace --force || true'
ssh alienware 'systemctl --user restart openclaw-gateway.service || true'

echo "Sync complete."
