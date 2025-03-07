# with open("q-multi-cursor-json.txt", "r") as file:
#     data = file.readlines()
#     data = ['"'+line.replace("\n","").replace('=','\":\"')+'"' for line in data]
#     output = ','.join(data)
#     output = '{'+output+'}'

# print(output)

# def process_zip_file(zip_filepath):
#     import os, zipfile, re, subprocess
#     from datetime import datetime

#     # Create a destination folder named "<zipfilename>_unzipped"
#     dest_dir = os.path.splitext(os.path.basename(zip_filepath))[0] + "_unzipped"
#     os.makedirs(dest_dir, exist_ok=True)

#     # Extract the ZIP file while preserving file timestamps.
#     with zipfile.ZipFile(zip_filepath, 'r') as zf:
#         for zi in zf.infolist():
#             extracted_path = zf.extract(zi, dest_dir)
#             mod_time = datetime(*zi.date_time).timestamp()
#             os.utime(extracted_path, (mod_time, mod_time))
    
#     # Replace all occurrences of "IITM" (any case) with "IIT Madras" in every file.
#     for root, _, files in os.walk(dest_dir):
#         for file in files:
#             file_path = os.path.join(root, file)
#             with open(file_path, 'rb') as f:
#                 data = f.read()
#             new_data = re.sub(b'iitm', b'IIT Madras', data, flags=re.IGNORECASE)
#             if new_data != data:
#                 with open(file_path, 'wb') as f:
#                     f.write(new_data)
    
#     # Run "cat * | sha256sum" in the destination folder and return its output.
#     output = subprocess.check_output("cat * | sha256sum", shell=True, cwd=dest_dir, text=True).strip()
#     return output

# output = process_zip_file('q-replace-across-files.zip')
# print(output)

# def process_zip_file(zip_filepath, min_size, min_date):
#     """
#     Processes the given ZIP file by:
#       - Extracting it into a folder named "<zipfilename>_unzipped" (preserving timestamps),
#       - Using 'ls -l --time-style=long-iso' to list files with their modification date and size,
#       - Filtering files that are at least min_size bytes and modified on or after min_date,
#       - Summing their sizes using an awk command.
    
#     Args:
#       zip_filepath (str): Path to the ZIP file.
#       min_size (int): Minimum file size in bytes.
#       min_date (str): Minimum modification date in the format "YYYY-MM-DD HH:MM" 
#                       (e.g., "1999-02-01 17:40").
    
#     Returns:
#       str: The output of the shell command (the total size of the matching files).
#     """
#     import os, zipfile, subprocess
#     from datetime import datetime

#     # Create destination folder "<zipfilename>_unzipped"
#     dest_dir = os.path.splitext(os.path.basename(zip_filepath))[0] + "_unzipped"
#     os.makedirs(dest_dir, exist_ok=True)

#     # Extract the ZIP file while preserving timestamps.
#     with zipfile.ZipFile(zip_filepath, 'r') as zf:
#         for zi in zf.infolist():
#             extracted_path = zf.extract(zi, dest_dir)
#             mod_time = datetime(*zi.date_time).timestamp()
#             os.utime(extracted_path, (mod_time, mod_time))
    
#     # Construct the shell command:
#     # Use ls with --time-style=long-iso to get ISO-like date format.
#     # awk filters files with size >= min_size and modification date/time >= min_date, then sums sizes.
#     cmd = f"""ls -l --time-style=long-iso | awk '$5>={min_size} && ($6" "$7)>= "{min_date}" {{sum+=$5}} END {{print sum}}'"""
    
#     # Run the shell command in the destination folder and return its output.
#     output = subprocess.check_output(cmd, shell=True, cwd=dest_dir, text=True).strip()
#     return output

# # Example usage:
# total_size = process_zip_file("q-list-files-attributes.zip", 8172, "1999-02-01 17:40")
# print(total_size)

# def move_rename_files(zip_filepath):
#     """
#     Processes the given ZIP file by:
#       - Extracting it into a folder named "<zipfilename>_unzipped" while preserving file timestamps,
#       - Moving all files (recursively) from the extracted folder into a new empty folder ("flat"),
#       - Renaming all files in the flat folder by replacing each digit with the next digit 
#         (with 9 wrapping to 0; e.g., a1b9c.txt becomes a2b0c.txt),
#       - Running the shell command "grep . * | LC_ALL=C sort | sha256sum" in that folder,
#       - Returning the output of the shell command.
    
