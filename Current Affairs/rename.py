import os
import re

def auto_rename_exam_papers_recursively(root_folder):
    # Matches the Assamese (Bengali script) Unicode block
    assamese_pattern = re.compile(r'[\u0985-\u09B9\u09CE-\u09DF\u09F0-\u09F1]')
    suffix = "_EA"
    
    renamed_count = 0
    skipped_count = 0
    error_count = 0
    
    # os.walk crawls the root_folder and ALL subfolders automatically
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.txt'):
                file_path = os.path.join(dirpath, filename)
                
                # Open and read the file
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                except Exception as e:
                    print(f"⚠️ Could not read {filename} in {dirpath}: {e}")
                    error_count += 1
                    continue
                
                # Check for Assamese characters
                has_assamese = bool(assamese_pattern.search(content))
                
                if has_assamese:
                    name_without_ext = filename[:-4] # Remove the '.txt'
                    
                    # Rename if it doesn't already have the suffix
                    if not name_without_ext.endswith(suffix):
                        new_filename = f"{name_without_ext}{suffix}.txt"
                        new_file_path = os.path.join(dirpath, new_filename)
                        
                        os.rename(file_path, new_file_path)
                        print(f"✅ Renamed: '{filename}' -> '{new_filename}'")
                        renamed_count += 1
                    else:
                        skipped_count += 1
                else:
                    skipped_count += 1

    # Print summary
    print("\n" + "="*40)
    print(f"Scan Summary:")
    print(f" - Files Renamed: {renamed_count}")
    print(f" - Files Skipped: {skipped_count} (Already named or English only)")
    if error_count > 0:
        print(f" - Errors:        {error_count}")

if __name__ == "__main__":
    print("CBT Go - Bulk Exam Renamer")
    print("="*40)
    print("Enter the full path to your main Exam Database folder.")
    print("Example: C:\\Users\\Name\\Desktop\\exam-database")
    print("(Or press Enter to scan the folder this script is currently inside)\n")
    
    user_input = input("Folder Path: ").strip()
    
    # Default to current directory if user just presses Enter
    TARGET_FOLDER = user_input if user_input else "."
    
    if os.path.exists(TARGET_FOLDER):
        print(f"\nStarting recursive scan in:\n{os.path.abspath(TARGET_FOLDER)}\n" + "="*40)
        auto_rename_exam_papers_recursively(TARGET_FOLDER)
        print("="*40 + "\nAll done!")
    else:
        print("❌ Error: The folder path you entered does not exist.")