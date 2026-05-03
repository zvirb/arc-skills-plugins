---
name: kebab-case-auto-fix
description: One-time setup for ClawCoach AI health coaching.
os: all
requires:
  bins: []
---

# ClawCoach Setup

This skill directs the agent to perform the initial configuration of the ClawCoach health coaching system.

## Execution Directives

1. **Verify Existing Profile:** Execute `read_file` on `~/.clawcoach/profile.json`. If the file exists and the user has not requested a reset, report that setup is complete and switch to `clawcoach-core`.
2. **Initialize Environment:** If `~/.clawcoach/` does not exist, execute `run_shell_command` to create the directory.
3. **Collect Profile Data:** Guide the user through a sequential inquiry process to obtain: `Name`, `Age`, `Gender`, `Height`, `Weight`, `Goal`, and `Activity Level`.
4. **Calculate Targets:** 
   - Apply the Mifflin-St Jeor equation (as defined in `SKILL.md` logic) to determine BMR.
   - Multiply by the activity factor and adjust based on the user's goal.
   - Calculate macro targets (1.8g protein/kg, 25% fat, remainder carbs).
5. **Establish Preferences:** Inquire about dietary restrictions, allergies, and food dislikes.
6. **Assign Persona:** Present "Supportive Mentor" and "Savage Roaster" options. Record the user's choice.
7. **Commit Profile:** Execute `write_file` to save the collected JSON object to `~/.clawcoach/profile.json`. Initialize `~/.clawcoach/food-log.json` with an empty meals array.
8. **Handover:** Deliver an introductory message in the chosen persona voice and transition to `clawcoach-core`.

## Expected Output
A confirmation message stating that the profile has been saved and coaching is initialized.
