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