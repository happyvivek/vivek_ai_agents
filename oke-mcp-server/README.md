# OKE MCP Server

The **OKE MCP Server** is a **Python-based Model Context Protocol (MCP) server** for interacting with **Oracle Kubernetes Engine (OKE)** clusters.  
It exposes Kubernetes operations as MCP tools (starting with `describe_pods`) and integrates seamlessly with MCP-compatible clients such as Claude Desktop.

---

##Features

- MCP server implementation in **Python**
- Exposes Kubernetes operations as **MCP tools**
- Built-in support for **`describe_pods`**
- Easy integration with **MCP-compatible clients**
- Extensible to support more Kubernetes operations (services, logs, scaling, etc.)

---

##Tools & Technologies

This project is built using the following tools and technologies:

- **[Python 3.9+](https://www.python.org/)** → Core programming language for implementing the MCP server  
- **[uv](https://github.com/astral-sh/uv)** → Fast Python package and project manager, used to run and manage dependencies  
- **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)** → Standard protocol for connecting AI models/agents to external tools and data sources  
- **[Oracle Kubernetes Engine (OKE)](https://www.oracle.com/cloud/cloud-native/container-engine-kubernetes/)** → Managed Kubernetes service on Oracle Cloud, the target cluster environment  
- **[Kubernetes Python Client](https://github.com/kubernetes-client/python)** → Python client library for interacting with Kubernetes APIs  
- **[Claude Desktop](https://claude.ai/)** (or any MCP-compatible client) → Example MCP client for integration with this server  
- **[kubeconfig](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)** → Local configuration file for authenticating and connecting to your OKE cluster  

---

## Installation

Clone this repository:

```bash
git clone https://github.com/happyvivek/vivek_ai_agents.git
cd vivek_ai_agents/oke-mcp-server
##Configure

{
  "mcpServers": {
    "oke-mcp-server": {
      "autoApprove": [
        "describe_pods"
      ],
      "disabled": false,
      "timeout": 60,
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "/Users/vivesisi/Downloads/code/oke-mcp-server",
        "run",
        "oracle_kubernetes_server.py"
      ]
    }
  }
}


## MCP Tools Reference (@mcp.tools)

The OKE MCP Server exposes the following tools for interacting with the Kubernetes cluster:

| Tool Name             | Description                                         | Input Parameters                                              | Output                                        |
|-----------------------|-----------------------------------------------------|---------------------------------------------------------------|-----------------------------------------------|
| `describe_pods`       | Lists all pods in the specified Kubernetes namespace | `namespace` → Name of the namespace (e.g., "default")        | `pods` → List of pod objects with name, status, node, labels, and container info |
| `list_services`       | Lists all services in the specified namespace       | `namespace` → Name of the namespace                           | `services` → List of service objects with name, type, cluster IP, ports, and selectors |
| `get_logs`            | Fetches logs from a specific pod and container      | `namespace`, `pod_name`, `container_name` (optional)         | `logs` → Logs output as a string              |
| `scale_deployments`   | Scales a deployment to a desired number of replicas | `namespace`, `deployment_name`, `replicas`                   | `status` → Success/failure message           |
| `describe_nodes`      | Fetches detailed information about all nodes       | None                                                          | `nodes` → List of node objects with name, status, capacity, labels, and roles |
| `create_deployment`   | Creates a new deployment in the cluster             | `namespace`, `deployment_name`, `image`, `replicas`, `ports` | `status` → Success/failure message           |
| `delete_deployment`   | Deletes an existing deployment                       | `namespace`, `deployment_name`                                 | `status` → Success/failure message           |
| `update_deployment`   | Updates an existing deployment (image or replicas)  | `namespace`, `deployment_name`, `image` (optional), `replicas` (optional) | `status` → Success/failure message           |
| `list_namespaces`     | Lists all namespaces in the cluster                 | None                                                          | `namespaces` → List of namespace names       |
| `get_service_details` | Retrieves details of a specific service            | `namespace`, `service_name`                                    | `service` → Service object with type, cluster IP, ports, and selectors |
| `create_service`      | Creates a new service in the cluster               | `namespace`, `service_name`, `type`, `ports`, `selector`      | `status` → Success/failure message           |
| `delete_service`      | Deletes an existing service                          | `namespace`, `service_name`                                    | `status` → Success/failure message           |
| `update_service`      | Updates an existing service (ports, type, selector) | `namespace`, `service_name`, `type` (optional), `ports` (optional), `selector` (optional) | `status` → Success/failure message           |
| `get_deployment_details` | Retrieves details of a deployment                 | `namespace`, `deployment_name`                                  | `deployment` → Deployment object with replicas, image, pods, and status |

