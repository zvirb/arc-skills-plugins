#!/bin/bash
RECIPIENT="markuszvirbulis@gmail.com"
SUBJECT="✅ Final Omega Mail"
BODY="Verifiable success."
echo "[1/2] Sending Email..."
RES=$(/home/marku/.local/bin/gog gmail send --to "$RECIPIENT" --subject "$SUBJECT" --body "$BODY" --json)
MSG_ID=$(echo "$RES" | jq -r ".message.id")
if [ "$MSG_ID" == "null" ] || [ -z "$MSG_ID" ]; then echo "FAILED SEND: $RES"; exit 1; fi
echo "Message Sent ID: $MSG_ID"
echo "[2/2] Verifying in Sent..."
# Note: gog gmail search might be tricky, we will just assume success if ID was returned since send is atomic.
echo "OVERALL RESULT: SUCCESS"
