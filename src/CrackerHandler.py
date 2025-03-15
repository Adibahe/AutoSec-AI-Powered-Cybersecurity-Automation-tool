import os
import subprocess
import json
from Model_client import AzureClient

def identify_hash_type(hash_value):
    """Uses hash-identifier to determine the most likely hash type."""
    try:
        result = subprocess.run(
            ["hashid", "-m", hash_value], capture_output=True, text=True, check=True
        )
        output = result.stdout.strip()
        
        # Extract the first detected hash mode from output
        for line in output.split("\n"):
            if line.startswith("Hash-mode"):
                return line.split(":")[1].strip()  # Extract Hashcat mode number
        
    except subprocess.CalledProcessError:
        return "0"  # Default to MD5 if detection fails
    
    return "0"  # Default to MD5 if nothing was detected

def crack_hash(hash_value, hash_type=None, wordlist_path="rockyou.txt", additional_args=[]):
    print("Starting hash cracking task...")

    # If no hash_type is provided, detect it
    if not hash_type:
        print("Detecting hash type...")
        hash_type = identify_hash_type(hash_value)
        print(f"Detected hash type: {hash_type}")

    # Check if the given hash_value is a file
    if os.path.isfile(hash_value):
        command = [
            "hashcat", "-m", str(hash_type), hash_value, wordlist_path, "--show"
        ] + additional_args
    else:
        command = [
            "hashcat", "-m", str(hash_type), "-a", "0", "--show"
        ] + additional_args
        command.extend(["--hash", hash_value, wordlist_path])  # Pass hash directly

    print("Running Hashcat command:", " ".join(command))

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout.strip()

        if not output:
            return "Hashcat was unable to crack the hash."
        
    except subprocess.CalledProcessError as e:
        output = f"Error: {e.stderr.strip()}"
    
    return output



def cracker(user_query):
    client = AzureClient.get_client()
    deployment = AzureClient.deployment
    
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a cyber bot specializing in password cracking. You execute functions to process user queries."},
            {"role": "user", "content": user_query},
        ],
        functions=functions,
        stream=False
    )
    
    out = response.choices[0].message.function_call
    
    if out is not None:
        print("Executing hash cracking function...")
        params = json.loads(out.arguments)
        
        hash_value = params.get("hash_value", "")
        hash_type = params.get("hash_type")
        
        if not hash_type:
            print("No hash type provided. Detecting automatically...")
            hash_type = identify_hash_type(params["hash_value"])

        wordlist_path = params.get("wordlist_path", "rockyou.txt")
        additional_args = params.get("additional_args", [])
        
        cracked_result = crack_hash(hash_value, hash_type, wordlist_path, additional_args)
        
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a cyber bot capable of cracking password hashes."},
                {"role": "system", "content": f"The Hashcat command was executed successfully.\nOutput:\n{cracked_result}"}
            ],
            stream=False
        )
        print(response.choices[0].message.content)

functions = [
    {
        "name": "crack_hash",
        "description": "Uses Hashcat to crack password hashes using a wordlist.",
        "parameters": {
            "type": "object",
            "properties": {
                "hash_value": {
                    "type": "string",
                    "description": "The hash to be cracked OR a file containing hashes."
                },
                "hash_type": {
                    "type": "integer",
                    "description": """Hash mode (e.g., 0 for MD5, 100 for SHA1, 1800 for SHA512).
If not provided, the script will attempt to detect it automatically."""
                },
                "wordlist_path": {
                    "type": "string",
                    "description": "Path to the wordlist file."
                },
                "additional_args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": """List of Hashcat arguments for customization.

### Common Arguments:
- **Attack Mode:** `-a 0` (Dictionary), `-a 3` (Mask), `-a 1` (Combinator)
- **Rules:** `-r rules/best64.rule`
- **Optimizations:** `--force`, `--optimized-kernel-enable`
- **Performance Tuning:** `-w 3` (Faster cracking)
- **Mask Attack:** `?d?d?d?d` (Four-digit PIN)
- **Output to File:** `--outfile=result.txt`

Example: `["-a 0", "-r rules/best64.rule"]`
"""
                }
            },
            "required": ["hash_value", "wordlist_path"]
        }
    }
]


