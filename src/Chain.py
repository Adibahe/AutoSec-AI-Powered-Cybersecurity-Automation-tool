import json
from Model_client import AzureClient
import ast
from taskfind import tasksfinder

class BaseModel:
    def __init__(self, data="", istool=False, tool_out=""):
        self.data = data
        self.istool = istool
        self.tool_out = tool_out

    def to_dict(self):
        return {
            "data": self.data,
            "istool": self.istool,
            "tool_out": self.tool_out
        }

def safe_parse_steps(response_text):
    try:
        result = ast.literal_eval(response_text.strip())
        if isinstance(result, list) and all(isinstance(item, str) for item in result):
            return result
    except Exception:
        pass
    raise ValueError("LLM response is not a valid list of strings")
def Chain(user_query):
    client = AzureClient.get_client() 
    deployment = AzureClient.deployment

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system", 
                "content": """You are a cyber bot. Your task is to take the user query and break it down into atomic, intermediate steps.
Each step must be a single clear task. 
🚫 Do NOT merge multiple tasks into one.
✅ Only return a valid Python list of strings — no explanations, no comments, no extra text.

For example:
User query: "do a fast nmap scan on 192.168.1.1 and find vulnerabilities from the result"
Output: ["Do a fast nmap scan on 192.168.1.1", "Find vulnerabilities from the result"]

Remember: return only a Python list. Nothing else.
"""
            },
            {"role": "user", "content": user_query},
        ],
        stream=False
    )

    reply_content = response.choices[0].message.content
    steps = safe_parse_steps(reply_content)
    
    print("LLM Steps:", steps)

    # ✅ Initialize temp here
    temp = user_query + "\nbot response:\n"

    for out in steps:
        for ele in tasksfinder(user_query, out):
            try:
                ele_dict = json.loads(ele)
                print(ele_dict["data"])  
                temp += ele_dict["data"] + "\n"  
            except Exception as e:
                print("Error parsing ele:", e)

    print("Final bot response:", temp)
