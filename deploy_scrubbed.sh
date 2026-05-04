#!/bin/bash
cat << 'EOF' > /tmp/hardened_wrapper.sh
#!/bin/bash
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
EOF

chmod +x /tmp/hardened_wrapper.sh

for d in /home/marku/.openclaw/workspace/skills/google-* /home/marku/.openclaw/workspace/skills/gmail-*; do
  if [ -f "$d/scripts/run.sh" ]; then
    cp /tmp/hardened_wrapper.sh "$d/scripts/run.sh"
  fi
done
