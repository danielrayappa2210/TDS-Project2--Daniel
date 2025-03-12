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

# promt_GA2_5 = '''
# You are a python developer and expert in google colab. There is a small mistake in this python code. Correct this code. Be concise, return the full corrected code as a json.

# ```python code
# import numpy as np
# from PIL import Image
# from google.colab import files
# import colorsys

# # There is a mistake in the line below. Fix it
# image = Image.open(list(files.upload().keys)[0])

# rgb = np.array(image) / 255.0
# lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x)[1], 2, rgb)
# light_pixels = np.sum(lightness > 0.455)
# print(f'Number of pixels with lightness > 0.455: {light_pixels}')
# ```

# '''

# import os
# import requests
# import re
# import json

# # Retrieve the token from an environment variable or replace with your token directly
# AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN", "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRhbmllbC5wdXR0YUBncmFtZW5lci5jb20ifQ.7ecKOqropYfrVXzrdflh5zKRh8JnYi3luH7x3qGKiIs")

# url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {AIPROXY_TOKEN}"
# }

# data = {
#     "model": "gpt-4o-mini",
#     "messages": [
#         {"role": "user", "content": prompt_GA1_2}
#     ]
# }

# response = requests.post(url, headers=headers, json=data)

# ========== for GA2_5 =================
# code_str = response.json()['choices'][0]['message']['content']
# new_code_str = re.sub(r"```json|```","",code_str, re.IGNORECASE)
# code_json = json.loads(new_code_str.strip())
# print(code_json['code'])

# ========================================

# import base64
# from io import BytesIO
# from PIL import Image

# def compress_and_encode_image(input_path):
#     """
#     Compress an image losslessly into WebP format and return a Base64 encoded data URI.
    
#     Parameters:
#       input_path (str): The file path to the source image.
      
#     Returns:
#       str: A Base64 encoded data URI of the compressed image.
#     """
#     # Open the input image
#     img = Image.open(input_path)
    
#     # Save the image in WebP format to an in-memory buffer using lossless compression with method=6
#     buffer = BytesIO()
#     img.save(buffer, format='WEBP', lossless=True, method=6)
    
#     # Get binary data from the buffer and encode it as Base64
#     binary_data = buffer.getvalue()
#     b64_data = base64.b64encode(binary_data).decode("utf-8")
    
#     # Construct and return the data URI
#     return f"data:image/webp;base64,{b64_data}"

# # Example usage:
# data_uri = compress_and_encode_image("shapes.png")
# print(data_uri)

# import os
# from datetime import datetime
# from github import Github

# def update_index_html(email):
#     """
#     Update the hard-coded index.html file in a hard-coded GitHub repository and branch.
    
#     This function writes two lines to the file:
#       1. An HTML comment with the provided email:
#          <!--email_off-->{email}<!--/email_off-->
#       2. The current date and time.
    
#     Parameters:
#       email (str): The email text to include in the file.
      
#     The GitHub token is read from the ACCESS_TOKEN environment variable.
#     """

#     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     new_content = f"<!--email_off-->{email}<!--/email_off-->\n{current_time}"

#     # Get token from environment variables
#     token = os.getenv("ACCESS_TOKEN")
#     if not token:
#         raise EnvironmentError("ACCESS_TOKEN environment variable is not set.")
    
#     # Hard-coded settings
#     repo_name = "danielrayappa2210/TDS-GA2"  # Replace with your GitHub username and repository name
#     branch = "main"
#     file_path = "index.html"
    
#     # Authenticate and get the repository
#     g = Github(token)
#     repos = g.get_user().get_repos()
#     repo = g.get_repo(repo_name)
    
#     # Retrieve the file to update (needed for its SHA)
#     file = repo.get_contents(file_path, ref=branch)
    
#     # Update the file with the new content
#     commit_message = "Update index.html via Python script"
#     update_response = repo.update_file(file.path, commit_message, new_content, file.sha, branch=branch)
    
#     return "https://danielrayappa2210.github.io/TDS-GA2/"

# # Example usage:

# email = "daniel.putta@gramener.com"
# gh_page_url = update_index_html(email)
# print(gh_page_url)

# ========================================

# import os
# import requests
# import base64
# import json

# def update_and_trigger_workflow(email):
#     """
#     Updates the GitHub Actions workflow file with the given email, 
#     commits the change using GitHub API, and triggers the workflow.
#     """
#     owner, repo, path, branch = "danielrayappa2210", "TDS", ".github/workflows/main.yml", "main"
#     token = os.getenv("ACCESS_TOKEN")
#     if not token: return print("Missing ACCESS_TOKEN")

#     headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"}
#     file_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

