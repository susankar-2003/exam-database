import os
import json
import urllib.parse

REPO_OWNER = "susankar-2003"
REPO_NAME = "exam-database"
BRANCH = "main"

live_files = {}

# Walk through all directories
for root, dirs, files in os.walk("."):
    # Skip git folders and hidden directories
    if ".git" in root or root.startswith("./."):
        continue
        
    for file in files:
        if file.endswith((".txt", ".zip")):
            # Construct the relative path
            path = os.path.relpath(os.path.join(root, file), ".")
            
            # URL encode the path to handle spaces and special characters safely
            url_path = urllib.parse.quote(path.replace("\\", "/"))
            
            # Create the raw download link
            raw_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{url_path}"
            
            # Save to our map
            live_files[file] = raw_url

# Load manual renames if the file exists
renames = {}
if os.path.exists("renames.json"):
    with open("renames.json", "r") as f:
        try:
            renames = json.load(f)
        except json.JSONDecodeError:
            pass

# Combine into master JSON
master_data = {
    "live_files": live_files,
    "renames": renames
}

with open("master_exams.json", "w") as f:
    json.dump(master_data, f, indent=4)
