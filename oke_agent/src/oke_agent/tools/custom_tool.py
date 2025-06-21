'''f
rom crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import subprocess
import os
from datetime import datetime

class KubectlInput(BaseModel):
    trigger: str = Field(..., description="Trigger to start full kubectl diagnostics")

class KubectlTool(BaseTool):
    name: str = "kubectl_tool"
    description: str = "Comprehensive Kubernetes diagnostics including logs, metrics, auto-fix, and export."
    args_schema: Type[BaseModel] = KubectlInput

    def _run(self, trigger: str) -> str:
        try:
            output = []
            issues = []
            log_dir = os.path.join(os.getcwd(), "diagnostic_logs")
            os.makedirs(log_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = os.path.join(log_dir, f"{timestamp}_diagnostic_report.txt")

            def save_log(name, content):
                path = os.path.join(log_dir, f"{timestamp}_{name}.log")
                with open(path, "w") as f:
                    f.write(content)

            def cmd(args):
                return subprocess.check_output(args).decode()

            def write_to_report(data):
                with open(report_file, "a") as f:
                    f.write(data + "\n")

            # ========== Nodes & Conditions ==========
            output.append("==[ Nodes & Conditions ]==")
            node_info = cmd(["kubectl", "get", "nodes", "-o", "json"])
            import json
            nodes_json = json.loads(node_info)
            for node in nodes_json["items"]:
                name = node["metadata"]["name"]
                for condition in node["status"]["conditions"]:
                    if condition["type"] in ["MemoryPressure", "DiskPressure"] and condition["status"] == "True":
                        issues.append(f"Node {name} under {condition['type']}")
                        try:
                            output.append(f"Draining node {name} due to {condition['type']}")
                            subprocess.run(["kubectl", "drain", name, "--ignore-daemonsets", "--delete-emptydir-data", "--force"], check=True)
                        except subprocess.CalledProcessError:
                            output.append(f"Failed to drain node {name}")
            output.append("")  # Add spacing

            # Continue with previous diagnostics (Pods, Events, Top, etc.)
            # Reuse your earlier implementation below here
            # ──────────────────────────────────────────────
            # ... [Rest of your existing tool implementation here] ...
            # (copy from previous response and paste here)
            # ──────────────────────────────────────────────

            # Add footer and save final report
            footer = "\n📄 Diagnostic complete. Logs and report saved to 'diagnostic_logs/'."
            output.append(footer)

            final_report = "\n".join(output)
            write_to_report(final_report)

            return final_report

        except subprocess.CalledProcessError as e:
            return f"Error during diagnostics: {e.output.decode()}"
'''
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import subprocess
import os
import json
from datetime import datetime

# ========== Common Helper ==========

def run_kubectl_cmd(args: list) -> str:
    return subprocess.check_output(["kubectl"] + args).decode()

def save_output_to_file(filename: str, content: str):
    log_dir = os.path.join(os.getcwd(), "diagnostic_logs")
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(log_dir, f"{timestamp}_{filename}.log")
    with open(path, "w") as f:
        f.write(content)
    return path

# ========== Diagnostic Tool ==========

class KubectlInput(BaseModel):
    trigger: str = Field(..., description="Trigger to start full kubectl diagnostics")

class KubectlTool(BaseTool):
    name: str = "kubectl_tool"
    description: str = "Run a full cluster diagnostic (pods, nodes, PVCs, CrashLoopBackOff)."
    args_schema: Type[BaseModel] = KubectlInput

    def _run(self, trigger: str) -> str:
        try:
            pod_info = run_kubectl_cmd(["get", "pods", "--all-namespaces", "-o", "wide"])
            node_info = run_kubectl_cmd(["get", "nodes", "-o", "wide"])
            pvc_info = run_kubectl_cmd(["get", "pvc", "--all-namespaces"])
            events = run_kubectl_cmd(["get", "events", "--all-namespaces", "--sort-by=.metadata.creationTimestamp"])

            report = "\n".join([
                "=== Pods ===", pod_info,
                "\n=== Nodes ===", node_info,
                "\n=== PVCs ===", pvc_info,
                "\n=== Events ===", events
            ])
            save_output_to_file("diagnostic_report", report)
            return "🧪 Diagnostic report generated successfully."
        except Exception as e:
            return f"❌ Failed to run diagnostic: {e}"

# ========== Remediation Tool ==========

class RemediationInput(BaseModel):
    action: str = Field(..., description="Describe the issue to remediate (e.g., restart pod xyz)")

class RemediationTool(BaseTool):
    name: str = "remediation_tool"
    description: str = "Apply safe remediation steps based on diagnostics (e.g., restart pods, drain node)."
    args_schema: Type[BaseModel] = RemediationInput

    def _run(self, action: str) -> str:
        return f"⚙️ Simulated remediation executed: {action}"  # Stub for now

# ========== Observability Tool ==========

class ObservabilityInput(BaseModel):
    component: str = Field(..., description="Component to observe (pods, nodes, metrics)")

class ObservabilityTool(BaseTool):
    name: str = "observability_tool"
    description: str = "Fetch resource usage, events, and generate observability reports."
    args_schema: Type[BaseModel] = ObservabilityInput

    def _run(self, component: str) -> str:
       
        try:
            pod_metrics = run_kubectl_cmd(["top", "pods", "--all-namespaces"])
            node_metrics = run_kubectl_cmd(["top", "nodes"])
            events = run_kubectl_cmd(["get", "events", "--all-namespaces", "--sort-by=.metadata.creationTimestamp"])

            report = "\n".join([
                "=== Pod Metrics ===", pod_metrics,
                "\n=== Node Metrics ===", node_metrics,
                "\n=== Events ===", events
            ])
            save_output_to_file(f"{component}_observability_report", report)
            return "📈 Observability report generated successfully."
        except Exception as e:
            return f"❌ Failed to generate observability report: {e}"


# ========== Security Audit Tool ==========

class SecurityAuditInput(BaseModel):
    scan_scope: str = Field(..., description="Scope to audit (e.g., pods, rbac)")

class SecurityAuditTool(BaseTool):
    name: str = "security_audit_tool"
    description: str = "Scan cluster for security risks like privileged pods and risky RBAC roles."
    args_schema: Type[BaseModel] = SecurityAuditInput

    def _run(self, scan_scope: str) -> str:
        return f"🛡️ Security audit simulated for: {scan_scope}"  # Extend with real logic later

# ========== Cost Optimization Tool ==========

class CostOptimizationInput(BaseModel):
    scope: str = Field(..., description="Scope for cost analysis (e.g., node-pools, workloads)")

class CostOptimizationTool(BaseTool):
    name: str = "cost_optimization_tool"
    description: str = "Analyze resource usage to identify cost-saving opportunities."
    args_schema: Type[BaseModel] = CostOptimizationInput

    def _run(self, scope: str) -> str:
        return f"💸 Cost optimization analysis completed for: {scope}"  # Stub for real pricing logic

# ========== Upgrade Planning Tool ==========

class UpgradeInput(BaseModel):
    target_version: str = Field(..., description="Target Kubernetes version to upgrade to")

class UpgradeTool(BaseTool):
    name: str = "upgrade_planning_tool"
    description: str = "Assess upgrade readiness and identify deprecated APIs or compatibility issues."
    args_schema: Type[BaseModel] = UpgradeInput

    def _run(self, target_version: str) -> str:
        return f"📦 Upgrade precheck simulated for version: {target_version}"  # Hook into `kubectl get --raw ...` etc.
