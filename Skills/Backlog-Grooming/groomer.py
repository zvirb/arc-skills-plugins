import json
import datetime

def groom_tasks():
    import os
    from datetime import datetime, timezone, timedelta
    
    print("--- Running Backlog Grooming ---")
    groomed = []
    
    try:
        from composio import Composio
        composio = Composio(api_key=os.environ.get("COMPOSIO_API_KEY", "dummy"))
        
        # 1. Fetch tasks
        list_result = composio.tools.execute(
            'GOOGLETASKS_LIST_TASKS',
            user_id='default',
            arguments={'tasklist': '@default', 'showHidden': True}
        )
        
        if not list_result.successful:
            return {"status": "error", "error": f"Failed to list tasks: {list_result.error}"}
            
        tasks = list_result.data.get('items', [])
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        
        # 2. Process tasks
        for t in tasks:
            # tasks updated format: 2026-03-01T00:00:00Z
            updated_str = t.get('updated', '')
            if not updated_str:
                continue
                
            try:
                # Handle standard ISO 8601 formatting with Z
                updated_date = datetime.strptime(updated_str.replace('Z', '+0000'), '%Y-%m-%dT%H:%M:%S.%f%z')
            except ValueError:
                try:
                    updated_date = datetime.strptime(updated_str.replace('Z', '+0000'), '%Y-%m-%dT%H:%M:%S%z')
                except ValueError:
                    continue
                    
            if updated_date < thirty_days_ago and not t.get('title', '').startswith('[STALE/ARCHIVED]'):
                print(f"Task '{t['title']}' is stale. Grooming...")
                new_title = f"[STALE/ARCHIVED] {t['title']}"
                
                # 3. Patch task
                patch_result = composio.tools.execute(
                    'GOOGLETASKS_PATCH_TASK',
                    user_id='default',
                    arguments={'tasklist': '@default', 'task': t['id'], 'title': new_title}
                )
                
                if patch_result.successful:
                    groomed.append({"id": t["id"], "new_title": new_title, "action": "patched"})
                else:
                    print(f"Failed to patch task {t['id']}: {patch_result.error}")
                    
        return {
            "status": "success",
            "tasks_groomed": len(groomed),
            "details": groomed
        }
        
    except Exception as e:
        print(f"Error during backlog grooming: {e}")
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    result = groom_tasks()
    print(json.dumps(result, indent=2))
