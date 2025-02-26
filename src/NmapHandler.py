import nmap
import json
from Model_client import AzureClient

def scanner(user_query):
    print("scanning task ....")
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
        print("running nmap scan...")
        params = out.arguments
 
        name = out.name
       
        
        params_dict = json.loads(params)
        ip = params_dict.get("ip", "")
        arguments = params_dict.get("arguments", [])
        
        args_str = " ".join(arguments)
        command = f"{ip} {args_str}"
        
        func = eval(name)
        out = func(ip, arguments)
        
        out_str = json.dumps(out, indent=2)
        
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a cyber bot that is capable of various tasks."},
                {"role": "system", "content": f"An Nmap command was run -> {command}\nThe output of the user's query is:\n{out_str}"}
            ],
            stream=False
        )
        print(response.choices[0].message.content)

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
