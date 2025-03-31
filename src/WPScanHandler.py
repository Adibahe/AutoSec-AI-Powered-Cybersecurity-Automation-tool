import os
import json
import subprocess
from Model_client import AzureClient


def wpscan(user_query):
    yield f"{json.dumps({'data': "Running WpScan ...", 'istool': False, 'tool_out': ''})}\n" 

    client = AzureClient.get_client()
    deployment = AzureClient.deployment


    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a cyber bot and your task is to run Wpscan, etc. For that, run functions."},
            {"role": "user", "content": user_query},
        ],
        functions=functions,
        stream=False
    )

    out = response.choices[0].message.function_call

    if out is not None:
        
        func_name = out.name
        func_args = json.loads(out.arguments)  
        print(func_args)
        command=func_args['command']
        print(command)
        output=scan(command=command)
        print(output)
        yield f"{json.dumps({'data': "task completed", 'istool': True, 'tool_out': output})}\n"

     
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a cyber bot that is capable of various tasks.,expalin the important parts of wpscan logs "},
                {"role": "system", "content": f"An wpscan command was run -> {command}\nThe output of the user's query is:\n{output}"}
            ],
            stream=True
        )
        for chunk in response:
            if chunk.choices and hasattr(chunk.choices[0], "delta") and chunk.choices[0].delta:
                yield json.dumps({"data": chunk.choices[0].delta.content, "istool": False, "tool_out": ""}) + "\n"


def scan(command):
    print(f"🔍 Running wpscan with command: {command}")

    command_list = command.split(" ")

    result = subprocess.run(command_list, capture_output=True, text=True)

    output = ""
    if result.stdout:
        output += result.stdout
    if result.stderr:
        output += f"\n{result.stderr}"
    
    return output  



functions = [
    {
        "name": "wpscan",
        "description": "Performs WordPress security scanning using WPScan. It detects vulnerabilities, plugins, themes, and user enumeration.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The WPScan command to execute for scanning a WordPress site. Examples:\n\n"
                                   "- `wpscan --url https://example.com`\n"
                                   "  → Performs a basic scan of the WordPress site.\n\n"
                                   "- `wpscan --url https://example.com --enumerate u`\n"
                                   "  → Enumerates WordPress users on the site.\n\n"
                                   "- `wpscan --url https://example.com --enumerate p`\n"
                                   "  → Enumerates WordPress plugins to check for vulnerabilities.\n\n"
                                   "- `wpscan --url https://example.com --enumerate t`\n"
                                   "  → Enumerates WordPress themes and checks for known vulnerabilities.\n\n"
                                   "- `wpscan --url https://example.com --api-token YOUR_API_TOKEN`\n"
                                   "  → Uses an API token to fetch vulnerability data from WPScan's database.\n\n"
                                   "- `wpscan --url https://example.com --proxy http://127.0.0.1:8080`\n"
                                   "  → Uses a proxy for scanning.\n\n"
                                   "- `wpscan --url https://example.com --force`\n"
                                   "  → Forces the scan, even if the target has protection mechanisms.\n\n"
                                   "- `wpscan --url https://example.com --stealthy`\n"
                                   "  → Runs the scan in stealth mode to reduce detection chances.\n\n"
                                   "- `wpscan --url https://example.com --output result.txt`\n"
                                   "  → Saves scan results to a file."
                }
            },
            "required": ["command"]
        }
    }
]
