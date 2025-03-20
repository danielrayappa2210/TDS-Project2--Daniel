# GA1 function description
GA1_tools = [
    {
        "type": "function",
        "function": {
            "name": "run_code_status",
            "description": "Executes the 'code -s' command in the terminal (or Command Prompt) to retrieve the status of Visual Studio Code.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_uv",
            "description": "Runs an HTTP request to httpbin.org with the given email address.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_address": {
                        "type": "string",
                        "description": "The email address to include in the request."
                    }
                },
                "required": [
                    "email_address"
                ],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_prettier",
            "description": "Formats the specified README file using Prettier and calculates its SHA-256 checksum.",
            "parameters": {
                "type": "object",
                "properties": {
                    "readme_file_path": {
                        "type": "string",
                        "description": "The file path of the README file to format."
                    }
                },
                "required": [
                    "readme_file_path"
                ],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_formula_in_google_sheet",
            "description": "Puts a formula in a google sheet at A1 cell, computes in B1, and returns the result from B1.",
            "parameters": {
                "type": "object",
                "properties": {
                    "formula": {
                        "type": "string",
                        "description": "The formula string."
                    }
                },
                "required": [
                    "formula"
                ],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_formula_in_excel_365_sheet",
            "description": "Evaluates a given Excel formula and returns its output by inserting the provided formula into an Excel sheet, calculating its result, and retrieving the output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "formula": {
                        "type": "string",
                        "description": "The Excel formula to be evaluated as a string."
                    }
                },
                "required": [
                    "formula"
                ],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_hidden_input_value",
            "description": "Extracts the value of a hidden input field from an HTML file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "html_path": {
                        "type": "string",
                        "description": "The path to the HTML file containing the hidden input field."
                    }
                },
                "required": [
                    "html_path"
                ],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_days_in_range",
            "description": "Counts the number of occurrences of a specific day of the week within a given date range.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date_str": {
                        "type": "string",
                        "description": "The start date in 'YYYY-MM-DD' format."
                    },
                    "end_date_str": {
                        "type": "string",
                        "description": "The end date in 'YYYY-MM-DD' format."
                    },
                    "target_day_name": {
                        "type": "string",
                        "description": "The name of the day of the week (e.g., 'Monday', 'Wednesday')."
                    }
                },
                "required": [
                    "start_date_str",
                    "end_date_str",
                    "target_day_name"
                ],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_answer_from_csv",
            "description": "Extracts and returns the value from the 'answer' column in the extract.csv file inside a given ZIP archive.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_file_path": {
                        "type": "string",
                        "description": "The file path to the ZIP archive."
                    }
                },
                "required": [
                    "zip_file_path"
                ],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sort_json_by_age_and_name",
            "description": "Sorts a JSON array of objects by the 'age' field in ascending order and by the 'name' field alphabetically in case of a tie.",
            "parameters": {
                "type": "object",
                "properties": {
                    "json_string": {
                        "type": "string",
                        "description": "The input JSON string containing an array of objects."
                    }
                },
                "required": [
                    "json_string"
                ],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_txt_to_json_and_hash",
            "description": "Reads a text file containing key=value pairs, converts it into a JSON object, and computes its hash using an online tool.",
            "parameters": {
                "type": "object",
                "properties": {
                    "txt_filepath": {
                        "type": "string",
                        "description": "The file path to the text file containing key=value pairs."
                    }
                },
                "required": [
                    "txt_filepath"
                ],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sum_data_values_of_divs",
            "description": "Parses an HTML file, finds all <div> elements with the class 'foo' inside a hidden element, and sums their 'data-value' attributes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "html_path": {
                        "type": "string",
                        "description": "The file path to the HTML file."
                    }
                },
                "required": ["html_path"],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sum_values_for_symbols",
            "description": "Reads and processes three differently encoded files, summing values for specific symbols across all files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_file_path": {
                        "type": "string",
                        "description": "The file path to the directory containing the data files."
                    },
                    "target_symbols": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "A list of symbols to filter and sum values for."
                    }
                },
                "required": ["zip_file_path", "target_symbols"],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_github_repo_and_push_json",
            "description": "Automates the process of creating a GitHub repository, committing a JSON file, and pushing it to GitHub.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_id": {
                        "type": "string",
                        "description": "The email address to be stored in the JSON file."
                    }
                },
                "required": ["email_id"],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "replace_iitm_and_compute_sha256",
            "description": "Extracts a ZIP archive, replaces all occurrences of 'IITM' (case-insensitive) with 'IIT Madras' in all files, and computes the SHA-256 checksum of the concatenated file contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_filepath": {
                        "type": "string",
                        "description": "The file path to the ZIP archive."
                    }
                },
                "required": ["zip_filepath"],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files_and_attributes",
            "description": "Processes the given ZIP file by extracting it into a folder, listing files with their modification date and size, filtering files that are at least min_size bytes and modified on or after min_date, and summing their sizes using an awk command.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_filepath": {
                        "type": "string",
                        "description": "Path to the ZIP file."
                    },
                    "min_size": {
                        "type": "integer",
                        "description": "Minimum file size in bytes."
                    },
                    "min_date": {
                        "type": "string",
                        "description": "Minimum modification date in the format 'YYYY-MM-DD HH:MM' (e.g., '1999-02-01 17:40')."
                    }
                },
                "required": [
                    "zip_filepath",
                    "min_size",
                    "min_date"
                ],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "move_rename_files",
            "description": "Processes the given ZIP file by extracting it, moving all files into a new flat folder, renaming files by incrementing each digit (with 9 wrapping to 0), and running a shell command to compute the SHA-256 hash of the sorted file contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_filepath": {
                        "type": "string",
                        "description": "Path to the ZIP file."
                    }
                },
                "required": [
                    "zip_filepath"
                ],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_files",
            "description": "Processes the given ZIP file by extracting it, reading 'a.txt' and 'b.txt', comparing them line by line, and returning the count of differing lines.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_filepath": {
                        "type": "string",
                        "description": "Path to the ZIP file."
                    }
                },
                "required": [
                    "zip_filepath"
                ],
                "additionalProperties": false
            },
            "strict": true
        }
    }
]

