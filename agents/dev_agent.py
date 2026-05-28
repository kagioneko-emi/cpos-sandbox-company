import os
import subprocess
from .base_agent import BaseAgent

class DevAgent(BaseAgent):
    def generate_code(self, spec, findings=None):
        target_path = spec["target_file"]
        
        if findings and os.path.exists(target_path):
            with open(target_path, "r", encoding="utf-8") as f:
                old_code = f.read()
            system_prompt = "You are an Expert Python Security Developer. Fix the vulnerabilities in the provided code based on the security findings. Output ONLY the raw Python code, no markdown blocks."
            user_prompt = f"Original Code:\n{old_code}\n\nSecurity Findings to Fix:\n{findings}\n\nWrite the fixed code."
        else:
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
        
        # Optional GitHub Integration: AI Commits its own code
        # We attempt to commit and push to a feature branch if git is available
        branch_name = f"feature/ai-generated-{spec['project_name'].lower().replace(' ', '-')}"
        git_status = "Skipped (Git not available or not configured)"
        
        try:
            # Check if inside a git repository
            if subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], capture_output=True).returncode == 0:
                subprocess.run(["git", "checkout", "-b", branch_name], check=False, capture_output=True)
                subprocess.run(["git", "add", target_path], check=False, capture_output=True)
                subprocess.run(["git", "commit", "-m", f"feat(AI): Generate {spec['project_name']} based on spec"], check=False, capture_output=True)
                
                # We attempt to push. In Azure Container Apps, it might fail without proper auth,
                # but we log the attempt as a demonstration of "Agentic Capability".
                push_result = subprocess.run(["git", "push", "origin", branch_name], capture_output=True)
                if push_result.returncode == 0:
                    git_status = f"Successfully pushed to {branch_name}"
                else:
                    git_status = f"Committed locally to {branch_name}, push failed (Auth required)"
                    
        except Exception as e:
            git_status = f"Git operation failed: {e}"
            
        self.cpos.log_audit("DevAgent", "git_integration", {"status": git_status, "branch": branch_name})
        
        return target_path
