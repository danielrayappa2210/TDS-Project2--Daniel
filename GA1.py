import subprocess
import json
import requests
import os
import re
import shutil

def run_uv(email_address):
    """
    Runs an HTTP request to httpbin.org with the given email address.

    Args:
        email_address: The email address to include in the request.

    Returns:
        A tuple containing (return_code, json_output, error_message).
        return_code: The exit code of the command (integer).
        json_output: The parsed JSON output (dictionary) or None.
        error_message: An error message (string) or None.
    """
    command_list = ["uv", "run", "--with", "httpie", "--", "https", "https://httpbin.org/get", f"email=={email_address}"]

    try:
        process = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            check=False,
        )
        stdout = process.stdout.strip() if process.stdout else ""
        stderr = process.stderr.strip() if process.stderr else ""
        return_code = process.returncode

        if return_code == 0:
            try:
                json_output = json.loads(stdout)
                return return_code, json_output, None
            except json.JSONDecodeError:
                return return_code, None, "Command output is not valid JSON."
        else:
            return return_code, None, stderr

    except Exception as e:
        return -1, None, str(e)

# Example usage:
email_to_use = "daniel.putta@gramener.com"
return_code, json_output, error_message = run_uv(email_to_use)

if return_code == 0:
    print("Request successful!")
    print(json.dumps(json_output, indent=4))
    print(f"Email from response: {json_output['args']['email']}")

elif error_message:
    print(f"Request failed with return code: {return_code}")
    print(f"Error: {error_message}")

else:
    print(f"Request failed with return code: {return_code}")

# ====================================================================================================================

def run_prettier():
    """
    Runs prettier on README.md and calculates its SHA256 checksum.

    This function executes the command "npx -y prettier@3.4.2 README.md | sha256sum"
    using the system shell. It formats the README.md file with prettier and then
    calculates the SHA256 checksum of the formatted output.

    Returns:
        A tuple containing (return_code, output, error_message).
        return_code: The exit code of the command (integer).
        output: The SHA256 checksum string (string) or the standard output if any.
        error_message: An error message (string) or an empty string if no error occurred.
    """
    command_string = "npx -y prettier@3.4.2 README.md | sha256sum"

    try:
        process = subprocess.run(
            command_string,
            capture_output=True,
            text=True,
            check=False,
            shell=True,  # Enable shell interpretation
        )
        stdout = process.stdout.strip() if process.stdout else ""
        stderr = process.stderr.strip() if process.stderr else ""
        return_code = process.returncode

        return return_code, stdout, stderr
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1, "", str(e)

return_code, output, error_message = run_prettier()

if return_code == 0:
    print(output)
else:
    print(f"Request failed with return code: {return_code}")

# ====================================================================================================================

