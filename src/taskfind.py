from openai import AzureOpenAI
from Model_client import AzureClient
from NmapHandler import scanner
from CrackerHandler import cracker
from ExploitHandler import runExploits

functions = [
    {
        "name": "scan",
        "description": "Performs a network scan using tools like nmap.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "cracker",
    "   description": "Handles any task related to breaking or cracking passwords.",
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
    "exploitation": runExploits
}

def tasksfinder(user_query):
    client = AzureClient.get_client() 
    deployment = AzureClient.deployment

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a cyber bot that is capable of various tasks."},
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

    return response.choices[0].message.content
