from Model_client import AzureClient
from NmapHandler import scanner
from CrackerHandler import cracker
from ExploitHandler import runExploits
from LookupHandler import lookup_handler
from SqlMapHandler import WebVulnHandler
import json
from Memory import MemorySingleton
from WPScanHandler import wpscan
from KatanaHandler import SpiderScan

memory = MemorySingleton()


functions = [
    {
        "name": "scan",
        "description": "Performs a network scan using tools like nmap.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "cracker",
        "description": "Handles any task related to breaking or cracking passwords.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "phishing_detector",
        "description": "Analyzes emails or URLs to detect phishing attempts.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "malware_analysis",
        "description": "Performs static and dynamic analysis on a given file or URL to detect malware.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "web_vulnerability_scan",
        "description": "Scans a website for common vulnerabilities like XSS, SQL injection, etc.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "forensic_analysis",
        "description": "Performs digital forensic analysis on logs or disk images to identify security incidents.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "steganography_detector",
        "description": "Detects hidden messages in images, audio, or text files using steganalysis.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "port_knocking_detector",
        "description": "Analyzes network traffic to detect port knocking attempts.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "social_engineering_analysis",
        "description": "Analyzes chat logs, emails, or messages for signs of social engineering attacks.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "exploitation",
        "description": "Executes exploits against a target using tools like Metasploit or manual scripts.,if user asked to run tools like :- metasploit,searchsploit",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "whois_lookup",
        "description": "Performs a WHOIS lookup on a domain or IP address.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "dns_lookup",
        "description": "Performs a DNS lookup for a given domain.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "ip_geolocation",
        "description": "Retrieves geolocation information for an IP address.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "reverse_ip_lookup",
        "description": "Performs a reverse IP lookup.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "ssl_certificate_lookup",
        "description": "Retrieves SSL certificate details for a given domain.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "mac_address_lookup",
        "description": "Retrieves vendor details for a given MAC address.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "email_verification",
        "description": "Verifies whether an email address is valid and deliverable.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "threat_intelligence_lookup",
        "description": "Checks for security threats associated with a domain, IP, or URL.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "domain_availability",
        "description": "Checks if a domain is available for registration.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
    
        "name": "sqlmap_scan",
        "description": "Performs SQL injection testing using sqlmap.",
        "parameters": {"type": "object", "properties": {}}
    },
     {
    
        "name": "wpscan",
        "description": "Scans a WordPress site for security vulnerabilities using WPScan.",
        "parameters": {"type": "object", "properties": {}}
    },   
    {
    
        "name": "SpiderScan",
        "description": "Performs web spider scans ,if user ask for spider some website or crawl some url etc ,or ask to run tools like katana",
        "parameters": {"type": "object", "properties": {}}
    },
]



task_map = {
    "scan": scanner,
    "cracker": cracker,
    "web_vulnerability_scan": WebVulnHandler,
    "exploitation": runExploits,
    "whois_lookup": lookup_handler,
    "dns_lookup": lookup_handler,
    "ip_geolocation": lookup_handler,
    "ssl_certificate_lookup": lookup_handler,
    "mac_address_lookup": lookup_handler,
    "email_verification": lookup_handler,
    "threat_intelligence_lookup": lookup_handler,
    "domain_availability": lookup_handler,
    "wpscan": wpscan,
    "SpiderScan":SpiderScan,
    "sqlmap_scan":WebVulnHandler
}

#old one 
# def tasksfinder(user_query):
#     client = AzureClient.get_client() 
#     deployment = AzureClient.deployment

#     history = memory.get_history() 
#     #print(f"User history -> {history}")
#     response = client.chat.completions.create(
#         model=deployment,
#         messages=[
#             {"role": "system", "content": "You are a cyber bot that is capable of various tasks."},
#             {"role": "system", "content": f"User history -> {history}"},
#             {"role": "user", "content": user_query},
#         ],
#         functions=functions,  
#         stream=False
#     )

#     out = response.choices[0].message.function_call

#     if out and hasattr(out, "name"):
#         func_name = out.name
#         task_func = task_map.get(func_name, lambda user_query: print("❌ Unknown function"))
#         return task_func(user_query)

#     output=response.choices[0].message.content
#     memory.add_message(user_input=user_query,bot_response=output)
#     return output


import json

class BaseModel:
    def __init__(self, data="", istool=False, tool_out=""):
        self.data = data
        self.istool = istool
        self.tool_out = tool_out

    def to_json(self):
        return json.dumps(self.__dict__)  # ✅ Ensures valid JSON

def tasksfinder(user_query,task):
    client = AzureClient.get_client() 
    deployment = AzureClient.deployment

    history = memory.get_history()  
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a cyber bot that is capable of various tasks."},
            {"role": "system", "content": f"User history -> {history}"},
            {"role": "user", "content": user_query},
            {"role": "user", "content": "sub part of the query currenlty need to be performed:-"+task},
        ],
        functions=functions,  
        stream=True  
    )

    function_call_detected = False
    func_name = None
    func_args = ""

    for chunk in response:  
        if not chunk.choices:
            continue  

        delta = chunk.choices[0].delta 

        if hasattr(delta, "function_call") and delta.function_call:
            function_call_detected = True
            if delta.function_call.name:
                func_name = delta.function_call.name  
            if delta.function_call.arguments:
                func_args += delta.function_call.arguments  # 🚀 Accumulate function args safely

        if hasattr(delta, "content") and delta.content:
            yield f"{json.dumps({'data': delta.content, 'istool': False, 'tool_out': ''})}\n"  # ✅ Ensure valid JSON

    if function_call_detected and func_name:
        print(f"\nFunction Call Detected: {func_name}")
        print(f"Function Arguments: {func_args}")

        try:
            func_args = json.loads(func_args)  # ✅ Convert args to dict
        except json.JSONDecodeError:
            print("⚠️ Warning: Function arguments are not valid JSON.")
            yield f"{json.dumps({'data': '⚠️ Error: Invalid function arguments', 'istool': False, 'tool_out': ''})}\n"
            return  

        task_func = task_map.get(func_name)

        if task_func:
            for output in task_func(user_query):  
                yield f"{output}\n"  # ✅ Always valid JSON
        else:
            yield f"{json.dumps({'data': f'⚠️ Error: Unknown function {func_name}', 'istool': False, 'tool_out': ''})}\n"
