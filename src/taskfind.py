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

def tasksfinder(user_query):
    print(extract_tool_chain(user_query))

    client = AzureClient.get_client() 
    deployment = AzureClient.deployment

    history = memory.get_history()  
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a cyber bot that is capable of various tasks."},
            {"role": "system", "content": f"User history -> {history}"},
            {"role": "user", "content": user_query},
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
