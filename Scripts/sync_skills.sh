#!/bin/bash
set -e

echo "Installing skills and binding to agents on local WSL..."
python3 /mnt/d/openClaw/Scripts/deploy_skills.py /mnt/d/openClaw/Skills/

echo "Copying skills, plugins, and deployment script to Alienware using scp..."
scp -r /mnt/d/openClaw/Skills alienware:/tmp/skills_sync
ssh alienware 'mkdir -p /tmp/plugins_sync/AutonomousWorkflows/dist /tmp/plugins_sync/GoogleWorkspace/dist /tmp/plugins_sync/LLMTransformations/dist /tmp/plugins_sync/ToolStrategyEngine/dist'
scp -r /mnt/d/openClaw/Plugins/AutonomousWorkflows/dist/* alienware:/tmp/plugins_sync/AutonomousWorkflows/dist/ || true
scp -r /mnt/d/openClaw/Plugins/GoogleWorkspace/dist/* alienware:/tmp/plugins_sync/GoogleWorkspace/dist/ || true
scp -r /mnt/d/openClaw/Plugins/LLMTransformations/dist/* alienware:/tmp/plugins_sync/LLMTransformations/dist/ || true
scp -r /mnt/d/openClaw/Plugins/ToolStrategyEngine/dist/* alienware:/tmp/plugins_sync/ToolStrategyEngine/dist/ || true
scp /mnt/d/openClaw/Scripts/deploy_skills.py alienware:/tmp/deploy_skills.py

echo "Installing skills and binding to agents on Alienware..."
ssh alienware 'python3 /tmp/deploy_skills.py /tmp/skills_sync'

echo "Installing plugins on Alienware..."
ssh alienware 'cp -r /tmp/plugins_sync/AutonomousWorkflows/dist/* ~/.openclaw/extensions/autonomous-workflows-plugin/dist/ || true'
ssh alienware 'cp -r /tmp/plugins_sync/GoogleWorkspace/dist/* ~/.openclaw/extensions/google-workspace-plugin/dist/ || true'
ssh alienware 'cp -r /tmp/plugins_sync/LLMTransformations/dist/* ~/.openclaw/extensions/llm-transformations-plugin/dist/ || true'
ssh alienware 'cp -r /tmp/plugins_sync/ToolStrategyEngine/dist/* ~/.openclaw/extensions/tool-strategy-engine/dist/ || true'
ssh alienware 'systemctl --user restart openclaw-gateway.service || true'

echo "Sync complete."
