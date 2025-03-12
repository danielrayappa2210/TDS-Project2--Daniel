from GA1 import *
from GA1_func_desc import *
from typing import Dict, Any

# Function calling 
def query_gpt(user_input: str, tools: list[Dict[str, Any]]) -> Dict[str, Any]:
    response = requests.post(
        "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('AIPROXY_TOKEN')}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": user_input}],
            "tools": tools,
            "tool_choice": "auto",
        },
    )
    return response.json()["choices"][0]["message"]

input_str = "question=Download and unzip file abcd.zip which has a single extract.csv file inside. What is the value in the 'answer' column of the CSV file?"
response = query_gpt(input_str, GA1_tools)
function_call_details = [tool_call["function"] for tool_call in response["tool_calls"]][0]
print(function_call_details)

# from fastapi import FastAPI, UploadFile, File, Form
# import os

# app = FastAPI()
# UPLOAD_DIR = "./uploaded_files"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# @app.post("/upload")
# async def upload(text: str = Form(...), file: UploadFile = File(...)):
#     data = await file.read()
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as f:
#         f.write(data)
#     # Now you can pass `file_path` to your LLM function
#     return {"filename": file.filename, "stored_at": file_path, "text": text}