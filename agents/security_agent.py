import json
from .base_agent import BaseAgent

class SecurityAgent(BaseAgent):
    def audit_code(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
            
        system_prompt = "You are a Cyber Security Auditor. Analyze the provided Python code for vulnerabilities. Output findings in JSON format: [{'severity': 'HIGH/MEDIUM/LOW', 'id': 'NAME', 'description': '...'}]"
        user_prompt = f"Code:\n{code}\n\nPerform audit and output JSON only."
        
        response_text = self.call_ai(system_prompt, user_prompt)
        
        try:
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            findings = json.loads(response_text.strip())
        except:
            findings = []
            
        for finding in findings:
            self.cpos.record_pointer("finding", file_path, f"{finding['id']}: {finding['description']}")
            
        self.cpos.log_audit("SecurityAgent", "audit_completed", {"findings_count": len(findings)})
        return findings