#     # Get file SHA
#     res = requests.get(file_url, headers=headers)
#     if res.status_code != 200: return print("Failed to get file SHA")
#     sha = res.json()["sha"]

#     # Format new YAML content
#     content = f"""on:\n  workflow_dispatch:\n\njobs:\n  test:\n    runs-on: ubuntu-latest\n    \n    steps:\n      - name: {email}\n        run: echo "Hello, world!"\n"""
#     encoded_content = base64.b64encode(content.encode()).decode()

#     # Update file
#     update_data = {"message": "Updated workflow", "content": encoded_content, "sha": sha, "branch": branch}
#     if requests.put(file_url, headers=headers, data=json.dumps(update_data)).status_code != 200:
#         return print("Failed to update file")

#     # Trigger workflow
#     trigger_url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/main.yml/dispatches"
#     if requests.post(trigger_url, json={"ref": branch}, headers=headers).status_code == 204:
#         return "https://github.com/danielrayappa2210/TDS"
#     else:
#         print("Failed to trigger workflow")


# gh_repo_url = update_and_trigger_workflow("user@example.com")
# print(gh_repo_url)

# ========================================

# import hashlib

# email = "daniel.putta@gramener.com"

# # Compute fake hash
# hashed_value = hashlib.sha256(f"{email} 2025".encode()).hexdigest()[-5:]
# print(f"Fake Hashed Value: {hashed_value}")

# ========================================

# import os
# import subprocess

# def build_and_push_image(tag):
#     # Read the Docker token from the environment.
#     token = os.getenv("DOCKER_TOKEN")
#     if not token:
#         raise EnvironmentError("DOCKER_TOKEN environment variable not set.")
    
#     # Hardcoded Docker Hub username and repository.
#     username = "danielrayappa"
#     repo = "tdsga"
#     image_tag = f"{username}/{repo}:{tag}"
    
#     # Log in to Docker Hub using your personal access token.
#     subprocess.run(["docker", "login", "--username", username, "--password", token], check=True)
    
#     # Build the Docker image from the current directory.
#     subprocess.run(["docker", "build", "-t", image_tag, "."], check=True)
    
#     # Push the Docker image to Docker Hub.
#     subprocess.run(["docker", "push", image_tag], check=True)
    
#     # Print the Docker Hub repository URL.
#     return f"https://hub.docker.com/repository/docker/{username}/{repo}/general"
    
# # Example usage:

# tag_input = "test"
# print(build_and_push_image(tag_input))

# ========================================

# from bs4 import BeautifulSoup

# def sum_data_values(html_path):
#     # Load the HTML file
#     with open(html_path, "r", encoding="utf-8") as file:
#         soup = BeautifulSoup(file, "html.parser")

#     # Find the hidden div with class 'd-none' and the exact title
#     hidden_element = soup.find("div", class_="d-none", title="This is the hidden element with the data-value attributes")

#     # Find all 'div' elements with class 'foo' inside the hidden div
#     foo_divs = hidden_element.find_all("div", class_="foo") if hidden_element else []

#     # Sum the data-value attributes
#     sum_value = sum(int(div.get("data-value", 0)) for div in foo_divs)

#     return sum_value

# # Call the function with the HTML file path
# print(sum_data_values("GA1.html"))

# ========================================

# from bs4 import BeautifulSoup

# def get_hidden_input_value(html_path):
#     # Load the HTML file
#     with open(html_path, "r", encoding="utf-8") as file:
#         soup = BeautifulSoup(file, "html.parser")

#     # Find the hidden input element with type="hidden" and disabled attribute
#     hidden_input = soup.find("input", {"type": "hidden", "disabled": True})

#     # Get the value attribute
#     input_value = hidden_input["value"] if hidden_input else None

#     return input_value

# # Call the function with the HTML file path
# print(get_hidden_input_value("GA1_daniel.html"))

# ========================================

# import re

# def excel_365_operations(formula):
#     # Extract arrays inside {}
#     arrays = re.findall(r"\{([^}]*)\}", formula)
#     array1 = list(map(int, arrays[0].split(','))) if len(arrays) > 0 else []
#     array2 = list(map(int, arrays[1].split(','))) if len(arrays) > 1 else []

#     # Extract standalone numbers (not inside arrays)
#     numbers = [int(num) for num in re.findall(r"[-]?\d+", formula)]
#     num3, num4 = numbers[-2:]  # Last two numbers (for TAKE function)

#     # SORTBY: Sort array1 based on values in array2
#     sorted_array = [x for _, x in sorted(zip(array2, array1))]

#     # TAKE: Take the first 'num4' elements after sorting
#     if num4 > 0:
#         taken_values = sorted_array[:num4]
#     elif num4 < 0:
#         taken_values = sorted_array[num4:]
#     else:
#         taken_values = []

