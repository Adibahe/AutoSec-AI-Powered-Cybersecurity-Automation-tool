import requests
import json

def pretty_print(data):
    """Formats and prints JSON output in a readable way."""
    print(json.dumps(data, indent=4, sort_keys=True))

def whois_lookup(query, api_key):
    """Queries the WhoisXML API for domain names, IP addresses, or ASNs."""
    base_url = "https://www.whoisxmlapi.com/whoisserver/WhoisService"
    url = f"{base_url}?apiKey={api_key}&domainName={query}&outputFormat=json&type=_all"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        pretty_print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error in Whois Lookup: {e}")

def dns_lookup(domain, api_key):
    """Queries the WhoisXML API for DNS records."""
    base_url = "https://www.whoisxmlapi.com/whoisserver/DNSService"
    url = f"{base_url}?apiKey={api_key}&domainName={domain}&outputFormat=json&type=_all"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        pretty_print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error in DNS Lookup: {e}")

def ip_geolocation(ip, api_key):
    """Queries the WhoisXML API for IP geolocation."""
    base_url = "https://ip-geolocation.whoisxmlapi.com/api/v1"
    url = f"{base_url}?apiKey={api_key}&ipAddress={ip}&outputFormat=json&type=_all"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        pretty_print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error in IP Geolocation: {e}")
    
def email_verification(email, api_key):
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

def threat_intelligence_lookup(ioc, api_key):
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
    
def ssl_certificate_lookup(domain, api_key):
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

def mac_address_lookup(mac, api_key):
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

def domain_availability(domain, api_key):
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

def main():
    api_key = ""
    
    while True:
        print("\nMenu:")
        print("1. Whois Lookup")
        print("2. DNS Lookup")
        print("3. IP Geolocation")
        print("4.email verification")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                query = input("Enter domain name: ")
                whois_lookup(query, api_key)
            case "2":
                query = input("Enter domain name: ")
                dns_lookup(query, api_key)
            case "3":
                ip = input("Enter IP address: ")
                ip_geolocation(ip, api_key)

            case "4":
                email = input("Enter email address: ")
                email_verification(email, api_key)

            case "5":
                domain = input("Enter domain name: ")
                ssl_certificate_lookup(domain, api_key)

            case "6":
                mac_address = input("Enter mac address: ")
                mac_address_lookup(mac_address, api_key)
            
            case "7":
                ioc = input("Enter IOC: ")
                threat_intelligence_lookup(ioc, api_key)

            case "8":
                domain = input("Enter domain: ")
                domain_availability(domain, api_key)

            case "0":
                print("Exiting...")
                break
            case _:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
