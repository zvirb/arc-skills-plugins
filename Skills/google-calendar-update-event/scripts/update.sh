#!/bin/bash
EVENT_ID=$1
SUMMARY=$2
/home/marku/.local/bin/gog calendar update primary "$EVENT_ID" --summary "$SUMMARY" --force --json
