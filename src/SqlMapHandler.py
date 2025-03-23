import subprocess
import json
from Model_client import AzureClient  

functions = [
    {
        "name": "sqlmap_scan",
        "description": "Performs an SQL Injection scan using SQLMap.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The full SQLMap command to execute, including -u for the target URL."
                },
                "target_url": {
                    "type": "string",
                    "description": "The target URL to scan for SQL injection. Example: 'http://example.com/index.php?id=1'"
                }
            },
            "required": ["command", "target_url"]  
        }
    }
]

def WebVulnHandler(user_query):
    print("🔍 Running WebVulnHandler...")  
    
    client = AzureClient().get_client() 
    deployment = AzureClient.deployment  

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a cyber bot and your task is to run exploit tools based on user queries."},
            {"role": "user", "content": user_query},
        ],
        functions=functions,
        stream=False
    )

    out = response.choices[0].message.function_call
    if out:
        func_name = out.name
        func_args = json.loads(out.arguments)  
        print(f"📌 Function called: {func_name} with args: {func_args}")

        if func_name == "sqlmap_scan":
            sqlmap_scan(func_args["command"], func_args["target_url"])  
        else:
            print("❌ Unknown function call received.")
    else:
        print("🤖 No function call detected.")

def sqlmap_scan(command, target_url):
    """Executes an SQLMap scan based on user input."""
    if "-u" not in command:
        command += f' -u "{target_url}"'  

    print(f"🚀 Running SQLMap: {command}")

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout
        print("✅ Scan Complete!")
        print(output)
        return output
    except Exception as e:
        print(f"❌ Error running SQLMap: {e}")
        return str(e)