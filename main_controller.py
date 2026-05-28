import os
import sys
import time
import json
from cpos.core import CPOSCore
from agents.planner_agent import PlannerAgent
from agents.dev_agent import DevAgent
from agents.security_agent import SecurityAgent
from agents.review_agent import ReviewAgent
from sandbox.runner import SandboxRunner

class CorporateCycle:
    def __init__(self):
        self.cpos = CPOSCore()
        self.planner = PlannerAgent(self.cpos)
        self.dev = DevAgent(self.cpos)
        self.security = SecurityAgent(self.cpos)
        self.sandbox = SandboxRunner(self.cpos)
        self.review = ReviewAgent(self.cpos)
        self.state_file = "cpos/state.json"

    def save_state(self, state_data):
        os.makedirs("cpos", exist_ok=True)
        with open(self.state_file, "w") as f:
            json.dump(state_data, f)

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                return json.load(f)
        return None

    def run_to_review(self):
        print("=== CPOS Agent Sandbox Company: AI Edition ===")
        self.cpos.log_audit("System", "session_started")

        # 1. Planning
        print("\n[Phase 1] Planning...")
        spec = self.planner.generate_spec()
        
        # 2. Development
        print("\n[Phase 2] Development...")
        file_path = self.dev.generate_code(spec)
        
        # 3. Security Audit & Feedback Loop
        print("\n[Phase 3] Security Audit...")
        findings = self.security.audit_code(file_path)
        
        if findings:
            print(f"  - {len(findings)} findings detected. Initiating Auto-Fix loop...")
            self.cpos.log_audit("System", "auto_fix_triggered", {"findings_count": len(findings)})
            
            print("\n[Phase 3.1] Development (Auto-Fix)...")
            file_path = self.dev.generate_code(spec, findings=findings)
            
            print("\n[Phase 3.2] Security Audit (Re-check)...")
            findings = self.security.audit_code(file_path)
            
        # 4. Sandbox Testing
        print("\n[Phase 4] Sandbox Verification...")
        sandbox_results = self.sandbox.run_tests(file_path)
        
        # 5. Final Review (AI)
        print("\n[Phase 5] AI Review Decision...")
        decision = self.review.decide(spec, file_path, findings)
        
        # Save state and wait for human
        state_data = {
            "spec": spec,
            "file_path": file_path,
            "findings": findings,
            "ai_decision": decision,
            "status": "WAITING_FOR_HUMAN"
        }
        self.save_state(state_data)
        self.cpos.log_audit("System", "waiting_for_human", {"ai_decision": decision})
        print(f"\n[*] AI Decision: {decision}. Waiting for Human Approval...")

    def complete_cycle(self, human_decision):
        state = self.load_state()
        if not state:
            return
        
        print(f"\n[Phase 6] Human Final Decision: {human_decision}")
        self.cpos.log_audit("System", "human_decision", {"decision": human_decision})
        
        if os.path.exists(self.state_file):
            os.remove(self.state_file)
            
        if human_decision == "APPROVE":
            print("[!] RELEASE SUCCESSFUL!")
            self.cpos.log_audit("System", "session_completed", {"status": "RELEASED"})
        elif human_decision == "RETRY":
            print("[!] RETRY REQUESTED BY HUMAN. Restarting cycle...")
            self.cpos.log_audit("System", "human_retry_requested", {"reason": "Human requested AI to fix findings and retry"})
            self.run_to_review()
        else:
            print("[X] RELEASE REJECTED BY HUMAN.")
            self.cpos.log_audit("System", "session_completed", {"status": "REJECTED"})

def main():
    cycle = CorporateCycle()
    cycle.run_to_review()

if __name__ == "__main__":
    main()
