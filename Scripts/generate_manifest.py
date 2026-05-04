import os

skills_dir = '/home/marku/.openclaw/workspace/skills/'
manifest_path = os.path.join(skills_dir, 'MANIFEST.md')

with open(manifest_path, 'w') as f:
    f.write('# OpenClaw Skill Manifest\n\n')
    f.write('| Skill Name | Description |\n')
    f.write('| :--- | :--- |\n')
    
    for d in sorted(os.listdir(skills_dir)):
        skill_path = os.path.join(skills_dir, d, 'SKILL.md')
        if os.path.isfile(skill_path):
            try:
                with open(skill_path, 'r') as sf:
                    content = sf.read()
                    desc = "No description provided"
                    if content.startswith('---'):
                        parts = content.split('---')
                        if len(parts) >= 3:
                            for line in parts[1].split('\n'):
                                if 'description:' in line:
                                    desc = line.split('description:')[1].strip().strip('"').strip("'")
                                    break
                    f.write(f'| {d} | {desc} |\n')
            except Exception as e:
                print(f'Error reading {d}: {e}')
