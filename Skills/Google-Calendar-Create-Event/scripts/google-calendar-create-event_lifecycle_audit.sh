#!/bin/bash
SUMMARY="✅ Final Omega Cal"
START="2026-05-02T22:00:00+10:00"
END="2026-05-02T22:15:00+10:00"
echo "[1/4] Creating Event..."
RES=$(/home/marku/.local/bin/gog calendar create primary --summary "$SUMMARY" --from "$START" --to "$END" --json)
EVENT_ID=$(echo "$RES" | jq -r ".event.id")
if [ "$EVENT_ID" == "null" ] || [ -z "$EVENT_ID" ]; then echo "FAILED CREATE: $RES"; exit 1; fi
echo "Event Created ID: $EVENT_ID"
echo "[2/4] Verifying Existence..."
/home/marku/.local/bin/gog calendar list --json | jq -e ".events[] | select(.id == "$EVENT_ID")" > /dev/null
echo "Verification: FOUND"
echo "[3/4] Deleting Event..."
/home/marku/.local/bin/gog calendar delete primary "$EVENT_ID" --force --json > /dev/null
echo "Deletion: DONE"
echo "[4/4] Final Verification..."
/home/marku/.local/bin/gog calendar list --json | jq -e ".events[] | select(.id == "$EVENT_ID")" && echo "OVERALL RESULT: FAILED (Still exists)" || echo "OVERALL RESULT: SUCCESS"
