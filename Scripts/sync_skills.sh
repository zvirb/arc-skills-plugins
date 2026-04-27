#!/bin/bash
set -e

echo "Installing skills and binding to agents on local WSL..."
python3 /mnt/d/openClaw/Scripts/deploy_skills.py /mnt/d/openClaw/Skills/

echo "Copying skills, plugins, and deployment script to Alienware using scp..."
scp -r /mnt/d/openClaw/Skills alienware:/tmp/skills_sync
scp -r /mnt/d/openClaw/Plugins alienware:/tmp/plugins_sync
scp /mnt/d/openClaw/Scripts/deploy_skills.py alienware:/tmp/deploy_skills.py

echo "Installing skills and binding to agents on Alienware..."
ssh alienware 'python3 /tmp/deploy_skills.py /tmp/skills_sync'

echo "Installing plugins on Alienware..."
ssh alienware 'mkdir -p ~/.openclaw/extensions/google-workspace-plugin/dist/'
ssh alienware 'cp -r /tmp/plugins_sync/GoogleWorkspace/dist/* ~/.openclaw/extensions/google-workspace-plugin/dist/'
ssh alienware 'systemctl --user restart openclaw-gateway.service || true'

echo "Sync complete."
