import json
import re
from Model_client import AzureClient
from functions import functions

def extract_tool_chain(user_query):
    tool_chain = []
    
    client = AzureClient.get_client() 
    deployment = AzureClient.deployment
    
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system", 
                "content": (
                    "You are provided with a map of tools that you can execute in 'functions'. "
                    "Your task is to build a structured chain of tools to process the user query.\n"
                    "For each step:\n"
                    "- Select the appropriate tool based on the user query choose a tool form the 'functions'.\n"
                    "- Specify the parameters, either from the user query or from the previous tool output.\n"
                    "- Generate a command-like instruction for this step (what is required by this steps tool), referring to parameters .\n"
                    "- Ensure the tools are executed in a logical order.\n\n"
                    "Return the output strictly in the following JSON format:\n\n"
                    "{\n"
                    "    \"steps\": [\n"
                    "        {\n"
                    "            \"step\": <step_number>,\n"
                    "            \"tool\": \"<tool_name>\",\n"
                    "            \"parameters\": { <parameters_key_value_pairs> },\n"
                    "            \"command\": \"<instruction for executing the tool>\"\n"
                    "        },\n"
                    "        ...\n"
                    "    ]\n"
                    "}\n\n"
                    "Do not include any additional explanations or text outside of the JSON format."
                )
            },
            {"role": "user", "content": user_query}  
        ],
        functions=functions,  
        stream=False
    )

    try:
        if hasattr(response, "choices") and response.choices:
            first_choice = response.choices[0]

            if hasattr(first_choice.message, "content") and first_choice.message.content:
                content = first_choice.message.content
                
                # Ensure the response is valid JSON
                try:
                    parsed_response = json.loads(content)
                    tool_chain = parsed_response.get("steps", [])
                except json.JSONDecodeError:
                    print("Invalid JSON format received from response.")
            else:
                print("No content found in the response message.")
        else:
            print("No choices found in response.")
    
    except Exception as e:
        print(f"Error extracting tools: {e}")
    
    return tool_chain
