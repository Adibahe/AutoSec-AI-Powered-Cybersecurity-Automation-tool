import nmap
import json
from Model_client import AzureClient
from Memory import MemorySingleton


memory = MemorySingleton()
class BaseModel:
    def __init__(self, data="", istool=False, tool_out=""):
        self.data = data
        self.istool = istool
        self.tool_out = tool_out

    def to_json(self):
        return json.dumps(self.__dict__)  # ✅ Ensures valid JSON

def scanner(user_query):
   
    yield f"{json.dumps({'data': "Scanning task...", 'istool': False, 'tool_out': ''})}\n" 
    print("Scanning task ....")

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
        print("Running Nmap scan...")
        params = out.arguments
        name = out.name

        try:
            params_dict = json.loads(params)
        except json.JSONDecodeError:
          
            yield f"{json.dumps({'data': "Error: Invalid function arguments", 'istool': False, 'tool_out': ''})}\n" 
            return  

        ip = params_dict.get("ip", "")
        arguments = params_dict.get("arguments", [])
        args_str = " ".join(arguments)
        command = f"{ip} {args_str}"

        function_map = {"scan": scan}

        if name in function_map:
           
            yield f"{json.dumps({'data': f"Running scan on {ip} with arguments: {args_str}", 'istool': False, 'tool_out': ''})}\n" 

            # Run scan
            scan_results = function_map[name](ip, arguments)
            scan_results_str = json.dumps(scan_results, indent=2)
            
            yield json.dumps({"data": "Scan completed.", "istool": True, "tool_out": scan_results_str}) + "\n"
        else:
            yield json.dumps({"data": f"⚠️ Error: Unknown function name: {name}", "istool": False, "tool_out": ""}) + "\n"
            return

        history = memory.get_history()
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a cyber bot that is capable of various tasks."},
                {"role": "system", "content": f"User history -> {history}"},
                {"role": "system", "content": f"An Nmap command was run -> {command}\nThe output of the user's query is:\n{scan_results_str}"}
            ],
            stream=True
        )

        for chunk in response:
            if chunk.choices and hasattr(chunk.choices[0], "delta") and chunk.choices[0].delta:
                yield json.dumps({"data": chunk.choices[0].delta.content, "istool": False, "tool_out": ""}) + "\n"

def scan(ip, arguments):
    nm = nmap.PortScanner()
    args_str = " ".join(arguments)
    nm.scan(ip, arguments=args_str)
    print(f"Running command: {ip} {args_str}")

    result = {}
    for host in nm.all_hosts():
        result[host] = {
            "hostname": nm[host].hostname(),
            "state": nm[host].state(),
            "protocols": {}
        }

        for proto in nm[host].all_protocols():
            result[host]["protocols"][proto] = {}
            ports = nm[host][proto].keys()
            for port in sorted(ports):
                result[host]["protocols"][proto][port] = nm[host][proto][port]["state"]

    return result

functions = [
    {
        "name": "scan",
        "description": "Performs a network scan on a given IP address using Nmap.",
        "parameters": {
            "type": "object",
            "properties": {
                "ip": {
                    "type": "string",
                    "description": "The target IP address to scan (e.g., '192.168.1.1')."
                },
                "arguments": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": """List of Nmap arguments to customize the scan. 

Example: `["-p 22,80,443", "-sV"]` 
"""
                }
            },
            "required": ["ip"]
        }
    }
]
