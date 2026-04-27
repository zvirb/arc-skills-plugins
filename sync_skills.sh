#!/bin/bash
set -e

echo "Installing skills and binding to agents on local WSL..."
python3 /mnt/d/openClaw/deploy_skills.py /mnt/d/openClaw/Skills/

echo "Copying skills and deployment script to Alienware..."
scp -r /mnt/d/openClaw/Skills alienware:/tmp/skills_sync
scp /mnt/d/openClaw/deploy_skills.py alienware:/tmp/deploy_skills.py

echo "Installing skills and binding to agents on Alienware..."
ssh alienware 'python3 /tmp/deploy_skills.py /tmp/skills_sync'

echo "Sync complete."
