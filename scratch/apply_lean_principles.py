import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Skills"))

LEAN_HEADER = """
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.
"""

for skill_name in os.listdir(base_dir):
    skill_path = os.path.join(base_dir, skill_name)
    if os.path.isdir(skill_path):
        md_path = os.path.join(skill_path, "SKILL.md")
        if os.path.exists(md_path):
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Find the YAML end or the first H1
            if LEAN_HEADER not in content:
                # Insert after the first # header or after YAML
                parts = content.split("---", 2)
                if len(parts) == 3:
                    new_content = f"---{parts[1]}---{LEAN_HEADER}\n{parts[2]}"
                else:
                    new_content = f"{LEAN_HEADER}\n{content}"
                
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {skill_name}/SKILL.md with Lean Principles.")

print("All SKILL.md files updated.")
