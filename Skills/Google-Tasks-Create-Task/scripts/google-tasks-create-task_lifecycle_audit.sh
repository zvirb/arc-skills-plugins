#!/bin/bash
TITLE="✅ Final Omega Task"
echo "[1/4] Creating Task..."
RES=$(/home/marku/.local/bin/gog tasks add @default --title "$TITLE" --json)
TASK_ID=$(echo "$RES" | jq -r ".task.id")
if [ "$TASK_ID" == "null" ] || [ -z "$TASK_ID" ]; then echo "FAILED CREATE: $RES"; exit 1; fi
echo "Task Created ID: $TASK_ID"
echo "[2/4] Verifying Existence..."
/home/marku/.local/bin/gog tasks list @default --json | jq -e ".[] | select(.id == "$TASK_ID")" > /dev/null
echo "Verification: FOUND"
echo "[3/4] Completing Task..."
/home/marku/.local/bin/gog tasks complete @default "$TASK_ID" --json > /dev/null
echo "Completion: DONE"
echo "[4/4] Final Verification..."
STATUS=$(/home/marku/.local/bin/gog tasks list @default --json | jq -r ".[] | select(.id == "$TASK_ID") | .status")
echo "Final Status: $STATUS"
if [ "$STATUS" == "completed" ]; then echo "OVERALL RESULT: SUCCESS"; else echo "OVERALL RESULT: FAILED ($STATUS)"; exit 1; fi
