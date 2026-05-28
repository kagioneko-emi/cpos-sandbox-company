import json
from .base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    def generate_spec(self, custom_prompt=None):
        system_prompt = "You are a Senior Product Manager. Generate a JSON specification for a simple Python tool. Output MUST be valid JSON only."
        if custom_prompt:
            user_prompt = f"Design a Python tool based on this GitHub Issue request:\n{custom_prompt}\n\nProvide: project_name, description, requirements (list), and target_file (path in outputs/python_tools/)."
        else:
            user_prompt = "Design a small Python CLI tool. Provide: project_name, description, requirements (list), and target_file (path in outputs/python_tools/)."
        
        response_text = self.call_ai(system_prompt, user_prompt)
        
        try:
            # Try to extract JSON from the response
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            spec = json.loads(response_text.strip())
        except:
            # Fallback
            spec = {
                "project_name": "DefaultTool",
                "description": "A fallback tool due to AI parsing error.",
                "requirements": ["python3"],
                "target_file": "outputs/python_tools/fallback.py"
            }
            
        self.cpos.log_audit("PlannerAgent", "generated_spec", spec)
        return spec
