import json
import os
from datetime import datetime

class CPOSCore:
    def __init__(self, base_dir="cpos"):
        self.base_dir = base_dir
        self.audit_log_path = os.path.join(base_dir, "audit_log.jsonl")
        self.pointers_path = os.path.join(base_dir, "pointers.jsonl")
        os.makedirs(base_dir, exist_ok=True)

    def log_audit(self, agent, event, metadata=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "event": event,
            "metadata": metadata or {}
        }
        with open(self.audit_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"[*] [CPOS Audit] {agent}: {event}")

    def record_pointer(self, context_type, location, summary, metadata=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": context_type,
            "location": location,
            "summary": summary,
            "metadata": metadata or {}
        }
        with open(self.pointers_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"[*] [CPOS Pointer] Recorded {context_type} at {location}")
