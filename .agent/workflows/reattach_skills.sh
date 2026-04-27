#!/bin/bash
# Script to verify and re-attach ClawHub skills safely.
# It checks if a skill exists on the ClawHub registry, and if so, installs it and removes the manual unmanaged copy.

echo "Checking ClawHub for published skills..."
# Get all manual skill folders (they are capitalized in D:\openClaw\Skills)
for manual_dir in ~/.openclaw/workspace/skills/*; do
    if [ -d "$manual_dir" ]; then
        folder_name=$(basename "$manual_dir")
        # Skip if it's already managed (.clawhub exists) or hidden directories
        if [ -d "$manual_dir/.clawhub" ] || [[ "$folder_name" == .* ]]; then
            continue
        fi

        # Extract slug from SKILL.md (it's usually the folder name lowercased)
        slug=$(echo "$folder_name" | tr '[:upper:]' '[:lower:]')
        
        echo -n "Checking $slug... "
        
        # Try to install it directly. If it fails (404), it's not published yet.
        # We redirect output to avoid clutter, but we capture the exit status.
        if openclaw skills install "$slug" > /dev/null 2>&1; then
            echo "SUCCESS! Re-attached to ClawHub."
            # If the manual folder was capitalized and different from the slug, remove the manual one to prevent duplicates
            if [ "$folder_name" != "$slug" ]; then
                rm -rf "$manual_dir"
            fi
        else
            echo "Not on registry yet (Rate limit wait). Kept local copy."
        fi
    fi
done

echo "Done! Run 'openclaw skills update --all' to update all managed skills."
