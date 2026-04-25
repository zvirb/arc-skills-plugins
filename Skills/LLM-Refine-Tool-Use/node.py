import sys
import json
import time
import subprocess
import os

# ==========================================
# STANDARDIZED WORK: CONFIGURATION & SCHEMAS
# ==========================================
MAX_RETRIES = 3
DEFAULT_SCHEMA_HINT = "A valid JSON object containing keys: 'refined_strategy' (string), 'recommended_tools' (array of strings), 'anti_patterns_to_avoid' (array of strings), 'argument_constraints' (object mapping tool names to strict argument rules to prevent hallucination)."
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "tool_history.json")

# Add parent directory to sys.path to import Shared modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from Shared.utils import validate_json_output as validate_output

def load_history():
    if not os.path.exists(HISTORY_FILE):
        seed_history = {
            "use_cases": {
                "file_manipulation": {
                    "successful_tools": ["write_to_file", "replace_file_content", "multi_replace_file_content"],
                    "anti_patterns": ["cat inside bash", "echo > inside bash", "sed inside bash"],
                    "notes": "Always use specific file editing tools to ensure atomic writes."
                }
            },
            "tool_constraints": {
                "run_command": {
                    "argument_rules": ["Requires 'Cwd' and 'CommandLine'.", "Do not use generic shell tools like cat/grep/sed if a native tool exists."],
                    "known_errors": ["Hallucinating arguments like 'cwd' instead of 'Cwd'", "Missing required WaitMsBeforeAsync argument."]
                }
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
    history = load_history()
    
    if action == "record":
        # Jidoka: Autonomous recording of success/failure and tool argument schemas
        use_case = arguments.get("use_case", "general")
        successful_tools = arguments.get("successful_tools", [])
        anti_patterns = arguments.get("anti_patterns", [])
        notes = arguments.get("notes", "")
        
        # New constraint tracking to prevent parameter hallucination
        tool_name = arguments.get("tool_name", "")
        error_encountered = arguments.get("error_encountered", "")
        argument_rule = arguments.get("argument_rule", "")

        # 1. Update Use Cases
        if use_case:
            if use_case not in history["use_cases"]:
                history["use_cases"][use_case] = {"successful_tools": [], "anti_patterns": [], "notes": ""}
            
            history["use_cases"][use_case]["successful_tools"] = list(set(history["use_cases"][use_case]["successful_tools"] + successful_tools))
            history["use_cases"][use_case]["anti_patterns"] = list(set(history["use_cases"][use_case]["anti_patterns"] + anti_patterns))
            if notes:
                history["use_cases"][use_case]["notes"] += f" | {notes}"

        # 2. Update Tool Constraints
        if tool_name:
            if tool_name not in history["tool_constraints"]:
                history["tool_constraints"][tool_name] = {"argument_rules": [], "known_errors": []}
                
            if argument_rule:
                history["tool_constraints"][tool_name]["argument_rules"].append(argument_rule)
                history["tool_constraints"][tool_name]["argument_rules"] = list(set(history["tool_constraints"][tool_name]["argument_rules"]))
                
            if error_encountered:
                history["tool_constraints"][tool_name]["known_errors"].append(error_encountered)
                history["tool_constraints"][tool_name]["known_errors"] = list(set(history["tool_constraints"][tool_name]["known_errors"]))

        save_history(history)
        return {"status": "success", "message": "Updated historical tool ledger with new constraints and mappings."}

    # Otherwise, Action is "plan"
    raw_task = arguments.get("task_description", "")
    available_tools = arguments.get("available_tools", [])
    
    # Filter constraints to only tools available, to save context window, or pass all if none provided
    relevant_constraints = history["tool_constraints"]
    if available_tools:
        relevant_constraints = {k: v for k, v in history["tool_constraints"].items() if k in available_tools}
    
    # 2. Kaizen: Context-Aware Prompting
    system_prompt = (
        "ROLE: Tool Strategy Engine.\n"
        "TASK: Analyze the task and historical ledger to prevent tool misuse and argument hallucination.\n"
        "RULES:\n"
        "1. Recommend tools with a history of success for this task.\n"
        "2. Explicitly define the 'argument_constraints' in your output for the recommended tools, mapping out exactly what arguments MUST be provided and which known errors to avoid based on the ledger.\n"
        "3. Explicitly flag and avoid any known anti-patterns.\n"
        "4. Output ONLY raw JSON matching the schema. No markdown wrapping.\n"
        f"SCHEMA_REQUIREMENT: {DEFAULT_SCHEMA_HINT}"
    )
    
    current_input = (
        f"INPUT_TASK: {raw_task[:4000]}\n"
        f"AVAILABLE_TOOLS: {json.dumps(available_tools)}\n"
        f"HISTORICAL_USE_CASES: {json.dumps(history['use_cases'])}\n"
        f"TOOL_CONSTRAINTS: {json.dumps(relevant_constraints)}"
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
            if is_valid and isinstance(result_data, dict) and "refined_strategy" in result_data and "argument_constraints" in result_data:
                return result_data
            
            error_feedback = f"PREVIOUS_FAILURE: {result_data}\nACTION: Fix JSON structure to include all required keys including 'argument_constraints' object."
            
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
