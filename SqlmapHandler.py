import subprocess
import json
from Model_client import AzureClient
from Memory import MemorySingleton

memory = MemorySingleton()

def sqlmap_scanner(user_query):
    print("🔍 Starting SQL Injection scan...")

    client = AzureClient.get_client()
    deployment = AzureClient.deployment

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a cyber bot that runs SQL injection detection using sqlmap."},
            {"role": "user", "content": user_query},
        ],
        functions=functions,
        stream=False
    )

    out = response.choices[0].message.function_call

    if out is not None:
        print("⚡ Running SQLMap...")
        try:
            params = json.loads(out.arguments)
            url = params.get("url", "").strip()
            arguments = params.get("arguments", [])

            if not url.startswith("http"):
                raise ValueError("Invalid URL format. Please provide a full valid URL.")

            args_str = " ".join(arguments)
            command = f"sqlmap -u \"{url}\" {args_str} --batch"

            print(f"🔹 Executing: {command}")

            output = sqlmap_scan(url, arguments)

            structured_output = format_sqlmap_output(output)

            # Retrieve history from memory
            history = memory.get_history()

            response = client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": "You are a cyber bot capable of various tasks."},
                    {"role": "system", "content": f"User history -> {history}"},
                    {"role": "system", "content": f"An SQLMap command was run -> {command}\n\n🔍 **Scan Results:**\n{structured_output}"}
                ],
                stream=False
            )

            output_message = response.choices[0].message.content
            memory.add_message(user_input=user_query, bot_response=output_message)

            print(output_message)

        except Exception as e:
            print(f"❌ Error: {str(e)}")


def sqlmap_scan(url, arguments):
    """Runs SQLMap with user-defined arguments and returns structured output."""
    args_str = " ".join(arguments)
    command = f"sqlmap -u \"{url}\" {args_str} --batch"

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {"output": result.stdout, "error": result.stderr}
    except Exception as e:
        return {"error": str(e)}

def format_sqlmap_output(raw_output):
    """Formats SQLMap output to make it more readable."""
    output_text = raw_output.get("output", "")
    error_text = raw_output.get("error", "")

    structured_result = "📌 **SQLMap Scan Report:**\n"
    
    if "back-end DBMS" in output_text:
        structured_result += "✅ **Database Identified:** " + extract_line(output_text, "back-end DBMS") + "\n"
    
    if "available databases" in output_text:
        structured_result += "📂 **Databases Found:** " + extract_line(output_text, "available databases") + "\n"

    if "available tables" in output_text:
        structured_result += "📋 **Tables Found:** " + extract_line(output_text, "available tables") + "\n"

    if "columns" in output_text:
        structured_result += "📊 **Columns Found:** " + extract_line(output_text, "columns") + "\n"

    if "WAF" in output_text:
        structured_result += "🚧 **Web Application Firewall (WAF) Detected!**\n"

    if error_text:
        structured_result += f"❌ **Errors:**\n```\n{error_text}\n```"

    return structured_result or "⚠️ No injection vulnerabilities found."

def extract_line(text, keyword):
    """Extracts a specific line of text containing a keyword."""
    for line in text.split("\n"):
        if keyword in line:
            return line.strip()
    return "Not Found"


# Functions that the AI can trigger
functions = [
    {
        "name": "sqlmap_scan",
        "description": "Runs an SQL injection scan on a given URL using sqlmap.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The target URL to test for SQL injection (e.g., 'http://example.com/page?id=1')."
                },
                "arguments": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "List of SQLMap arguments to customize the scan.\n\n"
                        "🔹 **Available SQLMap Arguments:**\n"
                        "- 🏦 **Database Enumeration**: `--dbs`\n"
                        "- 📂 **Dump Entire Database**: `--dump`\n"
                        "- 📋 **Retrieve Tables**: `--tables`\n"
                        "- 📊 **Retrieve Columns**: `--columns`\n"
                        "- 🔍 **Check for WAF**: `--identify-waf`\n"
                        "- ⚠️ **Risk Level (Higher = More Aggressive)**: `--risk=3`\n"
                        "- 🚀 **Level of Testing (Higher = More Tests)**: `--level=5`\n"
                        "- 🔄 **Bypass WAF**: `--tamper=randomcase`\n"
                        "- 🏎️ **Increase Speed**: `--threads=10`\n"
                        "- 🖥 **OS Shell Access (If Vulnerable)**: `--os-shell`\n"
                        "- 🔑 **Enumerate Usernames**: `--users`\n"
                        "- 🔐 **Retrieve Password Hashes**: `--passwords`\n"
                        "- 📎 **Enumerate Privileges**: `--privileges`\n"
                        "- 🎭 **Enumerate Roles**: `--roles`\n\n"
                        "📌 **Example:**\n"
                        "{\n"
                        '    "url": "http://example.com/page?id=1",\n'
                        '    "arguments": ["--dbs", "--level=5", "--risk=3"]\n'
                        "}"
                    )
                }
            },
            "required": ["url"]
        }
    }
]
