import json
import os

path = os.path.expanduser('~/.openclaw/openclaw.json')
with open(path, 'r') as f:
    data = json.load(f)

data['skills']['allowBundled'] = ["healthcheck", "diffs", "gog", "session-logs", "github", "weather", "wacli"]
for agent in data['agents']['list']:
    if agent['id'] == 'main':
        agent['skills'] = list(set(agent['skills'] + ["weather", "wacli"]))

with open(path, 'w') as f:
    json.dump(data, f, indent=2)