#     # SUM: Compute sum of the taken values
#     result = sum(taken_values)

#     return result

# # Example usage
# formula = "=SUM(TAKE(SORTBY({10,6,10,9,11,2,7,15,11,12,6,14,2,9,2,12}, {10,9,13,2,11,8,16,14,7,15,5,4,6,1,3,12}), 1, 14))"
# final_sum = excel_365_operations(formula)

# print("Final SUM:", final_sum)

# ========================================

# import numpy as np
# from PIL import Image
# import colorsys

# def count_light_pixels(image_path, threshold):
#     rgb = np.array(Image.open(image_path)) / 255.0
#     lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x)[1], 2, rgb)
#     return np.sum(lightness > threshold)

# image_path = "lenna.webp"
# threshold = 0.455

# light_pixels = count_light_pixels(image_path, threshold)
# print(f"Number of pixels with lightness > {threshold}: {light_pixels}")

# ========================================

# import os
# import requests
# import base64
# import time

# def deploy_to_vercel(json_filepath):
#     """Creates and deployes an app in vercel to expose the data in the provided JSON file.

#     Args:
#         json_filepath (str): The local path to the JSON file containing student marks.

#     Returns:
#         str: The deployed Vercel API URL or None if deployment fails."
#     """


#     github_repo = "danielrayappa2210/TDS-vercel"
#     json_file = "q-vercel-python.json"
#     github_branch = "main"
#     access_token = os.getenv("ACCESS_TOKEN")

#     vercel_token = os.getenv("VERCEL_TOKEN")
#     vercel_deployments_api = "https://api.vercel.com/v6/deployments"

#     if not access_token or not vercel_token:
#         print("Missing GitHub access token or Vercel token")
#         return None

#     try:
#         headers = {"Authorization": f"Bearer {vercel_token}"}
#         initial_response = requests.get(vercel_deployments_api, headers=headers)
#         initial_data = initial_response.json()

#         existing_deployment_id = None
#         if "deployments" in initial_data and initial_data["deployments"]:
#             existing_deployment_id = initial_data["deployments"][0]["uid"]

#         if not os.path.exists(json_filepath):
#             print("JSON file not found")
#             return None

#         with open(json_filepath, "rb") as f:
#             json_content = f.read()
#         encoded_content = base64.b64encode(json_content).decode()

#         github_api_url = f"https://api.github.com/repos/{github_repo}/contents/{json_file}"
#         headers = {"Authorization": f"token {access_token}"}

#         response = requests.get(github_api_url, headers=headers)
#         if response.status_code == 200:
#             sha = response.json().get("sha")
#         else:
#             sha = None

#         commit_data = {
#             "message": "Update JSON file",
#             "content": encoded_content,
#             "branch": github_branch
#         }

#         if sha:
#             commit_data["sha"] = sha

#         response = requests.put(github_api_url, json=commit_data, headers=headers)
#         if response.status_code not in [200, 201]:
#             print("Failed to update GitHub")
#             return None

#         headers = {"Authorization": f"Bearer {vercel_token}"}

#         for _ in range(60):
#             response = requests.get(vercel_deployments_api, headers=headers)
#             data = response.json()

#             if "deployments" in data and data["deployments"]:
#                 latest_deploy = data["deployments"][0]
#                 status = latest_deploy["state"]
#                 deploy_id = latest_deploy["uid"]
#                 url = latest_deploy["url"]

#                 if deploy_id != existing_deployment_id:
#                     if status == "READY":
#                         print("Vercel deployment ready")
#                         return f"https://{url}/api"
#                     elif status in ["ERROR", "FAILED"]:
#                         print("Vercel deployment failed")
#                         return None

#             time.sleep(5)

#         print("Vercel deployment timed out")
#         return None

#     except requests.RequestException as e:
#         print("GitHub or Vercel API request failed")
#         return None

# json_filepath = "q-vercel-python1.json"
# vercel_url = deploy_to_vercel(json_filepath)
# print("Deployment URL:", vercel_url)

# # ========================================

# import requests
# import os

# repo = "danielrayappa2210/TDS-vercel"
# file_path = "q-vercel-python.json"
# token = os.getenv("ACCESS_TOKEN")  # Load token from environment variable

# if not token:
#     print("Error: ACCESS_TOKEN not set.")
#     exit()

# headers = {"Authorization": f"token {token}"}
# url = f"https://api.github.com/repos/{repo}/contents/{file_path}"

# response = requests.get(url, headers=headers)
# data = response.json()

# if response.status_code == 200:
#     print("SHA:", data.get("sha", "SHA not found"))
# else:
#     print("Error:", data)


