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

# def compare_files(zip_filepath):
#     """
#     Processes the given ZIP file by:
#       - Deleting the destination folder ("<zipfilename>_unzipped") if it exists,
#       - Creating a new destination folder,
#       - Extracting the ZIP file into that folder while preserving file timestamps,
#       - Reading 'a.txt' and 'b.txt' from the folder,
#       - Comparing the two files line by line to count how many lines differ,
#       - Returning the count of differing lines.
    
#     Args:
#       zip_filepath (str): Path to the ZIP file.
    
#     Returns:
#       int: The number of lines that differ between a.txt and b.txt.
#     """
#     import os, zipfile, shutil
#     from datetime import datetime

#     # Determine destination folder based on the zip filename.
#     base = os.path.splitext(os.path.basename(zip_filepath))[0]
#     dest_dir = base + "_unzipped"
    
#     # If the destination folder exists, delete it.
#     if os.path.exists(dest_dir):
#         shutil.rmtree(dest_dir)
#     # Create a new destination folder.
#     os.makedirs(dest_dir)

#     # Extract the ZIP file while preserving timestamps.
#     with zipfile.ZipFile(zip_filepath, 'r') as zf:
#         for zi in zf.infolist():
#             extracted_path = zf.extract(zi, dest_dir)
#             mod_time = datetime(*zi.date_time).timestamp()
#             os.utime(extracted_path, (mod_time, mod_time))

#     # Define paths for a.txt and b.txt.
#     a_path = os.path.join(dest_dir, "a.txt")
#     b_path = os.path.join(dest_dir, "b.txt")

#     # Compare the two files line by line.
#     diff_count = 0
#     with open(a_path, 'r') as fa, open(b_path, 'r') as fb:
#         for line_a, line_b in zip(fa, fb):
#             if line_a != line_b:
#                 diff_count += 1

#     return diff_count

# # Example usage:
# diff_lines = compare_files('q-compare-files.zip')
# print(diff_lines)

# import requests
# from bs4 import BeautifulSoup

# # Replace with your URL
# url = 'https://exam.sanand.workers.dev/tds-2025-01-ga1'
# response = requests.get(url)

# # Parse the HTML
# soup = BeautifulSoup(response.content, 'html.parser')
# print(soup)
# # Find the first <input> tag with type="hidden"
# hidden_input = soup.find('input', {'type': 'hidden'})

# if hidden_input:
#     # Extract the value attribute
#     hidden_value = hidden_input.get('value')
#     print("Hidden input value:", hidden_value)
# else:
#     print("No hidden input found.")

promt = '''
You are a python developer and expert in google colab. There is a small mistake in this python code. Correct this code. Be concise, return the full corrected code as a json.

```python code
import numpy as np
from PIL import Image
from google.colab import files
import colorsys

# There is a mistake in the line below. Fix it
image = Image.open(list(files.upload().keys)[0])

rgb = np.array(image) / 255.0
lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x)[1], 2, rgb)
light_pixels = np.sum(lightness > 0.455)
print(f'Number of pixels with lightness > 0.455: {light_pixels}')
```

'''

import os
import requests
import re
import json

# Retrieve the token from an environment variable or replace with your token directly
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN", "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRhbmllbC5wdXR0YUBncmFtZW5lci5jb20ifQ.7ecKOqropYfrVXzrdflh5zKRh8JnYi3luH7x3qGKiIs")

url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AIPROXY_TOKEN}"
}

data = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "user", "content": promt}
    ]
}

response = requests.post(url, headers=headers, json=data)

# print("Status Code:", response.status_code)
# print("Response JSON:", response.json())
code_str = response.json()['choices'][0]['message']['content']
new_code_str = re.sub(r"```json|```","",code_str, re.IGNORECASE)
code_json = json.loads(new_code_str.strip())
print(code_json['code'])

# from PIL import Image

# def compress_image(input_path, output_path):
#     try:
#         # Open the image
#         img = Image.open(input_path)
        
#         # Save the image in WebP format with lossless compression.
#         # 'method=6' uses the slowest but most efficient compression.
#         img.save(output_path, format='WEBP', lossless=True, method=6)
#         print(f"Compressed image saved to {output_path}")
#     except Exception as e:
#         print("Error compressing image:", e)


# input_path = "shapes.png"
# output_path = "compressed_shapes.png"
# compress_image(input_path, output_path)