import requests
import json
import os
from Model_client import AzureClient

functions = []  # Ensure functions is defined before extending it
api_key = os.getenv("WHOISXML_API_KEY")

def pretty_print(data, task_name="Generic Task"):
    """Formats and prints JSON output in a readable way and sends it to the AI model."""
    formatted_data = json.dumps(data, indent=4, sort_keys=True)
    print(formatted_data)
    process_and_send_output(task_name, formatted_data)

def process_and_send_output(task_name, processed_output):
    """Sends processed function output to the AI model."""
    print("inside process_and_send_output")
    client = AzureClient.get_client()
    deployment = AzureClient.deployment
    truncated_output = processed_output[:4000]  # Prevent sending too much data

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a cyber bot that executes functions to process user queries."},
            {"role": "system", "content": f"The {task_name} task was executed.\nOutput:\n{truncated_output}"}
        ],
        stream=False
    )

    print("🔹 Response sent to AI Model:")
    print(response.choices[0].message.content)  # Print for debugging
    return response.choices[0].message.content  # Fixed typo here



def whois_lookup(query):
    """Queries the WhoisXML API for domain names, IP addresses, or ASNs."""
    base_url = "https://www.whoisxmlapi.com/whoisserver/WhoisService"
    url = f"{base_url}?apiKey={api_key}&domainName={query}&outputFormat=json&type=_all"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        pretty_print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error in Whois Lookup: {e}")
    return None

def dns_lookup(domain):
    """Queries the WhoisXML API for DNS records securely."""
    
    base_url = "https://www.whoisxmlapi.com/whoisserver/DNSService"
    url = f"{base_url}?apiKey={api_key}&domainName={domain}&outputFormat=json&type=_all"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        pretty_print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error in Whois Lookup: {e}")
    return None

def ip_geolocation(ip):
    """Queries the WhoisXML API for IP geolocation."""
    base_url = "https://ip-geolocation.whoisxmlapi.com/api/v1"
    url = f"{base_url}?apiKey={api_key}&ipAddress={ip}&outputFormat=json&type=_all"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        pretty_print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error in IP Geolocation: {e}")
    
def email_verification(email):
    """
    Verifies an email address using the WhoisXML API v3.
    """
    url = f"https://emailverification.whoisxmlapi.com/api/v3?apiKey={api_key}&emailAddress={email}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        pretty_print(data)
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def threat_intelligence_lookup(ioc):
    """
    Queries the WhoisXML Threat Intelligence API for a given IOC (Indicator of Compromise).
    """
    url = f"https://threat-intelligence.whoisxmlapi.com/api/v1?apiKey={api_key}&ioc={ioc}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        pretty_print(data)
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    
def ssl_certificate_lookup(domain):
    """
    Queries the WhoisXML API for SSL certificate details.
    """
    url = f"https://ssl-certificates.whoisxmlapi.com/api/v1?apiKey={api_key}&domainName={domain}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        pretty_print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error in SSL Certificate Lookup: {e}")

def mac_address_lookup(mac):
    """
    Queries the WhoisXML API for MAC address details.
    """
    url = f"https://mac-address.whoisxmlapi.com/api/v1?apiKey={api_key}&macAddress={mac}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        pretty_print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error in MAC Address Lookup: {e}")

def domain_availability(domain):
    """
    Checks if a domain is available for registration using WhoisXML API.
    """
    url = f"https://domain-availability.whoisxmlapi.com/api/v1?apiKey={api_key}&credits=DA&domainName={domain}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        pretty_print(data)
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None



def lookup_handler(user_query):
    print("Performing lookup task...")
    client = AzureClient.get_client()
    deployment = AzureClient.deployment
    
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a cyber bot specializing in various lookup services."},
            {"role": "user", "content": user_query},
        ],
        functions=functions,
        stream=False
    )
    
    out = response.choices[0].message.function_call
    
    if out is not None:
        print("Executing lookup function...")
        params = json.loads(out.arguments)
        lookup_type = out.name  # Extract function name

        lookup_functions = {
            "whois_lookup": whois_lookup,
            "dns_lookup": dns_lookup,
            "ip_geolocation": ip_geolocation,
            "email_verification": email_verification,
            "threat_intelligence_lookup": threat_intelligence_lookup,
            "ssl_certificate_lookup": ssl_certificate_lookup,
            "mac_address_lookup": mac_address_lookup,
            "domain_availability": domain_availability
        }
        
        if lookup_type in lookup_functions:
            query_param = params.get("query", params.get("domain", params.get("ip", params.get("email", params.get("ioc", params.get("mac", ""))))))
            if not query_param:
                print("❌ Error: No valid input extracted from the query.")
                return
            
            lookup_functions[lookup_type](query_param)
            
functions.extend([
    {"name": "whois_lookup", "description": "Performs a WHOIS lookup on a domain or IP address.", "parameters": {"type": "object", "properties": {"query": {"type": "string", "description": "The domain name or IP address to look up."}}, "required": ["query"]}},
    {"name": "dns_lookup", "description": "Performs a DNS lookup for a given domain.", "parameters": {"type": "object", "properties": {"domain": {"type": "string", "description": "The domain name to look up."}}, "required": ["domain"]}},
    {"name": "ip_geolocation", "description": "Performs IP geolocation lookup.", "parameters": {"type": "object", "properties": {"ip": {"type": "string", "description": "The IP address to look up."}}, "required": ["ip"]}},
    {"name": "email_verification", "description": "Verifies an email address.", "parameters": {"type": "object", "properties": {"email": {"type": "string", "description": "The email address to verify."}}, "required": ["email"]}},
    {"name": "threat_intelligence_lookup", "description": "Queries threat intelligence for a given IOC.", "parameters": {"type": "object", "properties": {"ioc": {"type": "string", "description": "Indicator of compromise to check."}}, "required": ["ioc"]}},
    {"name": "ssl_certificate_lookup", "description": "Queries SSL certificate details.", "parameters": {"type": "object", "properties": {"domain": {"type": "string", "description": "The domain name to look up."}}, "required": ["domain"]}},
    {"name": "mac_address_lookup", "description": "Queries MAC address details.", "parameters": {"type": "object", "properties": {"mac": {"type": "string", "description": "The MAC address to look up."}}, "required": ["mac"]}},
    {"name": "domain_availability", "description": "Checks if a domain is available for registration.", "parameters": {"type": "object", "properties": {"domain": {"type": "string", "description": "The domain name to check."}}, "required": ["domain"]}}
])




