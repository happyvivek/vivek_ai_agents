# 🤖 OKE Diagnostic Agent (CrewAI-Powered)

Welcome to **OKE Agent**, a modular AI-powered diagnostic framework built using [CrewAI](https://docs.crewai.com/). This project is designed to manage and troubleshoot Oracle Kubernetes Engine (OKE) clusters using multiple specialized agents that work together to identify, explain, and optionally fix issues.

---

## 🚀 Features

- ✅ **Diagnostic Agent** – Runs full cluster checks (`kubectl` pods, nodes, PVCs, events)
- 🔧 **Remediation Agent** – Simulates (or performs) safe remediations
- 📈 **Observability Agent** – Gathers `kubectl top`, metrics, and event patterns
- 🛡 **Security Audit Agent** – Flags risky RBACs, privileged pods, etc.
- 💸 **Cost Optimization Agent** – Finds idle/over-provisioned resources
- 📦 **Upgrade Planning Agent** – Simulates upgrade readiness with safety checks
- 📂 **Logs** – Outputs diagnostics to timestamped `.log` files in `diagnostic_logs/`

---

## 📁 Project Structure

```
oke_agent/
├── config/
│   ├── agents.yaml          # Agent definitions and personalities
│   └── tasks.yaml           # Task flow descriptions
├── diagnostic_logs/         # Auto-generated logs from kubectl
├── src/
│   └── oke_agent/
│       ├── crew.py          # Main CrewBase definition (agents + tasks)
│       ├── main.py          # Entry point for running the Crew
│       └── tools/
│           └── custom_tool.py  # All tools: kubectl, remediation, observability, etc.
```

---

## 🧠 Powered By CrewAI

CrewAI is a Python framework to build multi-agent systems that collaborate to complete goals. This project uses:

- `@CrewBase` – Marks the main orchestrator class
- `@agent` – Registers an agent using a config + tool
- `@task` – Defines what an agent should do
- `@crew` – Connects agents + tasks into a final pipeline

---

## ⚙️ Installation

### Prerequisites

- Python 3.10+
- `kubectl` installed and configured with a valid K8s cluster (OKE or otherwise)
- Optional: OCI CLI access for more integrations

### Setup

```bash
git clone https://github.com/happyvivek/vivek_ai_agents.git
cd vivek_ai_agents/oke_agent

# Set up virtualenv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install crewai pydantic
```

---

## 🧾 Configuration

All agent and task configurations live under `config/`:

### 🧑‍🚀 `agents.yaml`

Defines agent roles, goals, and which tool they use:
```yaml
diagnostic_agent:
  role: "Cluster Diagnostic Specialist"
  goal: "Run kubectl diagnostics on pods, PVCs, nodes..."
  model: gpt-4o-mini
```

### 🧠 `tasks.yaml`

Describes each task and links it to its agent:
```yaml
diagnostic_task:
  description: "Run diagnostics across pods/nodes"
  expected_output: "Log summary and initial report"
```

---

## 🧪 Running the Agent Crew

To run the entire diagnostic pipeline:

```bash
cd oke_agent
LOG_LEVEL=DEBUG crewai run --active
```

This runs all agents and tasks **sequentially** based on the config.

👉 Output reports (like pod status, node health) will be stored in:
```
diagnostic_logs/<timestamp>_diagnostic_report.log
```

---

## 🔬 Individual Tool Examples

Each tool class (in `custom_tool.py`) is:
- Based on `BaseTool`
- Has its own `args_schema` (via Pydantic)
- Implements `_run(...)` logic

Examples:
- `KubectlTool` – runs `kubectl get pods`, `nodes`, etc.
- `ObservabilityTool` – runs `kubectl top` and gathers events
- `RemediationTool` – prints a simulated fix (can be extended)

---

## 🧱 How the System Works (Simplified)

```
@CrewBase
class OkeDiagnosticAgent:
    @agent → diagnostic_agent
    @task  → diagnostic_task
    @crew  → combines them into a Crew
```

When `crewai run` executes:
- It finds all agents + tasks
- Matches tools from `tools/`
- Runs the full pipeline in order

---

## 🛠️ Extend the System

Want to add a new capability?

1. Create a tool in `custom_tool.py`:
   ```python
   class NewTool(BaseTool):
       name = "my_tool"
       args_schema = MyInput
       def _run(self, input): ...
   ```
2. Add agent + task to the YAML files
3. Register them in `crew.py` using `@agent` and `@task`

---

## 🧯 Error Handling

- All `_run()` methods are wrapped in `try/except`
- Failure messages return directly to the agent
- Invalid inputs or `kubectl` errors are printed clearly

---

## 🤝 Contributing

Feel free to:
- Add real remediation logic
- Extend the upgrade planner
- Integrate with Prometheus, Grafana, or OCI APIs

---

## 📜 License

MIT License (See `LICENSE` file)

---

## 📬 Author

Built with ❤️ by [Vivek Singh](https://github.com/happyvivek)
