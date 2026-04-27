#!/bin/bash
set -e

echo "Installing skills on local WSL..."
for d in /mnt/d/openClaw/Skills/*/; do
  openclaw skills install "$d"
done

echo "Restarting local gateway..."
openclaw gateway restart

echo "Copying skills to Alienware..."
scp -r /mnt/d/openClaw/Skills alienware:/tmp/skills_sync

echo "Installing skills on Alienware..."
ssh alienware 'for d in /tmp/skills_sync/*/; do openclaw skills install "$d"; done && openclaw gateway restart'

echo "Sync complete."
