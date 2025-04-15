import os

def count_lines_in_file(filepath):
   """Counts the number of lines in a file."""
   try:
      with open(filepath, 'r', encoding='utf-8') as file:
         return sum(1 for _ in file)
   except (UnicodeDecodeError, OSError):
      return 0

def find_python_files_with_line_counts(directory):
   """Finds all .py files in a directory and counts their lines."""
   python_files = []
   for root, dirs, files in os.walk(directory):
      # Skip .venv directories
      if '.venv' in root.split(os.sep):
         continue

      for file in files:
         if file.endswith('.py'):
            filepath = os.path.join(root, file)
            line_count = count_lines_in_file(filepath)
            python_files.append((file, line_count, filepath))
   return sorted(python_files, key=lambda x: x[1], reverse=True)

def display_table(python_files):
   """Displays .py files and their line counts in a table."""
   total_lines = sum(line_count for _, line_count, _ in python_files)
   print("{:<30} {:<10} {:<50}".format("File Name", "Lines", "Path"))
   print("=" * 90)
   for file, line_count, filepath in python_files:
      print("{:<30} {:<10} {:<50}".format(file, line_count, filepath))
   print("=" * 90)
   print(f"Total Lines: {total_lines}")

if __name__ == "__main__":
   current_directory = os.getcwd()
   python_files = find_python_files_with_line_counts(current_directory)
   display_table(python_files)
