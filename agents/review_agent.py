from .base_agent import BaseAgent

class ReviewAgent(BaseAgent):
    def decide(self, spec, code_path, findings):
        system_prompt = "You are a CTO. Review the development cycle results and decide whether to APPROVE or REJECT the release. Output: 'APPROVE' or 'REJECT' followed by a short reason."
        user_prompt = f"Spec: {spec}\nCode Path: {code_path}\nSecurity Findings: {findings}\n\nMake your decision."
        
        decision_text = self.call_ai(system_prompt, user_prompt)
        
        decision = "APPROVE" if "APPROVE" in decision_text.upper() else "REJECT"
        
        self.cpos.log_audit("ReviewAgent", "review_decision", {
            "decision": decision,
            "reason": decision_text
        })
        return decision
