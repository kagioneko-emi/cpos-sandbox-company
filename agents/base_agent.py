import os
from openai import AzureOpenAI

class BaseAgent:
    def __init__(self, cpos):
        self.cpos = cpos
        # Azure OpenAI settings from environment variables
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
        
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version="2024-08-01-preview", # Current stable preview version
            azure_endpoint=endpoint
        )

    def call_ai(self, system_prompt, user_prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            self.cpos.log_audit("System", "ai_error", {"error": str(e)})
            return None
