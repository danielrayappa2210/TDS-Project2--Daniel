def documentation_markdown():
    # Read markdown content from a file named "content.txt"
    try:
        with open('content.txt', 'r', encoding='utf-8') as file:
            markdown_text = file.read()
    except FileNotFoundError:
        print("Error: 'content.txt' not found.")

    # Optionally process the markdown_text if needed.
    # For this example, we'll simply output it.
    print(markdown_text)

documentation_markdown()

# ====================================================================================================================

import base64
from io import BytesIO
from PIL import Image

def compress_and_encode_image(input_path):
    """
    Compress an image losslessly into WebP format and return a Base64 encoded data URI.
    
    Parameters:
      input_path (str): The file path to the source image.
      
    Returns:
      str: A Base64 encoded data URI of the compressed image.
    """
    # Open the input image
    img = Image.open(input_path)
    
    # Save the image in WebP format to an in-memory buffer using lossless compression with method=6
    buffer = BytesIO()
    img.save(buffer, format='WEBP', lossless=True, method=6)
    
    # Get binary data from the buffer and encode it as Base64
    binary_data = buffer.getvalue()
    b64_data = base64.b64encode(binary_data).decode("utf-8")
    
    # Construct and return the data URI
    return f"data:image/webp;base64,{b64_data}"

# Example usage:
data_uri = compress_and_encode_image("shapes.png")
print(data_uri)

# ====================================================================================================================

import os
from datetime import datetime
from github import Github

def update_index_html(email):
    """
    Update the hard-coded index.html file in a hard-coded GitHub repository and branch.
    
    This function writes two lines to the file:
      1. An HTML comment with the provided email:
         <!--email_off-->{email}<!--/email_off-->
      2. The current date and time.
    
    Parameters:
      email (str): The email text to include in the file.
      
    The GitHub token is read from the ACCESS_TOKEN environment variable.
    """

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_content = f"<!--email_off-->{email}<!--/email_off-->\n{current_time}"

    # Get token from environment variables
    token = os.getenv("ACCESS_TOKEN")
    if not token:
        raise EnvironmentError("ACCESS_TOKEN environment variable is not set.")
    
    # Hard-coded settings
    repo_name = "danielrayappa2210/TDS-GA2"  # Replace with your GitHub username and repository name
    branch = "main"
    file_path = "index.html"
    
    # Authenticate and get the repository
    g = Github(token)
    repos = g.get_user().get_repos()
    repo = g.get_repo(repo_name)
    
    # Retrieve the file to update (needed for its SHA)
    file = repo.get_contents(file_path, ref=branch)
    
    # Update the file with the new content
    commit_message = "Update index.html via Python script"
    update_response = repo.update_file(file.path, commit_message, new_content, file.sha, branch=branch)
    
    return "https://danielrayappa2210.github.io/TDS-GA2/"

# Example usage:

email = "daniel.putta@gramener.com"
gh_page_url = update_index_html(email)
print(gh_page_url)

# ====================================================================================================================