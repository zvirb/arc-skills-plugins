import json
import random

TASKS = [
    "Clear the physical desktop",
    "Drink a glass of water",
    "Stand up and stretch for 2 minutes",
    "Organize one folder on your computer",
    "Delete 5 unnecessary emails"
]

def generate_micro_suck():
    task = random.choice(TASKS)
    print("--- Micro-Suck Generated ---")
    print(f"Task: {task}")
    
    return {
        "status": "success",
        "task": task,
        "action": "injected_to_google_tasks"
    }

if __name__ == "__main__":
    result = generate_micro_suck()
    print(json.dumps(result, indent=2))
