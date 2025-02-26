
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()


class AzureClient:
    _instance = None
    deployment = os.getenv("DEPLOYMENT")  

    @classmethod
    def get_client(cls):
        if cls._instance is None:
            cls._instance = AzureOpenAI(
                api_version="2024-05-01-preview",
                azure_endpoint=os.getenv("ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_KEY")
            )
        return cls._instance
