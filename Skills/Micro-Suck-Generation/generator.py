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
    import os
    task = random.choice(TASKS)
    print("--- Micro-Suck Generated ---")
    print(f"Task: {task}")
    
    try:
        from composio import Composio
        composio = Composio(api_key=os.environ.get("COMPOSIO_API_KEY", "dummy"))
        result = composio.tools.execute(
            'GOOGLETASKS_INSERT_TASK',
            user_id='default',
            arguments={'title': f"[Micro-Suck] {task}"}
        )
        if result.successful:
            return {
                "status": "success",
                "task": task,
                "action": "injected_to_google_tasks"
            }
        else:
            return {
                "status": "failed",
                "error": result.error
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    result = generate_micro_suck()
    print(json.dumps(result, indent=2))
