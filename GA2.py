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

import hashlib

def run_colab_authentication(email):
    """Authenticates user in Colab, retrieves user info, and returns the hashed value."""

    return hashlib.sha256(f"{email} 2025".encode()).hexdigest()[-5:]

email = "daniel.putta@gramener.com"
print(run_colab_authentication(email))

# ====================================================================================================================

import numpy as np
from PIL import Image
import colorsys

def run_image_library_colab(image_path, threshold):
    rgb = np.array(Image.open(image_path)) / 255.0
    lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x)[1], 2, rgb)
    return np.sum(lightness > threshold)

image_path = "lenna.webp"
threshold = 0.455

light_pixels = run_image_library_colab(image_path, threshold)
print(f"Number of pixels with lightness > {threshold}: {light_pixels}")

# ====================================================================================================================

import os
import requests
import base64
import json

def update_and_trigger_workflow(email):
    """
    Updates the GitHub Actions workflow file with the given email, 
    commits the change using GitHub API, and triggers the workflow.
    """
    owner, repo, path, branch = "danielrayappa2210", "TDS", ".github/workflows/main.yml", "main"
    token = os.getenv("ACCESS_TOKEN")
    if not token: return print("Missing ACCESS_TOKEN")

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"}
    file_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    # Get file SHA
    res = requests.get(file_url, headers=headers)
    if res.status_code != 200: return print("Failed to get file SHA")
    sha = res.json()["sha"]

    # Format new YAML content
    content = f"""on:\n  workflow_dispatch:\n\njobs:\n  test:\n    runs-on: ubuntu-latest\n    \n    steps:\n      - name: {email}\n        run: echo "Hello, world!"\n"""
    encoded_content = base64.b64encode(content.encode()).decode()

    # Update file
    update_data = {"message": "Updated workflow", "content": encoded_content, "sha": sha, "branch": branch}
    if requests.put(file_url, headers=headers, data=json.dumps(update_data)).status_code != 200:
        return print("Failed to update file")

    # Trigger workflow
    trigger_url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/main.yml/dispatches"
    if requests.post(trigger_url, json={"ref": branch}, headers=headers).status_code == 204:
        return "https://github.com/danielrayappa2210/TDS"
    else:
        print("Failed to trigger workflow")
      
# Example usage:

gh_repo_url = update_and_trigger_workflow("user@example.com")
print(gh_repo_url)

# ====================================================================================================================

import os
import subprocess

def build_and_push_image(tag):
    # Read the Docker token from the environment.
    token = os.getenv("DOCKER_TOKEN")
    if not token:
        raise EnvironmentError("DOCKER_TOKEN environment variable not set.")
    
    # Hardcoded Docker Hub username and repository.
    username = "danielrayappa"
    repo = "tdsga"
    image_tag = f"{username}/{repo}:{tag}"
    
    # Log in to Docker Hub using your personal access token.
    subprocess.run(["docker", "login", "--username", username, "--password", token], check=True)
    
    # Build the Docker image from the current directory.
    subprocess.run(["docker", "build", "-t", image_tag, "."], check=True)
    
    # Push the Docker image to Docker Hub.
    subprocess.run(["docker", "push", image_tag], check=True)
    
    # Print the Docker Hub repository URL.
    return f"https://hub.docker.com/repository/docker/{username}/{repo}/general"
    
# Example usage:

tag_input = "test"
print(build_and_push_image(tag_input))

# ====================================================================================================================