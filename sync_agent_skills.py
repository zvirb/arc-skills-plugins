import json
import os

config_path = os.path.expanduser("~/.openclaw/openclaw.json")
with open(config_path, "r") as f:
    config = json.load(f)

# Get all enabled skills
enabled_skills = []
for skill_name, skill_data in config.get("skills", {}).get("entries", {}).items():
    if skill_data.get("enabled", False):
        enabled_skills.append(skill_name)

# Ensure 'main' agent has all enabled skills
for agent in config.get("agents", {}).get("list", []):
    if agent.get("id") == "main":
        existing_skills = set(agent.get("skills", []))
        for skill in enabled_skills:
            if skill not in existing_skills:
                agent["skills"].append(skill)
                
        # Optional: sort them
        agent["skills"] = sorted(list(set(agent["skills"])))

with open(config_path, "w") as f:
    json.dump(config, f, indent=2)

print("Agent skills synced.")
