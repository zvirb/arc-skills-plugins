import sys
import json
import time
import subprocess
import os

# ==========================================
# STANDARDIZED WORK: CONFIGURATION & SCHEMAS
# ==========================================
MAX_RETRIES = 3
DEFAULT_SCHEMA_HINT = "A valid JSON object mapping keys to extracted entities."

# ==========================================
# JIDOKA: EVALUATOR & VALIDATION
# ==========================================
def validate_output(output_str):
    """
    Evaluator Pattern: Deterministic validation of LLM output.
    Returns (is_valid, data_or_error_message)
    """
    try:
        # Strip potential markdown artifacts if they slipped through
        clean = output_str.strip()
        if clean.startswith("```"):
            lines = clean.splitlines()
            if lines[0].startswith("```"): lines = lines[1:]
            if lines[-1].startswith("```"): lines = lines[:-1]
            clean = "\n".join(lines).strip()
        
        data = json.loads(clean)
        if not isinstance(data, dict):
            return False, "Output must be a JSON object ({...})."
        return True, data
    except json.JSONDecodeError as e:
        return False, f"JSON Decode Error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected validation failure: {str(e)}"

# ==========================================
# EXECUTION LOGIC (ATOMIC)
# ==========================================
def execute_node(arguments_json_str):
    # 1. Standardized Input
    try:
        arguments = json.loads(arguments_json_str)
    except:
        arguments = {"text": arguments_json_str}

    raw_text = arguments.get("text", "")
    schema_hint = arguments.get("schema", DEFAULT_SCHEMA_HINT)
    
    # 2. Kaizen: Blindfold the LLM
    system_prompt = (
        "ROLE: Extraction Node.\n"
        "TASK: Extract entities from text into JSON.\n"
        f"SCHEMA_REQUIREMENT: {schema_hint}\n"
        "RULES: Output ONLY raw JSON. No intro/outro. No markdown."
    )
    
    current_input = f"INPUT_TEXT: {raw_text[:4000]}"
    error_feedback = ""

    # 3. Jidoka: Andon Loop
    for attempt in range(1, MAX_RETRIES + 1):
        instruction = f"{system_prompt}\n\n{error_feedback}\n\n{current_input}"
        
        try:
            # Atomic Execution (No-Shell Pattern)
            # Calling wsl directly with a list avoids bash-specific escaping issues
            cmd = ["wsl", "openclaw", "infer", "model", "run", "--local", "--prompt", instruction]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            if result.returncode != 0:
                error_feedback = f"PROVIDER_ERROR: {result.stderr or 'Process failed'}"
                continue

            is_valid, result_data = validate_output(result.stdout)
            if is_valid:
                return result_data
            
            error_feedback = f"PREVIOUS_FAILURE: {result_data}\nACTION: Fix JSON and re-extract."
            
        except Exception as e:
            error_feedback = f"SYSTEM_EXCEPTION: {str(e)}"
            
        time.sleep(1)

    # 4. Deterministic Failure
    return {
        "status": "error",
        "message": f"Extraction failed after {MAX_RETRIES} attempts.",
        "final_error": error_feedback
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Missing input."}))
        sys.exit(1)
    
    print(json.dumps(execute_node(sys.argv[1]), indent=2))
