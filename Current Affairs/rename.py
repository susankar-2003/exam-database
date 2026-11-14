import os
import re

def smart_rename_exam_papers(root_folder):
    # Matches the Assamese (Bengali script) Unicode block
    assamese_pattern = re.compile(r'[\u0985-\u09B9\u09CE-\u09DF\u09F0-\u09F1]')
    
    renamed_count = 0
    skipped_count = 0
    error_count = 0
    
    # os.walk crawls the root_folder and ALL subfolders automatically
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.txt'):
                file_path = os.path.join(dirpath, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                except Exception as e:
                    print(f"⚠️ Could not read {filename} in {dirpath}: {e}")
                    error_count += 1
                    continue
                
                has_assamese = bool(assamese_pattern.search(content))
                
                # 1. Strip the .txt extension to manipulate the name
                name_no_ext = filename[:-4]
                
                # 2. Extract the question count tag (e.g., "25Q", "100Q") if it exists
                q_match = re.search(r'_(\d+Q)', name_no_ext, flags=re.IGNORECASE)
                q_tag = q_match.group(1).upper() if q_match else None
                
                # 3. Clean the base name by removing ANY existing _EA or _XXQ tags
                # This fixes files that were already named poorly (like "_25Q_EA")
                base_name = re.sub(r'_(?i)EA\b', '', name_no_ext)
                base_name = re.sub(r'_\d+(?i)Q\b', '', base_name)
                base_name = base_name.rstrip('_') # Clean up any trailing underscores
                
                # 4. Rebuild the perfect filename
                new_name_no_ext = base_name
                
                if has_assamese:
                    new_name_no_ext += "_EA"
                    
                if q_tag:
                    new_name_no_ext += f"_{q_tag}"
                    
                new_filename = new_name_no_ext + ".txt"
                
                # 5. Rename if the new formatted name is different from the original
                if filename != new_filename:
                    new_file_path = os.path.join(dirpath, new_filename)
                    os.rename(file_path, new_file_path)
                    print(f"✅ Fixed: '{filename}'  ->  '{new_filename}'")
                    renamed_count += 1
                else:
                    skipped_count += 1

    # Print summary
    print("\n" + "="*50)
    print(f"Scan Summary:")
    print(f" - Files Re-arranged/Renamed: {renamed_count}")
    print(f" - Files Perfect/Skipped:     {skipped_count}")
    if error_count > 0:
        print(f" - Errors:                    {error_count}")
    print("="*50)

if __name__ == "__main__":
    print("CBT Go - Smart Bulk Exam Renamer")
    print("="*50)
    print("Enter the full path to your main Exam Database folder.")
    print("Example: C:\\Users\\Name\\Desktop\\exam-database")
    print("(Or press Enter to scan the folder this script is currently inside)\n")
    
    user_input = input("Folder Path: ").strip()
    TARGET_FOLDER = user_input if user_input else "."
    
    if os.path.exists(TARGET_FOLDER):
        print(f"\nStarting smart scan in:\n{os.path.abspath(TARGET_FOLDER)}\n" + "-"*50)
        smart_rename_exam_papers(TARGET_FOLDER)
    else:
        print("❌ Error: The folder path you entered does not exist.")