#     Args:
#       zip_filepath (str): Path to the ZIP file.
    
#     Returns:
#       str: The output of the shell command.
#     """
#     import os, zipfile, subprocess, re, shutil
#     from datetime import datetime

#     # Determine destination folder based on zip filename.
#     base = os.path.splitext(os.path.basename(zip_filepath))[0]
#     dest_dir = base + "_unzipped"
#     if os.path.exists(dest_dir):
#         shutil.rmtree(dest_dir)
#     os.makedirs(dest_dir)

#     # Extract the ZIP file while preserving file timestamps.
#     with zipfile.ZipFile(zip_filepath, 'r') as zf:
#         for zi in zf.infolist():
#             extracted_path = zf.extract(zi, dest_dir)
#             mod_time = datetime(*zi.date_time).timestamp()
#             os.utime(extracted_path, (mod_time, mod_time))

#     # Create an empty "flat" folder inside dest_dir.
#     flat_dir = os.path.join(dest_dir, "flat")
#     os.makedirs(flat_dir, exist_ok=True)

#     # Move all files from the extracted directory tree into flat_dir.
#     for root, dirs, files in os.walk(dest_dir):
#         # Skip the flat directory itself.
#         if os.path.abspath(root) == os.path.abspath(flat_dir):
#             continue
#         for file in files:
#             source_path = os.path.join(root, file)
#             dest_path = os.path.join(flat_dir, file)
#             os.rename(source_path, dest_path)

#     # Rename all files in flat_dir: replace each digit with the next (9 -> 0).
#     def replace_digit(match):
#         digit = match.group()
#         return '0' if digit == '9' else str(int(digit) + 1)
    
#     for file in os.listdir(flat_dir):
#         old_path = os.path.join(flat_dir, file)
#         new_filename = re.sub(r'\d', replace_digit, file)
#         new_path = os.path.join(flat_dir, new_filename)
#         if new_filename != file:
#             os.rename(old_path, new_path)

#     # Run the shell command and capture its output.
#     output = subprocess.check_output(
#         "grep . * | LC_ALL=C sort | sha256sum",
#         shell=True, cwd=flat_dir, text=True
#     ).strip()
#     return output

# # Example usage:
# result = move_rename_files("q-move-rename-files.zip")
# print(result)

def compare_files(zip_filepath):
    """
    Processes the given ZIP file by:
      - Deleting the destination folder ("<zipfilename>_unzipped") if it exists,
      - Creating a new destination folder,
      - Extracting the ZIP file into that folder while preserving file timestamps,
      - Reading 'a.txt' and 'b.txt' from the folder,
      - Comparing the two files line by line to count how many lines differ,
      - Returning the count of differing lines.
    
    Args:
      zip_filepath (str): Path to the ZIP file.
    
    Returns:
      int: The number of lines that differ between a.txt and b.txt.
    """
    import os, zipfile, shutil
    from datetime import datetime

    # Determine destination folder based on the zip filename.
    base = os.path.splitext(os.path.basename(zip_filepath))[0]
    dest_dir = base + "_unzipped"
    
    # If the destination folder exists, delete it.
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    # Create a new destination folder.
    os.makedirs(dest_dir)

    # Extract the ZIP file while preserving timestamps.
    with zipfile.ZipFile(zip_filepath, 'r') as zf:
        for zi in zf.infolist():
            extracted_path = zf.extract(zi, dest_dir)
            mod_time = datetime(*zi.date_time).timestamp()
            os.utime(extracted_path, (mod_time, mod_time))

    # Define paths for a.txt and b.txt.
    a_path = os.path.join(dest_dir, "a.txt")
    b_path = os.path.join(dest_dir, "b.txt")

    # Compare the two files line by line.
    diff_count = 0
    with open(a_path, 'r') as fa, open(b_path, 'r') as fb:
        for line_a, line_b in zip(fa, fb):
            if line_a != line_b:
                diff_count += 1

    return diff_count

# Example usage:
diff_lines = compare_files('q-compare-files.zip')
print(diff_lines)