import subprocess
import json
import requests
import os
import re

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

import json
import subprocess

def process_text_and_execute_node(input_filepath):
    """
    Reads a text file, converts it to JSON, and executes a Node.js command with the JSON string.

    Args:
        input_filepath (str): The path to the input text file.
    """
    try:
        with open(input_filepath, 'r') as file:
            lines = file.readlines()

        data = {}
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    data[key] = value
                else:
                    print(f"Warning: Invalid line format: {line}")

        json_string = json.dumps(data)
        print(json_string)
        command = ["node", "cli.mjs", json_string]
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