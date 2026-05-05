import json
import os

config_path = os.path.expanduser('~/.openclaw/openclaw.json')
with open(config_path, 'r') as f:
    config = json.load(f)

# Update allowBundled
new_bundled = ["healthcheck", "diffs", "gog", "session-logs", "github", "weather", "wacli"]
config['skills']['allowBundled'] = list(set(config['skills'].get('allowBundled', []) + new_bundled))

# Update main agent skills
for agent in config['agents']['list']:
    if agent['id'] == 'main':
        new_skills = ["weather", "wacli"]
        agent['skills'] = list(set(agent.get('skills', []) + new_skills))

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
