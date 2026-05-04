import json
import os
import sys
import shutil

CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
BACKUP_PATH = CONFIG_PATH + ".bak.manual"

def deep_update(data, filter_fn, path=""):
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            new_path = f"{path}.{k}" if path else k
            new_dict[k] = deep_update(v, filter_fn, new_path)
        return new_dict
    elif isinstance(data, list):
        new_list = []
        for i, item in enumerate(data):
            new_path = f"{path}[{i}]"
            new_list.append(deep_update(item, filter_fn, new_path))
        return new_list
    else:
        # Leaf value
        if not filter_fn(path):
            return data
        
        # Skip some obviously non-user-editable stuff unless in full mode
        if any(skip in path for skip in ["meta", "wizard"]) and "full" not in sys.argv:
            return data

        print(f"\n--- {path} ---")
        print(f"Current value: {data}")
        
        # Suggest env var if key looks like an API key
        key_name = path.split(".")[-1]
        env_suggestion = os.environ.get(key_name.upper()) or os.environ.get(path.replace(".", "_").upper())
        if env_suggestion and env_suggestion != data:
            print(f"Found environment variable suggestion: {env_suggestion}")
            prompt = f"Use suggestion? (y/n/manual, default keep current): "
        else:
            prompt = f"Enter new value (or press Enter to keep current): "

        choice = input(prompt).strip()
        
        if choice == "" or choice.lower() == "n":
            return data
        if choice.lower() == "y" and env_suggestion:
            return env_suggestion
        
        val = choice if choice.lower() != "manual" else input("Enter value: ").strip()
        
        if val.lower() == "true": return True
        if val.lower() == "false": return False
        try:
            if "." in val: return float(val)
            return int(val)
        except ValueError:
            return val

def main():
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: {CONFIG_PATH} not found.")
        return

    print(f"Reading config from {CONFIG_PATH}")
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    print("\nOpenClaw Configuration Manager")
    print("===============================")
    print("This script will walk through your configuration and allow you to update keys.")
    print("Press Enter at any prompt to leave the value unchanged.")
    
    print("\nSelect mode:")
    print("1. Sensitive & API Keys (Default)")
    print("2. Environment Variables (env.vars)")
    print("3. Full Walkthrough (Expert)")
    
    mode = input("\nChoice (1/2/3): ").strip() or "1"
    
    if mode == "1":
        filter_fn = lambda p: any(x in p.lower() for x in ["key", "token", "auth", "pass", "secret"])
    elif mode == "2":
        filter_fn = lambda p: "env.vars" in p
    else:
        filter_fn = lambda p: True

    # Backup before saving
    shutil.copy2(CONFIG_PATH, BACKUP_PATH)
    print(f"\nBackup created at {BACKUP_PATH}")

    updated_config = deep_update(config, filter_fn)

    with open(CONFIG_PATH, "w") as f:
        json.dump(updated_config, f, indent=2)
    
    print(f"\nConfiguration updated and saved to {CONFIG_PATH}")
    print("You may need to restart OpenClaw services for changes to take effect.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(0)
