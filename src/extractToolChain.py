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
                    "You are provided with a list of tools in 'functions' that you can use to fulfill a user's query.\n\n"
                    "Your task is to create a logical sequence (chain) of tool invocations to fully address the user's request.\n\n"
                    "For each step:\n"
                    "- Select the appropriate tool from the available 'functions'."
                    "- If the tool requires input parameters, extract them directly from the user query or reference a previous step using the 'depends_on' field."
                    "- When referencing previous output:"
                    "- Leave the 'parameters' field empty."
                    "- Use 'depends_on' to specify:"
                    "- The step number of the tool providing the required output."
                    "- A field name , this should include what you want to extract from the output of the previous tool this can be like a statement or command"
                    "- A list of possible alternative field names in 'field_aliases', which may appear in the previous tool's output."
                    "- Use the 'command' field to briefly describe the purpose or intent of the step, similar to a shell-style instruction."
                    "Use the following JSON structure strictly:\n\n"
                    "{\n"
                    "  \"steps\": [\n"
                    "    {\n"
                    "      \"step\": <step_number>,\n"
                    "      \"tool\": \"<tool_name>\",\n"
                    "      \"parameters\": { <key_value_pairs_if_direct_input> },\n"
                    "      \"command\": \"<brief_instruction>\",\n"
                    "      \"depends_on\": {\n"
                    "        \"step\": <step_number>,\n"
                    "        \"field\": \"<field_to_extract>\",\n"
                    "        \"field_aliases\": [\"<alias1>\", \"<alias2>\"]\n"
                    "      }\n"
                    "    },\n"
                    "    ...\n"
                    "  ]\n"
                    "}\n\n"
                    "Notes:\n"
                    "- Only include 'depends_on' if the tool input comes from a previous step.\n"
                    "- If 'depends_on' is used, leave the 'parameters' field empty, and if the depends_on filed doesn't contain any value leave it empty\n"
                    "- Output only valid JSON. Do not include any explanations, comments, or markdown."
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

                try:
                    parsed_response = json.loads(content)
                    tool_chain = parsed_response.get("steps", [])

                    for step in tool_chain:
                        if "tool" in step:
                            # Remove prefix if exists (optional)
                            step["tool"] = step["tool"].replace("functions.", "")

                        # Normalize or validate dependency if present
                        if "depends_on" in step:
                            depends = step["depends_on"]
                            if "step" not in depends or "field" not in depends:
                                print(f"Warning: Incomplete dependency info in step {step['step']}")
                            else:
                                print(f"Step {step['step']} depends on step {depends['step']}, field '{depends['field']}'")

                except json.JSONDecodeError:
                    print("❌ Invalid JSON format received from response.")
            else:
                print("⚠️ No content found in the response message.")
        else:
            print("⚠️ No choices found in response.")

    except Exception as e:
        print(f"🔥 Error extracting tools: {e}")

    
    return tool_chain
