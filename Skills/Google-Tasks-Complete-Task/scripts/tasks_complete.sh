#!/bin/bash
if [ -z "$1" ]; then
  echo "Error: Missing Task ID"
  exit 1
fi
/home/marku/.local/bin/gog tasks complete @default "$1" --json
