import nmap
import json
from Model_client import AzureClient
from Memory import MemorySingleton

import json  
import subprocess


memory = MemorySingleton()
class BaseModel:
    def __init__(self, data="", istool=False, tool_out=""):
        self.data = data
        self.istool = istool
        self.tool_out = tool_out

    def to_json(self):
        return json.dumps(self.__dict__)  

def scanner(user_query):
   
    yield f"{json.dumps({'data': "Scanning task...\n", 'istool': False, 'tool_out': ''})}\n" 
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
        
        params = out.arguments
        name = out.name

        try:
            params_dict = json.loads(params)
        except json.JSONDecodeError:
          
            yield f"{json.dumps({'data': "Error: Invalid function arguments", 'istool': False, 'tool_out': ''})}\n" 
            return  

        command = params_dict['command']

        if name=="scan":
           
            yield f"{json.dumps({'data': f"Running nmap scan command:-{command}", 'istool': False, 'tool_out': ''})}\n" 

            # Run scan
            scan_results = scan(command)
            
            yield json.dumps({"data": "Scan completed.", "istool": True, "tool_out": scan_results}) + "\n"

            response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a cyber bot that is capable of various tasks.your genereal task is to explain nmap scan to the user,ensure proper line breaks to show clear output"},
                {"role": "system", "content": f"An Nmap command was run -> {command}\nThe output of the user's query is:\n{scan_results}"}
            ],
            stream=True
            )

            for chunk in response:
                if chunk.choices and hasattr(chunk.choices[0], "delta") and chunk.choices[0].delta:
                    yield json.dumps({"data": chunk.choices[0].delta.content, "istool": False, "tool_out": ""}) + "\n"

        elif name=="masscan":
            yield f"{json.dumps({'data': f"Running masscan scan command:-{command}", 'istool': False, 'tool_out': ''})}\n" 

            # Run scan
            scan_results = masscan(command)
            
            yield json.dumps({"data": "Scan completed.", "istool": True, "tool_out": scan_results}) + "\n"

            response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a cyber bot that is capable of various tasks.your genereal task is to explain masscan scan to the user,ensure proper line breaks to show clear output"},
                {"role": "system", "content": f"An masscan command was run -> {command}\nThe output of the user's query is:\n{scan_results}"}
            ],
            stream=True
            )

            for chunk in response:
                if chunk.choices and hasattr(chunk.choices[0], "delta") and chunk.choices[0].delta:
                    yield json.dumps({"data": chunk.choices[0].delta.content, "istool": False, "tool_out": ""}) + "\n"


def scan(command):
    print(f"🔍 Running nmapscan  : {command}")

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
  "name": "scan",
  "description": "Performs a network scan on a given IP address using Nmap",
  "parameters": {
    "type": "object",
    "properties": {
      "command": {
        "type": "string",
        "description": "Provide an Nmap command here (format: nmap [options] target). Common flags:\n\n\
-sS (TCP SYN), -sT (TCP connect), -sU (UDP), -sA (ACK), -sN (Null), -sF (FIN), -sX (Xmas),\n\
-sP/-sn (Ping scan), -sV (Service/version detection), -O (OS detection), -A (Aggressive: -O -sV -sC -traceroute),\n\
-p (Specify ports), -F (Fast scan), -r (Don't randomize ports), -T0-T5 (Timing: paranoid to insane),\n\
--open (Show only open), --top-ports (Top N ports), --exclude (Exclude hosts),\n\
-iL (Input list), -oN/-oX/-oG/-oA (Output formats), -Pn (Skip host discovery), -n (No DNS resolution),\n\
--script (NSE script), -sC (Default scripts), --traceroute, -v/-vv (Verbose), -d (Debug), --reason (Show reasons)"
      }
    },
    "required": ["command"]
  }
}

    , {
        "name": "masscan",
        "description": "runs masscan tool,run it when user want extremly fast portscanning or user explcilty asked for this tool or user only want port scanning ",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": """ usage:
masscan -p80,8000-8100 10.0.0.0/8 --rate=10000
 scan some web ports on 10.x.x.x at 10kpps
masscan --nmap
 list those options that are compatible with nmap
masscan -p80 10.0.0.0/8 --banners -oB <filename>
 save results of scan in binary format to <filename>
masscan --open --banners --readscan <filename> -oX <savefile>
 read binary scan results in <filename> and save them as xml in <savefile>
"""
                }
            },
            "required": ["command"]
        }
    }
]

def masscan(command):
    print(f"🔍 Running masscan : {command}")

    command_list = command.split(" ")

    result = subprocess.run(command_list, capture_output=True, text=True)

    output = ""
    if result.stdout:
        output += result.stdout
    if result.stderr:
        output += f"\n❌ Errors: {result.stderr}"
    
    return output  
