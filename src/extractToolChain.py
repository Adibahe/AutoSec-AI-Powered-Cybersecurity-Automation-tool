import json
import re
from Model_client import AzureClient
from functions import functions

def extract_tool_chain(user_query):
    tools = []
    
    
    client = AzureClient.get_client() 
    deployment = AzureClient.deployment
    
   
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are provided with a map of tools that you can execute in 'functions'. Your task is to build a chain of tools to process the user query."},
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

                matches = re.findall(r"functions\.(\w+)", content)
                if matches:
                    tools = [{"name": match, "params": {}} for match in matches]
                else:
                    print("No functions found in response text.")
            else:
                print("No content found in the response message.")
        else:
            print("No choices found in response.")
    
    except Exception as e:
        print(f"Error extracting tools: {e}")
    
    return tools
