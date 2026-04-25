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

# Add parent directory to sys.path to import Shared modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from Shared.utils import validate_json_output as validate_output

# ==========================================
# EXECUTION LOGIC (ATOMIC)
# ==========================================
def refine_tool_use(arguments_json_str):
    # 1. Standardized Input
    try:
        arguments = json.loads(arguments_json_str)
    except:
        arguments = {"task_description": arguments_json_str}

    raw_task = arguments.get("task_description", "")
    
    # 2. Kaizen: Blindfold the LLM
    system_prompt = (
        "ROLE: Tool Prioritization Refiner.\n"
        "TASK: Refine the input task description into a strict tool selection strategy.\n"
        "RULES:\n"
        "1. Prioritize specific tools (e.g., view_file, grep_search, write_to_file) over generic terminal commands.\n"
        "2. Explicitly avoid using 'cat' or 'grep' inside bash commands.\n"
        "3. Output ONLY raw JSON matching the schema. No markdown wrapping.\n"
        f"SCHEMA_REQUIREMENT: {DEFAULT_SCHEMA_HINT}"
    )
    
    current_input = f"INPUT_TASK: {raw_task[:4000]}"
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
