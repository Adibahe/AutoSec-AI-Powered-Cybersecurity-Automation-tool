from openai import AzureOpenAI
from Model_client import AzureClient
from NmapHandler import scanner
from CrackerHandler import cracker
from ExploitHandler import runExploits
from LookupHandler import lookup_handler

from Memory import MemorySingleton

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
    }
]


def scan(user_query):
    print("🔍 Running network scan...")

def phishing_detector(user_query):
    print("⚠️ Analyzing for phishing threats...")

def malware_analysis(user_query):
    print("🦠 Performing malware analysis...")

def web_vulnerability_scan(user_query):
    print("🌐 Scanning for web vulnerabilities...")

def forensic_analysis(user_query):
    print("🕵️ Performing digital forensic analysis...")

def steganography_detector(user_query):
    print("📷 Detecting hidden messages using steganalysis...")

def port_knocking_detector(user_query):
    print("🚪 Analyzing network traffic for port knocking attempts...")

def social_engineering_analysis(user_query):
    print("🗣️ Analyzing social engineering attacks...")



task_map = {
    "scan": scanner,
    "cracker": cracker,
    "phishing_detector": phishing_detector,
    "malware_analysis": malware_analysis,
    "web_vulnerability_scan": web_vulnerability_scan,
    "forensic_analysis": forensic_analysis,
    "steganography_detector": steganography_detector,
    "port_knocking_detector": port_knocking_detector,
    "social_engineering_analysis": social_engineering_analysis,
    "exploitation": runExploits,
    "whois_lookup": lookup_handler,
    "dns_lookup": lookup_handler,
    "ip_geolocation": lookup_handler,
    "ssl_certificate_lookup": lookup_handler,
    "mac_address_lookup": lookup_handler,
    "email_verification": lookup_handler,
    "threat_intelligence_lookup": lookup_handler,
    "domain_availability": lookup_handler,
}

def tasksfinder(user_query):
    client = AzureClient.get_client() 
    deployment = AzureClient.deployment

    history = memory.get_history() 
    #print(f"User history -> {history}")
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a cyber bot that is capable of various tasks."},
            {"role": "system", "content": f"User history -> {history}"},
            {"role": "user", "content": user_query},
        ],
        functions=functions,  
        stream=False
    )

    out = response.choices[0].message.function_call

    if out and hasattr(out, "name"):
        func_name = out.name
        task_func = task_map.get(func_name, lambda user_query: print("❌ Unknown function"))
        return task_func(user_query)

    output=response.choices[0].message.content
    memory.add_message(user_input=user_query,bot_response=output)
    return output
