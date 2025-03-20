# GA1 function description
GA1_tools = [
    {
        "type": "function",
        "function": {
            "name": "run_code_status",
            "description": "Runs the 'code -s' command in the terminal to capture and return Visual Studio Code's full status output, including version, commit hash, build details, and environment information.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_uv",
            "description": "Sends an HTTPS GET request to https://httpbin.org/get with the URL-encoded parameter email_id (installing httpie if needed) and returns only the JSON response body.",
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
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_prettier",
            "description": "Formats the README.md file using Prettier v3.4.2 via npx, pipes the output to sha256sum, and returns the resulting SHA256 hash of the formatted content.",
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
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_formula_in_google_sheet",
            "description": "Executes a Google Sheets-specific formula and returns the computed output.",
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
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_formula_in_excel_365_sheet",
            "description": "Executes an Office 365-exclusive Excel formula and returns the computed output.",
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
                "additionalProperties": False
            },
            "strict": True
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
                "additionalProperties": False
            },
            "strict": True
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
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_answer_from_csv",
            "description": "Downloads and extracts a ZIP file containing a CSV, then retrieves and returns the value in the 'answer' column from the extracted CSV file.",
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
                "additionalProperties": False
            },
            "strict": True
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
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_txt_to_json_and_hash",
            "description": "Downloads a text file containing key=value pairs, converts them into a single JSON object, computes its hash using an external JSON hashing tool, and returns the resulting hash.",
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
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sum_data_values_of_divs",
            "description": "Selects all <div> elements with the class 'foo' from a provided hidden HTML element, extracts their data-value attributes, sums them, and returns the total.",
            "parameters": {
                "type": "object",
                "properties": {
                    "html_path": {
                        "type": "string",
                        "description": "The file path to the HTML file."
                    }
                },
                "required": ["html_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sum_values_for_symbols",
            "description": "Downloads a ZIP archive containing three files with different encodings, parses each file to extract the 'symbol' and 'value' columns, filters rows where the symbol matches a predefined target set, and returns the sum of the associated values.",
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
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_github_repo_and_push_json",
            "description": "Creates a new public GitHub repository, commits and pushes a JSON file named email.json containing a provided email address, and returns the raw GitHub URL of the file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_id": {
                        "type": "string",
                        "description": "The email address to be stored in the JSON file."
                    }
                },
                "required": ["email_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "replace_iitm_and_compute_sha256",
            "description": "Extracts files from a provided archive, replaces every instance of 'IITM' (in any case variation) with 'IIT Madras' without altering line endings, and finally concatenates the files to return the SHA256 hash computed via 'cat * | sha256sum' in bash.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zip_filepath": {
                        "type": "string",
                        "description": "The file path to the ZIP archive."
                    }
                },
                "required": ["zip_filepath"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files_and_attributes",
            "description": "Downloads and extracts an archive, lists all files with their modification dates and sizes, filters files that meet a minimum size threshold and a specified modification date, and returns the total size of the matching files.",
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
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "move_rename_files",
            "description": "Downloads and extracts an archive, moves all files from subdirectories into an empty folder, renames each file by replacing every digit with its next value (with '9' wrapping to '0'), and computes the SHA256 hash of the concatenated and sorted file contents.",
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
                "additionalProperties": False
            },
            "strict": True
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
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

# GA2 function description
GA2_tools = [
    {
        "type": "function",
        "function": {
            "name": "documentation_markdown",
            "description": "Generates a Markdown document for an imaginary weekly step analysis that includes a level 1 heading, level 2 subheadings, bold text, italic text, inline code (e.g., sample_code), a fenced code block, a bulleted list, a numbered list, a table, a hyperlink, an image, and a blockquote.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
            "strict": True
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
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_index_html",
            "description": "Publishes a GitHub Pages site showcasing author's work with an email address embedded in the HTML enclosed by <!--email_off--> and <!--/email_off--> tags, and returns the site's public URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email text to include in the file."
                    }
                },
                "required": ["email"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_colab_authentication",
            "description": "Runs a Google Colab program that authenticates the user with the required email access and processes their account information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email address to authenticate and grant access to Google Colab."
                    }
                },
                "required": ["email"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_image_library_colab",
            "description": "Downloads given image, creates a new Google Colab notebook, fixes an error in the provided code, runs the corrected script to calculate the number of pixels above a defined brightness threshold, and returns the pixel count.",
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
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "deploy_to_vercel",
            "description": "Downloads a JSON file containing marks for imaginary students, deploys a Python app on Vercel that exposes an API endpoint accepting multiple 'name' query parameters, and returns a JSON response with the corresponding marks in the order provided.",
            "parameters": {
                "type": "object",
                "properties": {
                    "json_filepath": {
                        "type": "string",
                        "description": "The local path to the JSON file containing student marks."
                    }
                },
                "required": ["json_filepath"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_and_trigger_workflow",
            "description": "Creates a GitHub Action workflow file in a repository with at least one step whose name includes a specified email address, and returns the URL of the repository where the action is configured.",
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
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "build_and_push_image",
            "description": "Builds and pushes a Docker image to Docker Hub, adds a specific given tag to the image, and returns the Docker image URL in the expected format.",
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
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "deploy_fastapi",
            "description": "Downloads a CSV file with 'studentId' and 'class' columns, then creates and runs a FastAPI server with an '/api' endpoint that returns all student records as JSON in the same order as in the CSV, and supports filtering by one or more 'class' query parameters to return only matching records.",
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
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "setup_llamafile_with_ngrok",
            "description": "Downloads the Llamafile, runs the Llama-3.2-1B-Instruct.Q6_K.llamafile model using it, creates an ngrok tunnel to the server, and returns the public ngrok URL.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
            "strict": True
        }
    }
]