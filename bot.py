import os
import json
import urllib.parse

REPO_OWNER = "susankar-2003"
REPO_NAME = "exam-database"
BRANCH = "main"
DB_FILE = "paper_index.json"

def generate_download_url(path):
    # Ensure spaces and special characters are properly URL-encoded
    encoded_path = urllib.parse.quote(path)
    return f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{encoded_path}"

def main():
    # Load existing DB to preserve existing serial numbers
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            db = json.load(f)
    else:
        db = {"last_serial": 0, "papers": {}}

    # Create a reverse lookup dictionary: path -> paper_id
    existing_paths = {paper_data['path']: paper_id for paper_id, paper_data in db["papers"].items()}

    # Traverse the directory
    for root, _, files in os.walk("."):
        # Ignore git system files
        if ".git" in root:
            continue
        
        for file in files:
            if file.lower().endswith(('.txt', '.zip')):
                # Get the relative path (e.g., "Category/Exam1.txt")
                path = os.path.relpath(os.path.join(root, file), ".").replace("\\", "/")

                if path in existing_paths:
                    # Update name and URL in case they changed slightly
                    paper_id = existing_paths[path]
                    db["papers"][paper_id]["name"] = file
                    db["papers"][paper_id]["download_url"] = generate_download_url(path)
                else:
                    # Brand new file, assign the next serial number
                    db["last_serial"] += 1
                    new_id = str(db["last_serial"])
                    db["papers"][new_id] = {
                        "id": new_id,
                        "name": file,
                        "path": path,
                        "download_url": generate_download_url(path)
                    }

    # Save the updated database
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)
    print(f"Successfully synced {len(db['papers'])} papers to {DB_FILE}!")

if __name__ == "__main__":
    main()