# GA2 function description
GA2_tools = 
[
    {
        "type": "function",
        "function": {
            "name": "documentation_markdown",
            "description": "Generates a Markdown-formatted analysis of daily step counts over a week, comparing trends over time and with friends. It reads the Markdown content from a file and outputs it.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compress_and_encode_image",
            "description": "Compresses an image losslessly to ensure it remains under 1,500 bytes while preserving all pixel data, encodes it as Base64, and returns a data URI of the compressed image.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "The file path to the original image."
                    }
                },
                "required": ["input_path"],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_index_html",
            "description": "Updates the index.html file in a GitHub repository with new content that includes an HTML comment with the provided email and the current date and time, and returns the GitHub URL of the updated file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email text to include in the file."
                    }
                },
                "required": ["email"],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_colab_authentication",
            "description": "Authenticates a user in Colab using the provided email, retrieves user info, and returns a hashed value based on the email and a fixed string.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email address to authenticate and grant access to Google Colab."
                    }
                },
                "required": ["email"],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_image_library_colab",
            "description": "Processes an image in a Google Colab environment by loading it, converting to grayscale, and counting the number of pixels with brightness values greater than or equal to the given threshold.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "The file path to the image."
                    },
                    "threshold": {
                        "type": "integer",
                        "description": "The minimum brightness value (0-255) to consider a pixel as 'bright.'"
                    }
                },
                "required": ["image_path", "threshold"],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "deploy_to_vercel",
            "description": "Creates and deploys an app in Vercel to expose data from a provided JSON file by updating a file in a GitHub repository, and returns the deployed Vercel API URL or None if deployment fails.",
            "parameters": {
                "type": "object",
                "properties": {
                    "json_filepath": {
                        "type": "string",
                        "description": "The local path to the JSON file containing student marks."
                    }
                },
                "required": ["json_filepath"],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_and_trigger_workflow",
            "description": "Creates a GitHub Action in a repository with a step that includes the provided email ID. It creates the workflow file, commits it, and triggers the action, then returns the repository URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email address to include in the GitHub Action step name."
                    }
                },
                "required": [
                    "email"
                ],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "build_and_push_image",
            "description": "Builds and pushes a container image to Docker Hub (or a compatible registry) using the specified tag, and returns the repository URL of the pushed image.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tag": {
                        "type": "string",
                        "description": "The tag to assign to the container image (e.g., 'daniel.putta')."
                    }
                },
                "required": [
                    "tag"
                ],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "deploy_fastapi",
            "description": "Creates and deploys a FastAPI app to expose student class data from the provided CSV file by updating a file in a GitHub repository, and returns the deployed API URL or None if deployment fails.",
            "parameters": {
                "type": "object",
                "properties": {
                    "csv_filepath": {
                        "type": "string",
                        "description": "The local path to the CSV file containing student data."
                    }
                },
                "required": [
                    "csv_filepath"
                ],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    {
        "type": "function",
        "function": {
            "name": "setup_llamafile_with_ngrok",
            "description": "Sets up and runs the Llama-3.2-1B-Instruct model using Llamafile and exposes it via an Ngrok tunnel, returning the public URL if successful.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": false
            },
            "strict": true
        }
    }
]