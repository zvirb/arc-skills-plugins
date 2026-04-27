import os
import shutil
import json
import sys

source_dir = sys.argv[1] if len(sys.argv) > 1 else "/mnt/d/openClaw/Skills/"
dest_dir = os.path.expanduser("~/.openclaw/workspace/skills/")
config_path = os.path.expanduser("~/.openclaw/openclaw.json")

print("Deploying skills...")

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

skill_slugs = []

# 1. Copy and lowercase
for item in os.listdir(source_dir):
    src_path = os.path.join(source_dir, item)
    if os.path.isdir(src_path):
        slug = item.lower()
        skill_slugs.append(slug)
        dst_path = os.path.join(dest_dir, slug)
        
        # Remove existing if any
        if os.path.exists(dst_path):
            shutil.rmtree(dst_path)
            
        shutil.copytree(src_path, dst_path)
        print(f"Copied {item} -> {slug}")

# 2. Update config
print(f"Updating {config_path}...")
with open(config_path, "r") as f:
    config = json.load(f)

if "skills" not in config:
    config["skills"] = {}
if "entries" not in config["skills"]:
    config["skills"]["entries"] = {}

entries = config["skills"]["entries"]
added_count = 0

for slug in skill_slugs:
    if slug not in entries:
        entries[slug] = {"enabled": True}
        added_count += 1
    else:
        entries[slug]["enabled"] = True

# 3. Update Agents (Bind skills to main agent)
agent_updated_count = 0
if "agents" in config and "list" in config["agents"]:
    for agent in config["agents"]["list"]:
        if agent.get("id") == "main":
            if "skills" not in agent:
                agent["skills"] = []
            existing_skills = set(agent["skills"])
            for slug in skill_slugs:
                if slug not in existing_skills:
                    agent["skills"].append(slug)
                    agent_updated_count += 1
            agent["skills"] = sorted(list(set(agent["skills"])))

with open(config_path, "w") as f:
    json.dump(config, f, indent=2)

print(f"Updated config with {added_count} new entries. Bound {agent_updated_count} skills to main agent.")
print("Restarting gateway...")
os.system("systemctl --user restart openclaw-gateway.service")
print("Done.")
