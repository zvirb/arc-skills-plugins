#!/bin/bash
# Automatically load credentials from git-ignored Secrets directory
SECRET_FILE="$(dirname "$0")/../../../Secrets/gog.env"
if [ -f "$SECRET_FILE" ]; then
  source "$SECRET_FILE"
fi

BINARY=${GOG_BIN_PATH:-/home/marku/.local/bin/gog}

OUTPUT=$($BINARY "$@" 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  CLEAN_OUTPUT=$(echo "$OUTPUT" | sed 's/"/\\"/g' | tr -d '\n' | tr -d '\r')
  cat <<JSON
{
  "STATUS": "ERROR",
  "EXIT_CODE": $EXIT_CODE,
  "ERROR_MSG": "$CLEAN_OUTPUT",
  "ACTION": "Please check flags and syntax (e.g. @default)."
}
JSON
  exit 0
else
  echo "$OUTPUT"
fi
