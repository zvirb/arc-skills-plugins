import sys
import json
import time
import subprocess
import os

# ==========================================
# STANDARDIZED WORK: CONFIGURATION & SCHEMAS
# ==========================================
MAX_RETRIES = 3
DEFAULT_SCHEMA = {
    "summary": "string",
    "key_points": ["string"],
    "sentiment": "string"
}

# Add parent directory to sys.path to import Shared modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from Shared.utils import validate_json_output as validate_output

# ==========================================
# EXECUTION LOGIC (ATOMIC)
# ==========================================
def execute_node(arguments_json_str):
    # 1. Standardized Input Parsing
    try:
        arguments = json.loads(arguments_json_str)
    except:
        arguments = {"text": arguments_json_str}

    raw_text = arguments.get("text", "")
    schema_hint = arguments.get("schema", json.dumps(DEFAULT_SCHEMA))
    
    # 2. Kaizen: Blindfold the LLM (Constrained System Prompt)
    system_prompt = (
        "ROLE: Data Transformation Node.\n"
        "TASK: Summarize text into structured JSON.\n"
        f"SCHEMA: {schema_hint}\n"
        "RULES: Output ONLY raw JSON. No conversational text. No markdown blocks."
    )
    
    current_prompt = f"TEXT TO PROCESS: {raw_text[:3000]}"
    error_feedback = ""

    # 3. Jidoka: The "Andon" Loop (Self-Healing)
    for attempt in range(1, MAX_RETRIES + 1):
        instruction = f"{system_prompt}\n\n{error_feedback}\n\n{current_prompt}"
        
        try:
            # Atomic Execution (No-Shell Pattern)
            cmd = ["wsl", "openclaw", "infer", "model", "run", "--local", "--prompt", instruction]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            if result.returncode != 0:
                error_feedback = f"PROVIDER_ERROR: {result.stderr or 'Process failed'}"
                continue

            # Evaluation
            is_valid, result_data = validate_output(result.stdout)
            
            if is_valid:
                return result_data
            
            # Error Feedback (Andon)
            error_feedback = f"PREVIOUS_ERROR: {result_data}\nINSTRUCTION: Correct the JSON and try again."
            
        except Exception as e:
            error_feedback = f"SYSTEM_EXCEPTION: {str(e)}"
            
        time.sleep(1)

    # 4. Deterministic Exit
    return {
        "status": "error",
        "message": f"Failed to achieve valid state after {MAX_RETRIES} attempts.",
        "last_error": error_feedback
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Missing input arguments."}))
        sys.exit(1)
    
    print(json.dumps(execute_node(sys.argv[1]), indent=2))
