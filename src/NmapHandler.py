import nmap
import json
from Model_client import AzureClient
from Memory import MemorySingleton

memory = MemorySingleton()

def scanner(user_query):
    yield f"\n Scanning task ...\n"
    print("scanning task ....")
    
    client = AzureClient.get_client()
    deployment = AzureClient.deployment

    # Get the function call from the model
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
        params_dict = json.loads(params)
        ip = params_dict.get("ip", "")
        arguments = params_dict.get("arguments", [])
        yield f"\n \n"

        args_str = " ".join(arguments)
        command = f"{ip} {args_str}"

        function_map = {
            "scan": scan  # Ensure `scan` is a blocking function
        }

        if name in function_map:
            yield f"\nRunning scan on {ip} with arguments: {args_str}\n"
            
            # ⏳ **Block here until scan completes** ⏳
            scan_results = function_map[name](ip, arguments)  # `scan()` is blocking

        else:
            yield f"⚠️ Error: Unknown function name: {name}\n"
            return

        out_str = json.dumps(scan_results, indent=2)

        history = memory.get_history()
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a cyber bot that is capable of various tasks."},
                {"role": "system", "content": f"User history -> {history}"},
                {"role": "system", "content": f"An Nmap command was run -> {command}\nThe output of the user's query is:\n{out_str}"}
            ],
            stream=True
        )

        yield "\nFinal Scan Result:\n"

     
        for chunk in response:
            if chunk.choices and hasattr(chunk.choices[0], "delta") and chunk.choices[0].delta:
                yield chunk.choices[0].delta.content


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

Available arguments:
- **Port Scanning**: `-p 80,22` (specific ports), `-p 80-100` (range of ports)
- **Service & Version Detection**: `-sV`
- **OS Detection**: `-O`
- **Aggressive Scan**: `-A`
- **Ping Scan**: `-sn`
- **Fast Scan**: `-F`
- **UDP Scan**: `-sU`
- **Scan Entire Subnet**: `-p 22,80,443 192.168.1.0/24`
- **Stealth Scan (SYN)**: `-sS`
- **Disable DNS Resolution**: `-n`
- **TCP Connect Scan**: `-sT`

Example: `["-p 22,80,443", "-sV"]` 
"""
                }
            },
            "required": ["ip"]
        }
    }
]
