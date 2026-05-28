import subprocess
import os

class SandboxRunner:
    def __init__(self, cpos):
        self.cpos = cpos

    def run_tests(self, file_path):
        results = {
            "exit_code": 0,
            "stdout": "",
            "stderr": ""
        }
        
        # 1. Run Ruff
        print(f"[*] [Sandbox] Running ruff check on {file_path}...")
        try:
            res = subprocess.run(["ruff", "check", file_path], capture_output=True, text=True)
            results["stdout"] += res.stdout
            results["stderr"] += res.stderr
            if res.returncode != 0:
                results["exit_code"] = res.returncode
        except FileNotFoundError:
            results["stderr"] += "Error: 'ruff' not found in environment.\n"
            results["exit_code"] = 1

        # 2. Run Mock Pytest (simulating test run)
        # In MVP, we just check if it's executable
        print(f"[*] [Sandbox] Verifying execution of {file_path}...")
        try:
            # We don't actually want to execute it if it's dangerous, but for MVP/simulation:
            res = subprocess.run(["python3", "-m", "py_compile", file_path], capture_output=True, text=True)
            if res.returncode != 0:
                results["exit_code"] = res.returncode
                results["stderr"] += res.stderr
        except Exception as e:
            results["stderr"] += f"Execution check failed: {e}\n"
            results["exit_code"] = 1

        self.cpos.log_audit("SandboxRunner", "sandbox_completed", {"exit_code": results["exit_code"]})
        return results
