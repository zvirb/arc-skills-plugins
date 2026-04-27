import os, re

def fix_files():
    for root, _, files in os.walk('d:/openClaw/Skills'):
        for file in files:
            if file == 'SKILL.md':
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = re.sub(r'(?m)^os:\s*windows', 'os: all', content)
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {path}")

if __name__ == '__main__':
    fix_files()
