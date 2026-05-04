#!/bin/bash
# Fixed: No hardcoded credentials.
BINARY=${GOG_BIN_PATH:-/home/marku/.local/bin/gog}

OUTPUT=$($BINARY "$@" 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  CLEAN_OUTPUT=$(echo "$OUTPUT" | sed 's/"/\\"/g' | tr -d '\n' | tr -d '\r')
  cat <<EOF
{
  "STATUS": "ERROR",
  "EXIT_CODE": $EXIT_CODE,
  "ERROR_MSG": "$CLEAN_OUTPUT",
  "ACTION": "Please check flags and syntax (e.g. @default)."
}
EOF
  exit 0
else
  echo "$OUTPUT"
fi
