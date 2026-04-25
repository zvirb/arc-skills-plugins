import json
import os
import shlex
import subprocess
try:
    from composio import Composio
except ImportError:
    Composio = None

def get_decomposition_prompt(vague_task):
    return f"""You are an expert productivity coach and technical project manager. 
Your goal is to break down the following vague task into 3-5 distinct, actionable Google Tasks.
Make sure the tasks are phrased as direct actions starting with a verb.

Vague Task: "{vague_task}"

Output exactly a JSON array of strings, where each string is a clear, actionable subtask.
Do not output markdown formatting, just the raw JSON array.
"""

def decompose_task(vague_task):
    """
    Decomposes a vague task into actionable Google Tasks by constructing a tailored prompt
    and running it via the OpenClaw CLI.
    """
    prompt = get_decomposition_prompt(vague_task)
    
    # Run the LLM inference via OpenClaw CLI
    try:
        command = [
            "wsl", "--", "bash", "-c", 
            f"openclaw infer model run --prompt {shlex.quote(prompt)} --json"
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Parse the output assuming openclaw returns a JSON response containing the text
        response_data = json.loads(result.stdout)
        # Extract the assistant's reply (which should be our JSON array of strings)
        llm_reply = response_data.get("response", "[]")
        
        # Clean markdown wrappers if any exist
        if llm_reply.startswith("```json"):
            llm_reply = llm_reply.replace("```json\\n", "").replace("\\n```", "")
            
        subtasks = json.loads(llm_reply)
        return subtasks
    except Exception as e:
        print(f"Error during OpenClaw inference: {e}")
        # Fallback for testing/failure
        return [f"Analyze requirements for: {vague_task[:20]}...", "Draft implementation plan"]

def push_to_google_tasks(subtasks):
    """
    Sends tasks to Google Tasks via Composio SDK.
    """
    if Composio is None:
        print("Composio SDK not installed. Returning mocked results.")
        return [f"Created Google Task (Mocked): {task}" for task in subtasks]
        
    composio = Composio(api_key=os.environ.get("COMPOSIO_API_KEY", "dummy"))
    results = []
    
    for task in subtasks:
        try:
            # Execute the GOOGLETASKS_INSERT_TASK action
            result = composio.tools.execute(
                'GOOGLETASKS_INSERT_TASK',
                user_id='default',
                arguments={'title': task}
            )
            if result.successful:
                results.append(f"Created Google Task: {task}")
            else:
                results.append(f"Failed to create Google Task: {task} - {result.error}")
        except Exception as e:
            results.append(f"Exception creating Google Task '{task}': {e}")
            
    return results

if __name__ == "__main__":
    task = "Build a new CRM integration"
    subtasks = decompose_task(task)
    print(push_to_google_tasks(subtasks))
