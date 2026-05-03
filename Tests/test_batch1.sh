#!/bin/bash

log_file="Logs/batch1_results.log"
TS=$(date +%s)
echo "=== Batch 1 Testing (ID: $TS) ===" > $log_file

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
run_test "Alienware" "ssh -o StrictHostKeyChecking=no marku@100.109.60.113" "Google-Tasks-Create-Task" "Create a task in Google Tasks called 'Batch1 Alienware Create $TS' with notes 'Initial Alienware Note'."
run_test "Alienware" "ssh -o StrictHostKeyChecking=no marku@100.109.60.113" "Google-Tasks-Find-Tasks" "List my recent Google Tasks. Specifically find the ID for the task 'Batch1 Alienware Create $TS'."
run_test "Alienware" "ssh -o StrictHostKeyChecking=no marku@100.109.60.113" "Google-Tasks-Update-Task" "Update the Google Task named 'Batch1 Alienware Create $TS' to have notes 'Updated by Alienware'."
run_test "Alienware" "ssh -o StrictHostKeyChecking=no marku@100.109.60.113" "Google-Tasks-Complete-Task" "Mark the Google Task named 'Batch1 Alienware Create $TS' as completed."

echo "Batch 1 complete."
