
#!/usr/bin/env python
import os
import sys
import warnings
from datetime import datetime
import traceback

# Extend sys.path to locate oke_agent package
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from oke_agent.crew import OkeDiagnosticAgent  # Now using pure Python crew

# Suppress irrelevant warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def get_inputs():
    return {
        "diagnostic_task": {
            "trigger": "Run full diagnostics now"
        },
        "remediation_task": {
            "action": "Restart CrashLoopBackOff pods"
        },
        "observability_task": {
            "component": "pods"
        },
        "security_audit_task": {
            "scan_scope": "pods"
        },
        "cost_optimization_task": {
            "scope": "node-pools"
        },
        "upgrade_readiness_task": {
            "target_version": "v1.28"
        }
    }

def run():
    print(f" Starting OKE Diagnostic Crew - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    inputs = get_inputs()

    try:
        result = OkeDiagnosticAgent().crew().kickoff(inputs=inputs)
        print("\n Final Output:\n")
        print(result.raw)
    except Exception as e:
        traceback.print_exc()
        print(f"\n Error occurred while executing the crew: {e}")

if __name__ == "__main__":
    run()
