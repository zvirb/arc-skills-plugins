import subprocess
import json
import os
try:
    from composio import Composio
except ImportError:
    Composio = None

class WorkspaceManager:
    def __init__(self):
        self.composio_api_key = os.environ.get("COMPOSIO_API_KEY")

    def run_gog(self, args):
        """Helper to run the `gog` CLI."""
        try:
            cmd = ["wsl", "--", "bash", "-c", f"gog {' '.join(args)} --json"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except Exception as e:
            print(f"gog command failed: {e}")
            return None

    def search_emails(self, query):
        """Searches emails using gog, fallbacks to Composio."""
        print(f"Searching emails for: {query}")
        result = self.run_gog(["gmail", "search", f"'{query}'"])
        if result is not None:
            return result
        
        # Fallback
        if Composio:
            client = Composio(api_key=self.composio_api_key)
            res = client.tools.execute("GMAIL_SEARCH", arguments={"query": query})
            return res.data if res.successful else None
        return []

    def schedule_task(self, task_name, duration_minutes, due_date):
        """
        Retrieves calendar events, checks for conflicts, and schedules a task.
        In a real implementation, this would iterate backwards from due_date,
        find a free block of `duration_minutes`, and create an event.
        """
        print(f"Scheduling task '{task_name}' for {duration_minutes}m before {due_date}")
        
        # 1. Retrieve existing events (mock logic representing the check)
        events = self.run_gog(["calendar", "list", f"--before={due_date}"])
        if events is None:
            # Fallback
            events = []
            
        # 2. Logic to find free slot
        # (Assuming we found a free slot at 'calculated_time')
        calculated_time = "2026-04-26T10:00:00Z"
        
        # 3. Schedule it
        result = self.run_gog(["calendar", "create", f"--title='{task_name}'", f"--time={calculated_time}"])
        if result is not None:
            return result
            
        # Fallback
        if Composio:
            client = Composio(api_key=self.composio_api_key)
            res = client.tools.execute("GOOGLECALENDAR_CREATE_EVENT", arguments={"title": task_name, "start_time": calculated_time})
            return res.data if res.successful else None
        return {"status": "mocked", "time": calculated_time}

    def search_drive(self, query):
        """Searches Google Drive."""
        result = self.run_gog(["drive", "search", f"'{query}'"])
        if result is not None:
            return result
            
        if Composio:
            client = Composio(api_key=self.composio_api_key)
            res = client.tools.execute("GOOGLEDRIVE_SEARCH", arguments={"query": query})
            return res.data if res.successful else None
        return []

if __name__ == "__main__":
    manager = WorkspaceManager()
    print("Testing Email Search:", manager.search_emails("project update"))
    print("Testing Scheduling:", manager.schedule_task("Finish Report", 60, "2026-04-30"))
