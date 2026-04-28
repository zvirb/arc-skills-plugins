import unittest
import os
import re

class TestSkillIntegrity(unittest.TestCase):
    def setUp(self):
        self.skills_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Skills'))
        
    def get_all_skills(self):
        skills = []
        for d in os.listdir(self.skills_dir):
            if os.path.isdir(os.path.join(self.skills_dir, d)) and d != '__pycache__':
                skills.append(d)
        print(f"Found {len(skills)} skills in {self.skills_dir}")
        return skills

    def test_all_skills_have_skill_md(self):
        skills = self.get_all_skills()
        self.assertTrue(len(skills) > 0, "No skills found in the Skills directory")
        
        for skill in skills:
            skill_md_path = os.path.join(self.skills_dir, skill, 'SKILL.md')
            with self.subTest(skill=skill):
                self.assertTrue(os.path.exists(skill_md_path), f"Missing SKILL.md in {skill}")

    def test_skill_md_frontmatter_and_content(self):
        skills = self.get_all_skills()
        for skill in skills:
            skill_md_path = os.path.join(self.skills_dir, skill, 'SKILL.md')
            if not os.path.exists(skill_md_path):
                continue
                
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            with self.subTest(skill=skill):
                # Check for YAML frontmatter
                self.assertTrue(content.startswith('---'), f"{skill}/SKILL.md must start with YAML frontmatter (---)")
                
                parts = content.split('---')
                self.assertTrue(len(parts) >= 3, f"{skill}/SKILL.md must have a closing --- for frontmatter")
                
                frontmatter = parts[1]
                self.assertIn('name:', frontmatter, f"{skill}/SKILL.md frontmatter must contain 'name:'")
                self.assertIn('description:', frontmatter, f"{skill}/SKILL.md frontmatter must contain 'description:'")

if __name__ == '__main__':
    unittest.main()
