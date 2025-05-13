import subprocess
import json
from Model_client import AzureClient  
from Memory import MemorySingleton

memory = MemorySingleton()

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
    },
    {
  "name": "ffuf",
  "description": "Performs fuzzing using ffuf.",
  "parameters": {
    "type": "object",
    "properties": {
      "command": {
        "type": "string",
        "description": " by default u have to use common.txt for wordlist if user didnt have provided the path for wordlist , Full ffuf command. Flags:\n\
-u : Target URL (must include FUZZ)           \n\
-w : Wordlist file (and optional keyword)     \n\
-H : Header (e.g., 'Host: FUZZ')              \n\
-X : HTTP method (GET, POST, etc.)            \n\
-d : POST data                                \n\
-b : Cookies (e.g., 'key=value')              \n\
-r : Follow redirects                         \n\
-t : Number of threads                        \n\
-x : Proxy URL (http/socks5)                  \n\
-recursion : Enable recursive fuzzing         \n\
-recursion-depth : Max recursion depth        \n\
-rate : Requests per second                   \n\
-p : Delay between requests                   \n\
-v : Verbose output                           \n\
-s : Silent mode                              \n\
-json : JSON output                           \n\
-o : Output file path                         \n\
-of : Output format (json, html, etc.)        \n\
-e : Extensions to append to FUZZ             \n\
-mode : clusterbomb, pitchfork, sniper        \n\
-mc/-mr/-ms/-mw : Matchers (status, regex, etc.)\n\
-fc/-fr/-fs/-fw : Filters                     \n\
Example: ffuf -w wordlist.txt -u http://host/FUZZ -mc 200 -fs 42 -t 50 -v"
      }
    },
    "required": ["command"]
  }
}

]

def WebVulnHandler(user_query):
    # print("🔍 Running WebVulnHandler...")  
    yield f"{json.dumps({'data': "Task:-Web Vulnebility ...", 'istool': False, 'tool_out': ''})}\n" 

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
    func_name = out.name
    if out is not None:

        if func_name=="sqlmap_scan":
            yield f"{json.dumps({'data': "running sqlMap", 'istool': False, 'tool_out': ''})}\n" 
     
            func_args = json.loads(out.arguments)  
            print(func_args)
            command=func_args['command']
            targeturl=func_args['target_url']
            print(command)
            output=sqlmap_scan(command=command,target_url=targeturl)
            print(output)
            yield f"{json.dumps({'data': "task completed", 'istool': True, 'tool_out': output})}\n"

            history = memory.get_history()
            response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a cyber bot that is capable of various tasks.,expalin the important logs of sqlmap that was ran ,,ensure proper line breaks to show clear output "},
                {"role": "system", "content": f"An sqlmap command was run -> {command}\nThe output of the user's query is:\n{output}"}
            ],
            stream=True
           )
            for chunk in response:
                if chunk.choices and hasattr(chunk.choices[0], "delta") and chunk.choices[0].delta:
                    yield json.dumps({"data": chunk.choices[0].delta.content, "istool": False, "tool_out": ""}) + "\n"
        elif func_name=="ffuf":
            yield f"{json.dumps({'data': "running ffuf fuzzer", 'istool': False, 'tool_out': ''})}\n"
            func_args = json.loads(out.arguments)  
            print(func_args)
            command=func_args['command']
            print(command)
            output=ffuf(command=command)
            print(output)
            yield f"{json.dumps({'data': "task completed", 'istool': True, 'tool_out': output})}\n"
            response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a cyber bot that is capable of various tasks.,expalin the important logs of ffuf that was ran ,,ensure proper line breaks to show clear output ,make sure provide proper next follow if you find vulnerbilities."},
                {"role": "system", "content": f"An sqlmap command was run -> {command}\nThe output of the user's query is:\n{output}"}
            ],
            stream=True
           )
            for chunk in response:
                if chunk.choices and hasattr(chunk.choices[0], "delta") and chunk.choices[0].delta:
                    yield json.dumps({"data": chunk.choices[0].delta.content, "istool": False, "tool_out": ""}) + "\n"



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
    

def ffuf(command):
      
    print(f"🔍 Running ffuf :-  {command}")

    command_list = command.split(" ")

    result = subprocess.run(command_list, capture_output=True, text=True)

    output = ""
    if result.stdout:
        output += result.stdout
    if result.stderr:
        output += f"\n❌ Errors: {result.stderr}"
    
    return output  