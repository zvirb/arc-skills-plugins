#!/bin/bash

log_file="/mnt/d/openClaw/Logs/batch2_results.log"
TS=$(date +%s)
echo "=== Batch 2 Testing (ID: $TS) ===" > $log_file

run_test() {
  local env=$1
  local cmd_prefix=$2
  local test_name=$3
  local prompt=$4
  local session_id="test-${env}-${test_name}"

  echo "Testing [$env] $test_name..." | tee -a $log_file
  eval "$cmd_prefix '/home/marku/.local/share/pnpm/openclaw agent --session-id \"$session_id\" --message \"$prompt. Please execute this and if you encounter a persistent error, stop and report it.\"'" >> $log_file 2>&1
  echo "Done testing $test_name." | tee -a $log_file
  echo "----------------------" >> $log_file
}

# WSL Tests

# Alienware Tests
run_test "Alienware" "ssh -o StrictHostKeyChecking=no alienware" "Google-Calendar-Create-Event" "Create an event in Google Calendar called 'Batch2 Alienware Event $TS' tomorrow at 4 PM for 1 hour."
run_test "Alienware" "ssh -o StrictHostKeyChecking=no alienware" "Google-Calendar-Find-Event" "Find the Google Calendar event called 'Batch2 Alienware Event $TS'."
run_test "Alienware" "ssh -o StrictHostKeyChecking=no alienware" "Google-Calendar-Update-Event" "Update the Google Calendar event 'Batch2 Alienware Event $TS' to start at 5 PM tomorrow."
run_test "Alienware" "ssh -o StrictHostKeyChecking=no alienware" "Google-Calendar-Delete-Event" "Delete the Google Calendar event 'Batch2 Alienware Event $TS'."

echo "Batch 2 complete."
