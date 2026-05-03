#!/bin/bash
if [ -z "$1" ]; then
  echo "Error: Missing Title"
  exit 1
fi
/home/marku/.local/bin/gog tasks add @default --title "$1" --json
