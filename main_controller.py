import os
import sys
from cpos.core import CPOSCore
from agents.planner_agent import PlannerAgent
from agents.dev_agent import DevAgent
from agents.security_agent import SecurityAgent
from agents.review_agent import ReviewAgent
from sandbox.runner import SandboxRunner

def main():
    print("=== CPOS Agent Sandbox Company: AI Edition ===")
    
    # Initialize Core
    cpos = CPOSCore()
    cpos.log_audit("System", "session_started")

    # Initialize Agents
    planner = PlannerAgent(cpos)
    dev = DevAgent(cpos)
    security = SecurityAgent(cpos)
    sandbox = SandboxRunner(cpos)
    review = ReviewAgent(cpos)

    # 1. Planning
    print("\n[Phase 1] Planning...")
    spec = planner.generate_spec()
    print(f"Product Spec: {spec.get('project_name', 'Unknown')}")

    # 2. Development
    print("\n[Phase 2] Development...")
    file_path = dev.generate_code(spec)
    print(f"Code generated at: {file_path}")

    # 3. Security Audit
    print("\n[Phase 3] Security Audit...")
    findings = security.audit_code(file_path)
    if findings:
        print(f"  - {len(findings)} findings detected.")
    else:
        print("  - No security findings.")

    # 4. Sandbox Testing
    print("\n[Phase 4] Sandbox Verification...")
    sandbox_results = sandbox.run_tests(file_path)
    if sandbox_results["exit_code"] == 0:
        print("  - Sandbox verification passed.")
    else:
        print("  - Sandbox verification failed.")

    # 5. Final Review
    print("\n[Phase 5] Final Review Decision...")
    decision = review.decide(spec, file_path, findings)
    
    print(f"Decision: {decision}")

    cpos.log_audit("System", "session_completed", {"decision": decision})
    print("\n=== Cycle Completed. Audit log updated in cpos/audit_log.jsonl ===")

if __name__ == "__main__":
    main()
