import os
import json
import hashlib
import urllib.parse

REPO_OWNER = "susankar-2003"
REPO_NAME = "exam-database"
BRANCH = "main"
DB_FILE = "paper_index.json"

def generate_download_url(path):
    encoded_path = urllib.parse.quote(path)
    return f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{encoded_path}"

def get_file_hash(filepath):
    """Generates an MD5 hash of the file content to track renames/moves accurately."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except Exception:
        return None

def main():
    # Load existing database
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            db = json.load(f)
    else:
        db = {"last_serial": 0, "papers": {}}

    existing_papers = db["papers"]
    
    # Create lookup dictionaries from the existing database
    hash_to_id = {}
    path_to_id = {}
    
    for pid, pdata in existing_papers.items():
        if "hash" in pdata:
            hash_to_id[pdata["hash"]] = pid
        path_to_id[pdata["path"]] = pid

    current_found_ids = set()

    # Walk through repository directories
    for root, _, files in os.walk("."):
        if ".git" in root or ".github" in root:
            continue
        
        for file in files:
            if file.lower().endswith(('.txt', '.zip')):
                filepath = os.path.join(root, file)
                path = os.path.relpath(filepath, ".").replace("\\", "/")
                file_hash = get_file_hash(filepath)

                matched_id = None

                # Priority 1: Match by exact path (unchanged files)
                if path in path_to_id:
                    matched_id = path_to_id[path]
                
                # Priority 2: Match by file content hash (file was renamed or moved to a new folder)
                elif file_hash and file_hash in hash_to_id:
                    matched_id = hash_to_id[file_hash]

                if matched_id:
                    # Keep the exact same ID, but update name, path, link, and hash
                    existing_papers[matched_id]["name"] = file
                    existing_papers[matched_id]["path"] = path
                    existing_papers[matched_id]["download_url"] = generate_download_url(path)
                    existing_papers[matched_id]["hash"] = file_hash
                    current_found_ids.add(matched_id)
                else:
                    # Priority 3: Truly brand new file, assign the next serial number
                    db["last_serial"] += 1
                    new_id = str(db["last_serial"])
                    
                    existing_papers[new_id] = {
                        "id": new_id,
                        "name": file,
                        "path": path,
                        "download_url": generate_download_url(path),
                        "hash": file_hash
                    }
                    current_found_ids.add(new_id)

    # Save the updated database back to file
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)
        
    print(f"Successfully synced paper database. Total papers: {len(existing_papers)}")

if __name__ == "__main__":
    main()
