import os
from .base_agent import BaseAgent

class DevAgent(BaseAgent):
    def generate_code(self, spec):
        system_prompt = "You are an Expert Python Developer. Write a single-file Python script based on the provided specification. The code should be functional but can include complex logic."
        user_prompt = f"Spec: {spec}\n\nWrite the code. Output ONLY the raw Python code, no markdown blocks."
        
        code = self.call_ai(system_prompt, user_prompt)
        
        # Clean up if AI included markdown blocks
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0]
        elif "```" in code:
            code = code.split("```")[1].split("```")[0]
            
        target_path = spec["target_file"]
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(code.strip())
        
        self.cpos.log_audit("DevAgent", "generated_code", {"file": target_path})
        self.cpos.record_pointer("code", target_path, f"Initial implementation of {spec['project_name']}")
        return target_path
