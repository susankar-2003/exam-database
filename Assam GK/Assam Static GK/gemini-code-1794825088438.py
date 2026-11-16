import re
import os
import tkinter as tk
from tkinter import filedialog

def format_question_papers():
    # Initialize tkinter and hide the main window
    root = tk.Tk()
    root.withdraw()
    
    # Open file dialog to select multiple text files
    print("Opening file dialog... Please select your files.")
    file_paths = filedialog.askopenfilenames(
        title="Select Question Paper Files",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    if not file_paths:
        print("No files selected. Exiting.")
        return

    # Process each selected file
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        formatted_lines = []
        for line in lines:
            # Check if the line is a multiple-choice option
            if re.match(r'^[A-D]\)', line.strip()):
                # Replace the parentheses around the text with a slash
                formatted_line = re.sub(r'\s*\(([^)]+)\)', r' / \1', line.rstrip())
                formatted_lines.append(formatted_line + '\n')
            else:
                # Keep all other lines exactly the same
                formatted_lines.append(line)

        # Overwrite the original file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(formatted_lines)
        
        # Extract just the file name for a cleaner print statement
        file_name = os.path.basename(file_path)
        print(f"Successfully updated: {file_name}")

    print("\nAll selected files have been processed!")

if __name__ == "__main__":
    format_question_papers()