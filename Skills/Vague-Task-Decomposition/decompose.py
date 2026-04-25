import json
import os
import shlex

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
    Decomposes a vague task into actionable Google Tasks by constructing a tailored prompt.
    """
    prompt = get_decomposition_prompt(vague_task)
    
    # Simulating the LLM inference that would normally use openclaw infer or an SDK
    # e.g., result = subprocess.run(["wsl", "openclaw", "infer", "model", "run", "--prompt", prompt, "--json"])
    
    print(f"--- Sending Prompt to LLM ---\n{prompt}\n-----------------------------")
    
    # Mocked LLM JSON response parsing
    subtasks = [
        f"Analyze requirements for: {vague_task[:20]}...",
        "Draft implementation plan",
        "Execute and test"
    ]
    return subtasks

def push_to_google_tasks(subtasks):
    """
    Simulates sending tasks to Google Tasks via Composio.
    """
    results = []
    for task in subtasks:
        # Avoid concatenating raw shell strings, use shlex.quote if running a command
        safe_task = shlex.quote(task)
        # Mock execution
        results.append(f"Created Google Task: {task}")
    return results

if __name__ == "__main__":
    task = "Build a new CRM integration"
    subtasks = decompose_task(task)
    print(push_to_google_tasks(subtasks))
