import json

# ==========================================
# JIDOKA: SHARED EVALUATORS
# ==========================================

def validate_json_output(output_str, expected_schema=None):
    """
    Evaluator Pattern: Deterministic validation of LLM JSON output.
    Returns (is_valid, data_or_error_message)
    """
    try:
        # Strip potential markdown artifacts if they slipped through
        clean = output_str.strip()
        if clean.startswith("```"):
            lines = clean.splitlines()
            if lines and lines[0].startswith("```"): lines = lines[1:]
            if lines and lines[-1].startswith("```"): lines = lines[:-1]
            clean = "\n".join(lines).strip()
        
        data = json.loads(clean)
        
        # Basic structural check - ensure it's a dict
        if not isinstance(data, dict):
            return False, "Output must be a JSON object ({...}), not a list or primitive."
        
        return True, data
    except json.JSONDecodeError as e:
        return False, f"JSON Decode Error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected validation failure: {str(e)}"

def validate_json_array_output(output_str):
    """
    Evaluator Pattern: Deterministic validation of LLM JSON array output.
    Returns (is_valid, data_or_error_message)
    """
    try:
        # Strip potential markdown artifacts
        clean = output_str.strip()
        if clean.startswith("```"):
            lines = clean.splitlines()
            if lines and lines[0].startswith("```"): lines = lines[1:]
            if lines and lines[-1].startswith("```"): lines = lines[:-1]
            clean = "\n".join(lines).strip()
        
        data = json.loads(clean)
        
        # Basic structural check - ensure it's a list
        if not isinstance(data, list):
            return False, "Output must be a JSON array ([...]), not an object or primitive."
        
        return True, data
    except json.JSONDecodeError as e:
        return False, f"JSON Decode Error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected validation failure: {str(e)}"


def evaluate_tool_output(result_obj, tool_name):
    """
    Evaluator Pattern: Checks if an API tool actually succeeded in its objective.
    Returns (is_valid, data_or_error)
    """
    if not result_obj:
        return False, f"{tool_name} returned empty response."
    
    # Check for common Google API error indicators
    error_msg = result_obj.get("error", {}).get("message", "")
    if error_msg:
        return False, f"API Error: {error_msg}"
    
    # Success check: API returned data correctly
    if any(key in result_obj for key in ["spreadsheetId", "updates", "id", "title"]):
        return True, result_obj
        
    return False, f"{tool_name} response lacks recognizable success markers (e.g. 'id', 'spreadsheetId')."
