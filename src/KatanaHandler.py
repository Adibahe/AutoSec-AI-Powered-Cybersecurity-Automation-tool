import json
import subprocess
from Model_client import AzureClient
from Memory import MemorySingleton

memory = MemorySingleton()

def SpiderScan(user_query):
    yield f"{json.dumps({'data': "Web spider ...", 'istool': False, 'tool_out': ''})}\n" 

    client = AzureClient.get_client()
    deployment = AzureClient.deployment


    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a cyber bot and your task is to scan networks, etc. For that, run functions."},
            {"role": "user", "content": user_query},
        ],
        functions=functions,
        stream=False
    )

    out = response.choices[0].message.function_call

    if out is not None:
        yield f"{json.dumps({'data': "running katana", 'istool': False, 'tool_out': ''})}\n" 
        func_name = out.name
        func_args = json.loads(out.arguments)  
        print(func_args)
        command=func_args['command']
        print(command)
        output=spider(command=command)
        print(output)
        yield f"{json.dumps({'data': "task completed", 'istool': True, 'tool_out': output})}\n"

        history = memory.get_history()
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a cyber bot that is capable of various tasks.,expalin the important parts of katana logs web spider and crawling "},
                {"role": "system", "content": f"User history -> {history}"},
                {"role": "system", "content": f"An katana command was run -> {command}\nThe output of the user's query is:\n{output}"}
            ],
            stream=True
        )
        for chunk in response:
            if chunk.choices and hasattr(chunk.choices[0], "delta") and chunk.choices[0].delta:
                yield json.dumps({"data": chunk.choices[0].delta.content, "istool": False, "tool_out": ""}) + "\n"



def spider(command):
    print(f"🔍 Running katana with command: {command}")

    command_list = command.split(" ")

    result = subprocess.run(command_list, capture_output=True, text=True)

    output = ""
    if result.stdout:
        output += result.stdout
    if result.stderr:
        output += f"\n❌ Errors: {result.stderr}"
    
    return output  

        




functions = [
    {
        "name": "spider",
        "description": "Performs web crawling and spidering on the target using Katana. It discovers URLs, subdomains, and API endpoints.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The Katana command to execute for web crawling. Examples:\n\n"
                                   "- `katana -u https://example.com`\n"
                                   "  → Performs basic crawling of the given URL.\n\n"
                                   "- `katana -u https://example.com -jc`\n"
                                   "  → Extracts JavaScript endpoints from the target.\n\n"
                                   "- `katana -u https://example.com -d 3`\n"
                                   "  → Crawls the target up to a depth of 3.\n\n"
                                   "- `katana -u https://example.com -fs`\n"
                                   "  → Follows subdomains found during crawling.\n\n"
                                   "- `katana -u https://example.com -proxy http://127.0.0.1:8080`\n"
                                   "  → Uses a proxy for crawling.\n\n"
                                   "- `katana -u https://example.com -o output.txt`\n"
                                   "  → Saves results to a file."
                }
            },
            "required": ["command"]
        }
    }
]

