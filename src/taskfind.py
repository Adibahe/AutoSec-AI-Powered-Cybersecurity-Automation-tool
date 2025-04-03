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
from extractToolChain import extract_tool_chain
from functions import functions
memory = MemorySingleton()


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

import json
from Model_client import AzureClient
from functions import functions

def tasksfinder(user_query):
    tools = extract_tool_chain(user_query)  # Extract toolchain
    print(tools)
    if not tools:
        print("No tools extracted.")
        return

    client = AzureClient.get_client()
    deployment = AzureClient.deployment
    history = memory.get_history()

    for tool in tools:
        func_name = tool["tool"]  # Extract only the tool name (remove "functions.")
        params = json.dumps(tool["parameters"])  # Convert parameters to JSON
        user_query = f"{tool['command']} with parameters: {params}"  # Generate user query

        print(f"\nExecuting: {func_name} -> {user_query}")  # Debugging

        task_func = task_map.get(func_name)  # Get function from task_map
        if not task_func:
            print(f"⚠️ Error: Unknown function {func_name}")
            yield json.dumps({'data': f'⚠️ Error: Unknown function {func_name}', 'istool': False, 'tool_out': ''}) + "\n"
            continue

        # Call the function and yield results
        for output in task_func(user_query):
            yield output + "\n"  # Ensure valid JSON output
