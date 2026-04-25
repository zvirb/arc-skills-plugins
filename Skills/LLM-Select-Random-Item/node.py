import sys
import json
import time
import subprocess

def validate_output(output_str):
    try:
        data = json.loads(output_str) if isinstance(output_str, str) else output_str
        return isinstance(data, dict) and "selected" in data
    except:
        return False

def execute_node(arguments_json_str, max_retries=3):
    try:
        arguments = json.loads(arguments_json_str)
    except:
        arguments = {"items": arguments_json_str} # Fallback if passed raw string

    items = arguments.get("items", [])
    prompt = f"From the following list of items, select one random item and output ONLY valid JSON in this format: {{'selected': 'item_text'}}. Items: {json.dumps(items)}"

    for attempt in range(1, max_retries + 1):
        print(f"Attempt {attempt}: Executing LLM Select Random Item transformation...")
        try:
            cmd = ["wsl", "--", "bash", "-c", f"openclaw infer '{prompt}'"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            clean_out = result.stdout.strip()
            if clean_out.startswith("```json"):
                clean_out = clean_out[7:]
            if clean_out.startswith("```"):
                clean_out = clean_out[3:]
            if clean_out.endswith("```"):
                clean_out = clean_out[:-3]
            clean_out = clean_out.strip()

            if validate_output(clean_out):
                return json.loads(clean_out)
        except Exception as e:
            print(f"OpenClaw Inference failed on attempt {attempt}: {e}")
            
        print("Validation failed or LLM hallucinated format. Retrying...")
        time.sleep(2)
        
    raise Exception("Failed to achieve valid JSON schema after max retries.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python node.py '<json_arguments>'")
        sys.exit(1)
    print(json.dumps(execute_node(sys.argv[1]), indent=2))
