import sys
import json
import time
import subprocess
import os

# ==========================================
# STANDARDIZED WORK: CONFIGURATION & SCHEMAS
# ==========================================
MAX_RETRIES = 3
DEFAULT_SCHEMA_HINT = "A valid JSON object containing keys: 'refined_strategy' (string), 'recommended_tools' (array of strings), 'anti_patterns_to_avoid' (array of strings)."
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "tool_history.json")

# Add parent directory to sys.path to import Shared modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from Shared.utils import validate_json_output as validate_output

def load_history():
    if not os.path.exists(HISTORY_FILE):
        seed_history = {
            "file_manipulation": {
                "successful_tools": ["write_to_file", "replace_file_content", "multi_replace_file_content"],
                "anti_patterns": ["cat inside bash", "echo > inside bash", "sed inside bash"],
                "notes": "Always use specific file editing tools to ensure atomic writes and avoid escaping issues."
            },
            "search_and_discovery": {
                "successful_tools": ["grep_search", "list_dir", "view_file"],
                "anti_patterns": ["grep inside bash", "find inside bash", "ls inside bash"],
                "notes": "Native search tools prevent shell injection and provide structured JSON output."
            }
        }
        save_history(seed_history)
        return seed_history
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# ==========================================
# EXECUTION LOGIC (ATOMIC)
# ==========================================
def refine_tool_use(arguments_json_str):
    try:
        arguments = json.loads(arguments_json_str)
    except:
        arguments = {"action": "plan", "task_description": arguments_json_str}

    action = arguments.get("action", "plan")
    
    if action == "record":
        # Jidoka: Autonomous recording of success/failure mappings
        history = load_history()
        use_case = arguments.get("use_case", "general")
        successful_tools = arguments.get("successful_tools", [])
        anti_patterns = arguments.get("anti_patterns", [])
        notes = arguments.get("notes", "")
        
        if use_case not in history:
            history[use_case] = {"successful_tools": [], "anti_patterns": [], "notes": ""}
            
        history[use_case]["successful_tools"] = list(set(history[use_case]["successful_tools"] + successful_tools))
        history[use_case]["anti_patterns"] = list(set(history[use_case]["anti_patterns"] + anti_patterns))
        if notes:
            history[use_case]["notes"] += f" | {notes}"
            
        save_history(history)
        return {"status": "success", "message": f"Updated history for use case '{use_case}'."}

    # Otherwise, Action is "plan"
    raw_task = arguments.get("task_description", "")
    available_tools = arguments.get("available_tools", [])
    history = load_history()
    
    # 2. Kaizen: Context-Aware Prompting
    system_prompt = (
        "ROLE: Tool Strategy Engine.\n"
        "TASK: Map the input task description against the historical tool ledger and output an optimal tool execution strategy.\n"
        "RULES:\n"
        "1. Identify the closest matching 'use_case' from the historical ledger.\n"
        "2. Recommend tools that have a history of success for this type of task.\n"
        "3. Explicitly flag and avoid any known anti-patterns documented in the ledger.\n"
        "4. If 'available_tools' are provided, prioritize from that list.\n"
        "5. Output ONLY raw JSON matching the schema. No markdown wrapping.\n"
        f"SCHEMA_REQUIREMENT: {DEFAULT_SCHEMA_HINT}"
    )
    
    current_input = (
        f"INPUT_TASK: {raw_task[:4000]}\n"
        f"AVAILABLE_TOOLS: {json.dumps(available_tools)}\n"
        f"HISTORICAL_LEDGER: {json.dumps(history)}"
    )
    error_feedback = ""

    # 3. Jidoka: Andon Loop
    for attempt in range(1, MAX_RETRIES + 1):
        instruction = f"{system_prompt}\n\n{error_feedback}\n\n{current_input}"
        
        try:
            # Atomic Execution (No-Shell Pattern)
            cmd = ["wsl", "openclaw", "infer", "model", "run", "--local", "--prompt", instruction]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            if result.returncode != 0:
                error_feedback = f"PROVIDER_ERROR: {result.stderr or 'Process failed'}"
                continue

            is_valid, result_data = validate_output(result.stdout)
            if is_valid and isinstance(result_data, dict) and "refined_strategy" in result_data:
                return result_data
            
            error_feedback = f"PREVIOUS_FAILURE: {result_data}\nACTION: Fix JSON structure to include required keys ('refined_strategy', 'recommended_tools', 'anti_patterns_to_avoid')."
            
        except Exception as e:
            error_feedback = f"SYSTEM_EXCEPTION: {str(e)}"
            
        time.sleep(1)

    # 4. Deterministic Failure
    return {
        "status": "error",
        "message": f"Refinement failed after {MAX_RETRIES} attempts.",
        "final_error": error_feedback
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Missing input."}))
        sys.exit(1)
    
    print(json.dumps(refine_tool_use(sys.argv[1]), indent=2))
