from openai import AzureOpenAI
from Model_client import AzureClient
from NmapHandler import scanner
from CrackerHandler import cracker
from ExploitHandler import runExploits
from LookupHandler import lookup_handler
from Memory import MemorySingleton
import subprocess
import re

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
        "name": "sqlmap_scan",
        "description": "Performs an SQL Injection scan using SQLMap.",
        "parameters": {
            "type": "object",
            "properties": {
                "target_url": {
                    "type": "string",
                    "description": "The target URL to test for SQL injection."
                }
            },
            "required": ["target_url"]
        }
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

def sqlmap_scan(user_query):
    target_url = extract_target_url(user_query)
    if not target_url:
        return "❌ Error: No valid URL found in query."

    print(f"🚀 Running SQLMap on: {target_url}")

    try:
        command = [
            "sqlmap",
            "-u", target_url,
            "--dbs",
            "--batch"
        ]
        
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            structured_output = parse_sqlmap_output(result.stdout)
            return f"✅ SQLMap Scan Complete:\n{structured_output}"
        else:
            return f"⚠ SQLMap encountered an error:\n{result.stderr}"
    except Exception as e:
        return f"❌ Exception occurred: {str(e)}"

def parse_sqlmap_output(output):
    dbms_match = re.search(r"back-end DBMS: (.+?)", output)
    dbms = dbms_match.group(1) if dbms_match else "Unknown"

    databases_match = re.findall(r"available databases \[\d+\]:\n- (.+)\n", output, re.MULTILINE)
    databases = "\n".join(databases_match) if databases_match else "No databases found"
    
    return f"**Detected DBMS:** {dbms}\n**Databases:**\n{databases}"
