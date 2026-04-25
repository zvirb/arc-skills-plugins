import json
import datetime

def groom_tasks():
    # Simulated Google Tasks API response
    tasks = [
        {"id": "1", "title": "Review old project docs", "updated": "2026-03-01T00:00:00Z"},
        {"id": "2", "title": "Buy groceries", "updated": "2026-04-20T00:00:00Z"}
    ]
    
    groomed = []
    print("--- Running Backlog Grooming ---")
    for t in tasks:
        # Mock logic to check age > 30 days
        if "2026-03" in t["updated"]:
            print(f"Task '{t['title']}' is stale. Grooming...")
            new_title = f"[STALE/ARCHIVED] {t['title']} (Summary: Blocked task)"
            groomed.append({"id": t["id"], "new_title": new_title, "action": "moved_to_archive"})
            
    return {
        "status": "success",
        "tasks_groomed": len(groomed),
        "details": groomed
    }

if __name__ == "__main__":
    result = groom_tasks()
    print(json.dumps(result, indent=2))
