import os
import json
import subprocess
from urllib.parse import urlparse
from Model_client import AzureClient

class WPScanHandler:
    def __init__(self):
        """
        Initializes the WPScanHandler by fetching the API key securely from environment variables.
        """
        self.api_key = os.getenv("WPSCAN_API_KEY")  # Secure API Key storage

        if not self.api_key:
            raise ValueError("❌ WPScan API key is missing! Set WPSCAN_API_KEY as an environment variable.")

    def is_valid_url(self, url):
        """
        Validates if the provided URL is correctly formatted.
        """
        parsed_url = urlparse(url)
        return bool(parsed_url.scheme and parsed_url.netloc)

    def scan(self, user_query):
        """
        Processes the user query, extracts the target URL, and performs a WPScan.
        """
        yield json.dumps({"status": "Performing wpscan ...."}) + "\n"

        client = AzureClient.get_client()
        deployment = AzureClient.deployment
        
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "Extract the target URL from the user's query."},
                {"role": "user", "content": user_query},
            ],
            functions=functions,
            stream=False
        )

        out = response.choices[0].message.function_call if response.choices else None
        if not out or not hasattr(out, 'arguments'):
            yield json.dumps({"error": "⚠ Could not extract target URL from query."}) + "\n"
            return

        try:
            params_dict = json.loads(out.arguments)
            target_url = params_dict.get("target_url", "")
            if isinstance(target_url, set):
                target_url = list(target_url)  # Ensure it's JSON serializable
        except json.JSONDecodeError:
            yield json.dumps({"error": "⚠ Invalid function arguments."}) + "\n"
            return

        if not self.is_valid_url(target_url):
            yield json.dumps({"error": "❌ Invalid URL! Please enter a valid website URL."}) + "\n"
            return

        yield json.dumps({"data": f"🔍 Scanning {target_url} with WPScan...", "istool": False, "tool_out": ""}) + "\n"
        print(f"🔍 Scanning {target_url} with WPScan...")

        command = [
            "wpscan",
            "--url", target_url,
            "--api-token", self.api_key,
            "--format", "json"
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            output = result.stdout.strip()
            if output:
                scan_results = json.loads(output)  # Convert JSON output to Python dictionary
                scan_results_str = json.dumps(scan_results, indent=2)
                yield json.dumps({"data": "✅ Scan completed.", "istool": True, "tool_out": scan_results_str}) + "\n"
            else:
                yield json.dumps({"error": "⚠ No output from WPScan. Check WPScan installation."}) + "\n"
        except subprocess.CalledProcessError as e:
            yield json.dumps({"error": f"⚠ WPScan execution failed: {e}"}) + "\n"
        except json.JSONDecodeError:
            yield json.dumps({"error": "⚠ Failed to parse WPScan JSON output. Please check WPScan installation."}) + "\n"

functions = [
    {
        "name": "scan",
        "description": "Scans a WordPress site for vulnerabilities using WPScan.",
        "parameters": {
            "type": "object",
            "properties": {
                "target_url": {
                    "type": "string",
                    "description": "The URL of the WordPress site to scan."
                }
            },
            "required": ["target_url"]
        }
    }
]