def calculate_formula_in_sheet(web_app_url, formula):
    """
    Puts a formula in A1, computes in B1, and returns the result.

    Args:
        web_app_url: The URL of your Google Apps Script web app.
        formula: The formula string.

    Returns:
        The computed result, or None if an error occurs.
    """
    try:
        data = {"formula": formula}
        headers = {"Content-Type": "application/json"}
        response = requests.post(web_app_url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        print("Raw Response:", response.text)  # Add this line
        result = response.json().get("result")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None

# Example usage:
web_app_url = "https://script.google.com/macros/s/AKfycbzqSnAvZWmFgIrqofWolaflgaeiRz1Vi6toM1-EXX5fDCF6SffZMwV_hvs0i9VHLVs5/exec"  # Replace with your web app URL
formula = "=SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 4, 0), 1, 10))"
result = calculate_formula_in_sheet(web_app_url, formula)

if result is not None:
    print(f"Result of formula '{formula}': {result}")

# ====================================================================================================================

import openpyxl
from xlcalculator import Model, parser, Evaluator

def evaluate_formula_string(formula_string):
    """
    Evaluates an Excel formula string directly.

    Args:
        formula_string (str): The Excel formula as a string (e.g., "=SUM(A1:A10)").

    Returns:
        The result of the formula evaluation, or None if an error occurs.
    """
    try:
        model = Model()
        parser = parser(model)
        parser.parse("=SUM(1,2,3)") #Very simple formula.
        evaluator = Evaluator(model)
        result = evaluator.evaluate("A1", {})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
# formula_to_evaluate = "=SUM(TAKE(SORTBY({10,6,10,9,11,2,7,15,11,12,6,14,2,9,2,12}, {10,9,13,2,11,8,16,14,7,15,5,4,6,1,3,12}), 1, 14))" #example of your formula

# result = evaluate_formula_string(formula_to_evaluate)

# if result is not None:
#     print(f"The result of the formula is: {result}")
# else:
#     print("Could not evaluate the formula.")

# Example of a simpler formula
simple_formula = "=SUM(1,2,3)"
simple_result = evaluate_formula_string(simple_formula)
if simple_result is not None:
    print(f"The result of the simple formula is: {simple_result}")
else:
    print("Could not evaluate the formula.")

# ====================================================================================================================

import datetime

def count_days_in_range(start_date_str, end_date_str, target_day_name):
    """
    Counts the number of occurrences of a specific day of the week within a given date range.

    Args:
        start_date_str: The start date in 'YYYY-MM-DD' format.
        end_date_str: The end date in 'YYYY-MM-DD' format.
        target_day_name: The name of the day of the week (e.g., "Monday", "Wednesday").

    Returns:
        The number of occurrences of the target day within the date range.
    """

    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        target_day_index = day_names.index(target_day_name)

        count = 0
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() == target_day_index:
                count += 1
            current_date += datetime.timedelta(days=1)

        return count

    except ValueError:
        return "Invalid date format or day name."

# Example usage:
start_date = "1988-12-05"
end_date = "2010-05-02"
target_day = "Wednesday"

result = count_days_in_range(start_date, end_date, target_day)
print(f"Number of {target_day}s between {start_date} and {end_date}: {result}")

start_date2 = "2023-01-01"
end_date2 = "2023-12-31"
target_day2 = "Sunday"

result2 = count_days_in_range(start_date2, end_date2, target_day2)
print(f"Number of {target_day2}s between {start_date2} and {end_date2}: {result2}")

# ====================================================================================================================

import zipfile
import os
import pandas as pd

def extract_answer_from_zip(zip_file_path):
    """
    Unzips a zip file, reads a CSV within it, and extracts the 'answer' column.

    Args:
        zip_file_path (str): The path to the zip file.

    Returns:
        list: A list of values from the 'answer' column, or None if an error occurs.
    """
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # Extract all files to a temporary directory
            temp_dir = "temp_unzipped"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            zip_ref.extractall(temp_dir)

            # Find the CSV file (assuming only one CSV exists)
            csv_file_path = None
            for filename in os.listdir(temp_dir):
                if filename.lower().endswith(".csv"):
                    csv_file_path = os.path.join(temp_dir, filename)
                    break

            if csv_file_path:
                # Read the CSV using pandas
                df = pd.read_csv(csv_file_path)

                # Extract the 'answer' column
                if 'answer' in df.columns:
                    answers = df['answer'].tolist()

                    # Clean up the temporary directory
                    for filename in os.listdir(temp_dir):
                        file_path = os.path.join(temp_dir, filename)
                        os.remove(file_path)
                    os.rmdir(temp_dir)

                    return answers
                else:
                    print("Error: 'answer' column not found in the CSV.")
                    # Clean up the temporary directory
                    for filename in os.listdir(temp_dir):
                        file_path = os.path.join(temp_dir, filename)
                        os.remove(file_path)
                    os.rmdir(temp_dir)
                    return None

            else:
                print("Error: No CSV file found in the zip archive.")
                # Clean up the temporary directory
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    os.remove(file_path)
                os.rmdir(temp_dir)
                return None

    except FileNotFoundError:
        print(f"Error: Zip file not found at {zip_file_path}")
        return None
    except zipfile.BadZipFile:
        print(f"Error: {zip_file_path} is not a valid zip file.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
        # Clean up the temporary directory
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            os.remove(file_path)
        os.rmdir(temp_dir)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Clean up the temporary directory
        if os.path.exists(temp_dir):
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                os.remove(file_path)
            os.rmdir(temp_dir)
        return None
    
zip_file_path = "q-extract-csv-zip.zip"  # Replace with your zip file path
answers = extract_answer_from_zip(zip_file_path)

if answers:
    print("Answers:", answers)
else:
    print("Failed to extract answers.")

# ====================================================================================================================

def sort_json_array(json_string):
    """
    Sorts a JSON array of objects by age, then by name in case of a tie.

    Args:
        json_string: A JSON string representing an array of objects.

    Returns:
        A JSON string representing the sorted array, without spaces or newlines.
    """
    try:
        data = json.loads(json_string)
        sorted_data = sorted(data, key=lambda x: (x.get("age"), x.get("name")))
        return json.dumps(sorted_data, separators=(',', ':'))
    except json.JSONDecodeError:
        return "Invalid JSON"

# Example Usage (replace with your JSON string):
json_data = '[{"name":"Alice","age":26},{"name":"Bob","age":10},{"name":"Charlie","age":72},{"name":"David","age":56},{"name":"Emma","age":55},{"name":"Frank","age":54},{"name":"Grace","age":56},{"name":"Henry","age":18},{"name":"Ivy","age":36},{"name":"Jack","age":9},{"name":"Karen","age":95},{"name":"Liam","age":86},{"name":"Mary","age":97},{"name":"Nora","age":11},{"name":"Oscar","age":22},{"name":"Paul","age":84}]'
sorted_json = sort_json_array(json_data)
print(sorted_json)

# ====================================================================================================================

import json
import subprocess

def process_text_and_execute_node(input_filepath):
    """
    Reads a text file, converts it to JSON, and executes a Node.js command with the JSON string.

    Args:
        input_filepath (str): The path to the input text file.
    """
    try:
        with open("q-multi-cursor-json.txt", "r") as file:
            data = file.readlines()
            data = ['"'+line.replace("\n","").replace('=','\":\"')+'"' for line in data]
            output = ','.join(data)
            output = '{'+output+'}'

        command = ["node", "cli.mjs", output]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            print("Node.js command executed successfully.")
            print("Output:", result.stdout)
        else:
            print("Node.js command failed.")
            print("Error:", result.stderr)

    except FileNotFoundError:
        print(f"Error: File not found at {input_filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_filepath = "q-multi-cursor-json.txt"

process_text_and_execute_node(input_filepath)

# ====================================================================================================================

import zipfile
import csv
import io

def sum_values_for_symbols(zip_file_path, target_symbols):
    """
    Downloads and processes files from a zip archive, summing values for specified symbols.

    Args:
        zip_file_path (str): Path to the zip file.
        target_symbols (list or set): A list or set of symbols to search for.

    Returns:
        int: Sum of values associated with the target symbols.
    """

    target_symbols = set(target_symbols)  # Convert to set for efficient lookup
    total_sum = 0

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            # Process data1.csv (CP-1252)
            with zip_file.open('data1.csv') as file1:
                decoded_file1 = io.TextIOWrapper(file1, encoding='cp1252')
                reader1 = csv.reader(decoded_file1)
                for row in reader1:
                    if len(row) == 2 and row[0] in target_symbols:
                        try:
                            total_sum += int(row[1])
                        except ValueError:
                            pass

            # Process data2.csv (UTF-8)
            with zip_file.open('data2.csv') as file2:
                decoded_file2 = io.TextIOWrapper(file2, encoding='utf-8')
                reader2 = csv.reader(decoded_file2)
                for row in reader2:
                    if len(row) == 2 and row[0] in target_symbols:
                        try:
                            total_sum += int(row[1])
                        except ValueError:
                            pass

            # Process data3.txt (UTF-16)
            with zip_file.open('data3.txt') as file3:
                decoded_file3 = io.TextIOWrapper(file3, encoding='utf-16')
                reader3 = csv.reader(decoded_file3, delimiter='\t')
                for row in reader3:
                    if len(row) == 2 and row[0] in target_symbols:
                        try:
                            total_sum += int(row[1])
                        except ValueError:
                            pass

    except FileNotFoundError:
        print(f"Error: Zip file not found at {zip_file_path}")
    except KeyError as e:
        print(f"Error: File not found in zip archive: {e}")
    except zipfile.BadZipFile:
        print(f"Error: Invalid zip file: {zip_file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return total_sum

# Example Usage:
zip_file_path = 'q-unicode-data.zip'  # Replace with your zip file path.
target_symbols = ['‡', '‹', '—']
result = sum_values_for_symbols(zip_file_path, target_symbols)
print(f"Sum of values: {result}")

target_symbols2 = ['‡', 'A'] #example of a different set of symbols.
result2 = sum_values_for_symbols(zip_file_path, target_symbols2)
print(f"Sum of values for target symbols 2: {result2}")

# ====================================================================================================================

import requests
import json
import secrets
import os

try:
    token = secrets.ACCESS_TOKEN
    print(f"Token: {token}")
except KeyError:
    print("Error: ACCESS_TOKEN not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

def update_github_email_json_api(github_username, repo_name, email_id):
    """
    Updates the email.json file in a GitHub repository using the GitHub API.

    Args:
        github_username (str): Your GitHub username.
        repo_name (str): The name of your GitHub repository.
        email_id (str): The email address to add to the JSON.

    Returns:
        str: The raw GitHub URL of email.json, or None if an error occurs.
    """
    try:
        github_token = secrets.ACCESS_TOKEN
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        # Get the file's SHA and content
        api_url = f"https://api.github.com/repos/{github_username}/{repo_name}/contents/email.json"
        print(f"Fetching file from: {api_url}") # Debug print
        response = requests.get(api_url, headers=headers)
        print(f"Response status code: {response.status_code}") # Debug print
        response.raise_for_status()
        file_data = response.json()
        sha = file_data["sha"]
        content = file_data["content"]
        decoded_content = json.loads(requests.compat.unquote(content).encode('utf-8').decode('utf-8'))

        # Update the email
        decoded_content["email"] = email_id

        # Commit the changes
        commit_data = {
            "message": "Updated email_id",
            "content": requests.compat.quote(json.dumps(decoded_content).encode('utf-8')),
            "sha": sha,
            "branch": "main",
        }
        print(f"Committing changes to: {api_url}") # Debug print
        response = requests.put(api_url, headers=headers, json=commit_data)
        print(f"Response status code: {response.status_code}") # Debug print
        response.raise_for_status()

        raw_url = f"https://raw.githubusercontent.com/{github_username}/{repo_name}/main/email.json"
        return raw_url

    except requests.exceptions.RequestException as e:
        print(f"Error during GitHub API request: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
    except KeyError as e:
        print(f"Key error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

# Example usage:
repo_path = "https://github.com/danielrayappa2210/TDS"
github_username = "danielrayappa2210"
email_id = "test@example.com"
url = update_github_email_json_api(repo_path, github_username, email_id)
if url:
    print(f"Raw GitHub URL: {url}")

# ====================================================================================================================

def replace_across_files(zip_filepath):
    """
    Processes the given ZIP file by:
      - Extracting it into a folder named "<zipfilename>_unzipped" while preserving file timestamps,
      - Recursively replacing all occurrences of "IITM" (in any case) with "IIT Madras" in all files,
      - Running the shell command 'cat * | sha256sum' in the extracted folder,
      - Returning the output of the shell command (the SHA256 checksum).

    Args:
      zip_filepath (str): Path to the ZIP file to process.

    Returns:
      str: The output of the 'cat * | sha256sum' command (i.e., the SHA256 checksum).
    """
    import os, zipfile, re, subprocess
    from datetime import datetime

    # Create a destination folder named "<zipfilename>_unzipped"
    dest_dir = os.path.splitext(os.path.basename(zip_filepath))[0] + "_unzipped"
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    # Extract the ZIP file while preserving file timestamps.
    with zipfile.ZipFile(zip_filepath, 'r') as zf:
        for zi in zf.infolist():
            extracted_path = zf.extract(zi, dest_dir)
            mod_time = datetime(*zi.date_time).timestamp()
            os.utime(extracted_path, (mod_time, mod_time))
    
    # Replace all occurrences of "IITM" (any case) with "IIT Madras" in every file.
    for root, _, files in os.walk(dest_dir):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                data = f.read()
            new_data = re.sub(b'iitm', b'IIT Madras', data, flags=re.IGNORECASE)
            if new_data != data:
                with open(file_path, 'wb') as f:
                    f.write(new_data)
    
    # Run "cat * | sha256sum" in the destination folder and return its output.
    output = subprocess.check_output("cat * | sha256sum", shell=True, cwd=dest_dir, text=True).strip()
    return output

output = replace_across_files('q-replace-across-files.zip')
print(output)

# ====================================================================================================================

def list_files_and_attributes(zip_filepath, min_size, min_date):
    """
    Processes the given ZIP file by:
      - Extracting it into a folder named "<zipfilename>_unzipped" (preserving timestamps),
      - Using 'ls -l --time-style=long-iso' to list files with their modification date and size,
      - Filtering files that are at least min_size bytes and modified on or after min_date,
      - Summing their sizes using an awk command.
    
    Args:
      zip_filepath (str): Path to the ZIP file.
      min_size (int): Minimum file size in bytes.
      min_date (str): Minimum modification date in the format "YYYY-MM-DD HH:MM" 
                      (e.g., "1999-02-01 17:40").
    
    Returns:
      str: The output of the shell command (the total size of the matching files).
    """
    import os, zipfile, subprocess
    from datetime import datetime

    # Create destination folder "<zipfilename>_unzipped"
    dest_dir = os.path.splitext(os.path.basename(zip_filepath))[0] + "_unzipped"
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    # Extract the ZIP file while preserving timestamps.
    with zipfile.ZipFile(zip_filepath, 'r') as zf:
        for zi in zf.infolist():
            extracted_path = zf.extract(zi, dest_dir)
            mod_time = datetime(*zi.date_time).timestamp()
            os.utime(extracted_path, (mod_time, mod_time))
    
    # Construct the shell command:
    # Use ls with --time-style=long-iso to get ISO-like date format.
    # awk filters files with size >= min_size and modification date/time >= min_date, then sums sizes.
    cmd = f"""ls -l --time-style=long-iso | awk '$5>={min_size} && ($6" "$7)>= "{min_date}" {{sum+=$5}} END {{print sum}}'"""
    
    # Run the shell command in the destination folder and return its output.
    output = subprocess.check_output(cmd, shell=True, cwd=dest_dir, text=True).strip()
    return output

# Example usage:
total_size = list_files_and_attributes("q-list-files-attributes.zip", 8172, "1999-02-01 17:40")
print(total_size)

# ====================================================================================================================

def move_rename_files(zip_filepath):
    """
    Processes the given ZIP file by:
      - Extracting it into a folder named "<zipfilename>_unzipped" while preserving file timestamps,
      - Moving all files (recursively) from the extracted folder into a new empty folder ("flat"),
      - Renaming all files in the flat folder by replacing each digit with the next digit 
        (with 9 wrapping to 0; e.g., a1b9c.txt becomes a2b0c.txt),
      - Running the shell command "grep . * | LC_ALL=C sort | sha256sum" in that folder,
      - Returning the output of the shell command.
    
    Args:
      zip_filepath (str): Path to the ZIP file.
    
    Returns:
      str: The output of the shell command.
    """
    import os, zipfile, subprocess, re, shutil
    from datetime import datetime

    # Determine destination folder based on zip filename.
    base = os.path.splitext(os.path.basename(zip_filepath))[0]
    dest_dir = base + "_unzipped"
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    # Extract the ZIP file while preserving file timestamps.
    with zipfile.ZipFile(zip_filepath, 'r') as zf:
        for zi in zf.infolist():
            extracted_path = zf.extract(zi, dest_dir)
            mod_time = datetime(*zi.date_time).timestamp()
            os.utime(extracted_path, (mod_time, mod_time))

    # Create an empty "flat" folder inside dest_dir.
    flat_dir = os.path.join(dest_dir, "flat")
    os.makedirs(flat_dir, exist_ok=True)

    # Move all files from the extracted directory tree into flat_dir.
    for root, dirs, files in os.walk(dest_dir):
        # Skip the flat directory itself.
        if os.path.abspath(root) == os.path.abspath(flat_dir):
            continue
        for file in files:
            source_path = os.path.join(root, file)
            dest_path = os.path.join(flat_dir, file)
            os.rename(source_path, dest_path)

    # Rename all files in flat_dir: replace each digit with the next (9 -> 0).
    def replace_digit(match):
        digit = match.group()
        return '0' if digit == '9' else str(int(digit) + 1)
    
    for file in os.listdir(flat_dir):
        old_path = os.path.join(flat_dir, file)
        new_filename = re.sub(r'\d', replace_digit, file)
        new_path = os.path.join(flat_dir, new_filename)
        if new_filename != file:
            os.rename(old_path, new_path)

    # Run the shell command and capture its output.
    output = subprocess.check_output(
        "grep . * | LC_ALL=C sort | sha256sum",
        shell=True, cwd=flat_dir, text=True
    ).strip()
    return output

# Example usage:
result = move_rename_files("q-move-rename-files.zip")
print(result)

# ====================================================================================================================

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