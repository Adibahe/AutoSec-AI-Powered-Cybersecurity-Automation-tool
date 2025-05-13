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

import json

class BaseModel:
    def __init__(self, data="", istool=False, tool_out=""):
        self.data = data
        self.istool = istool
        self.tool_out = tool_out

    def to_json(self):
        return json.dumps(self.__dict__)  # ✅ Ensures valid JSON

def extract_using_ai(output_json, field_name, field_aliases=None):
    client = AzureClient.get_client()
    deployment = AzureClient.deployment
    field_aliases = field_aliases or []

    prompt = (
        f"You are given a JSON object from a tool output. Your task is to extract the most likely values and change the values with respect to the asked field "
        f"for the field '{field_name}' or some thing like this. Also consider any aliases: {field_aliases}. this fileds might be statement instead of extact field names"
        f"Return only the value as plain text, no formatting or explanation. if not able to extract just return empty\n\n"
        f"JSON:\n{json.dumps(output_json, indent=2)}"
    )

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are an AI that extracts values from JSON outputs."},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )
    return response.choices[0].message.content.strip()

def fill_missing_parameters(tool_chain, all_outputs):
    extraction_cache = {}  # Cache to store previously extracted values

    for step in tool_chain:
        if "depends_on" in step and step["depends_on"]:
            dep = step["depends_on"]
            dep_step = dep.get("step")
            field = dep.get("field")
            aliases = tuple(dep.get("field_aliases", []))

            source_output = all_outputs.get(dep_step, {})
            cache_key = (dep_step, field, aliases)

            if cache_key in extraction_cache:
                extracted = extraction_cache[cache_key]
                print(f"📦 Using cached value for {cache_key}: {extracted}")
            else:
                print(f"\n🔍 Extracting field '{field}' (aliases: {aliases}) from step {dep_step} output")
                extracted = extract_using_ai(source_output, field, list(aliases))
                extraction_cache[cache_key] = extracted


            if extracted:
                print(f"✅ Extracted value: {extracted}")
                if not step["parameters"]:
                    step["parameters"] = {field: extracted}
                else:
                    for key in step["parameters"]:
                        if step["parameters"][key] == "":
                            step["parameters"][key] = extracted
            else:
                print(f"⚠️ Could not resolve dependency for step {step['step']}: field '{field}' not found.")
                raise ValueError(f"Unresolved dependency for step {step['step']}: field '{field}'")
    return tool_chain

def tasksfinder(user_query):
    client = AzureClient.get_client()
    deployment = AzureClient.deployment
    history = memory.get_history()

    tools = extract_tool_chain(user_query)


    if not tools:
        print("No tools extracted.")
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a cyber bot that is capable of various tasks."},
                {"role": "user", "content": user_query},
            ],
            functions=functions,
            stream=True
        )
        for chunk in response:
            if chunk.choices and hasattr(chunk.choices[0], "delta") and chunk.choices[0].delta:
                yield json.dumps({"data": chunk.choices[0].delta.content, "istool": False, "tool_out": ""}) + "\n"
        return

    all_outputs = {}

    i = 0
    while i < len(tools):
        print("new tools:", tools)
        tool = tools[i]

        func_name = tool["tool"]
        params = json.dumps(tool["parameters"])
        user_query = f"{tool['command']} with parameters: {params}"

        print(f"\n🚀 Executing: {func_name} -> {user_query}")

        task_func = task_map.get(func_name)
        if not task_func:
            print(f"⚠️ Error: Unknown function {func_name}")
            yield json.dumps({'data': f'⚠️ Error: Unknown function {func_name}', 'istool': False, 'tool_out': ''}) + "\n"
            i += 1
            continue

        result = ""
        for output in task_func(user_query):
            yield output + "\n"
            try:
                parsed = json.loads(output)
                if parsed.get("istool") and parsed.get("tool_out"):
                    result = json.loads(parsed["tool_out"])
            except Exception as e:
                print(f"❌ Error parsing tool output: {e}")

        all_outputs[tool["step"]] = result
        i += 1
        try:
            tools = fill_missing_parameters(tools, all_outputs)
        except ValueError as ve:
            print(f"❌ Stopping execution: {ve}")
            yield json.dumps({'data': f'❌ Execution stopped: {ve}', 'istool': False, 'tool_out': ''}) + "\n"
        