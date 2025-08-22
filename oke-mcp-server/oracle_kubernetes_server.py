from mcp.server.fastmcp import FastMCP

import subprocess

mcp = FastMCP("OKE Diagnostic Server")

def run_command(cmd: list) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

# ----------------------- MCP Tools -----------------------

@mcp.tool()
def get_nodes() -> str:
    """
    Returns a list of all Kubernetes nodes in JSON format.
    """
    return run_command(["kubectl", "get", "nodes", "-o", "json"])

@mcp.tool()
def get_all_pods() -> str:
    """
    Returns a list of all pods across all namespaces.
    """
    return run_command(["kubectl", "get", "pods", "--all-namespaces", "-o", "json"])

@mcp.tool()
def get_all_services() -> str:
    """
    Returns a list of all services across all namespaces.
    """
    return run_command(["kubectl", "get", "svc", "--all-namespaces", "-o", "json"])

@mcp.tool()
def describe_nodes() -> str:
    """
    Describes all nodes in the cluster.
    """
    return run_command(["kubectl", "describe", "nodes"])

@mcp.tool()
def describe_pods() -> str:
    """
    Describes all pods in the cluster.
    """
    return run_command(["kubectl", "describe", "pods", "--all-namespaces"])

@mcp.tool()
def kubectl_rollout(deployment: str, namespace: str = "default") -> str:
    """
    Gets rollout status for a deployment.
    
    Args:
        deployment: The name of the deployment.
        namespace: The namespace (default is 'default').
    """
    return run_command(["kubectl", "rollout", "status", f"deployment/{deployment}", "-n", namespace])

@mcp.tool()
def kubectl_context() -> str:
    """
    Returns the current Kubernetes context.
    """
    return run_command(["kubectl", "config", "current-context"])

@mcp.tool()
def explain_resource(resource: str) -> str:
    """
    Explains a Kubernetes resource.

    Args:
        resource: The name of the resource (e.g., pod, deployment).
    """
    return run_command(["kubectl", "explain", resource])

@mcp.tool()
def install_helm_chart(release: str, chart: str, namespace: str = "default") -> str:
    """
    Installs a Helm chart.

    Args:
        release: Name of the release.
        chart: Helm chart (e.g., bitnami/nginx).
        namespace: Kubernetes namespace (default is 'default').
    """
    return run_command(["helm", "install", release, chart, "-n", namespace])

@mcp.tool()
def upgrade_helm_chart(release: str, chart: str, namespace: str = "default") -> str:
    """
    Upgrades a Helm chart.

    Args:
        release: Release name.
        chart: Updated chart version.
        namespace: Namespace of the release.
    """
    return run_command(["helm", "upgrade", release, chart, "-n", namespace])

@mcp.tool()
def uninstall_helm_chart(release: str, namespace: str = "default") -> str:
    """
    Uninstalls a Helm release.

    Args:
        release: Release name.
        namespace: Namespace the release is deployed in.
    """
    return run_command(["helm", "uninstall", release, "-n", namespace])

@mcp.tool()
def port_forward(pod: str, local_port: int, remote_port: int, namespace: str = "default") -> str:
    """
    Port-forwards from a local port to a pod port.

    Args:
        pod: Pod name.
        local_port: Local machine port.
        remote_port: Pod container port.
        namespace: Namespace where the pod exists.
    """
    return f"kubectl port-forward pod/{pod} {local_port}:{remote_port} -n {namespace}"

@mcp.tool()
def stop_port_forward() -> str:
    """
    Stops all ongoing port-forwarding sessions.
    """
    return run_command(["pkill", "-f", "kubectl port-forward"])

@mcp.tool()
def exec_in_pod(pod: str, command: str, namespace: str = "default") -> str:
    """
    Executes a shell command in a specified pod.

    Args:
        pod: Pod name.
        command: Shell command to run.
        namespace: Namespace where the pod exists.
    """
    return run_command(["kubectl", "exec", pod, "-n", namespace, "--", "sh", "-c", command])

@mcp.tool()
def list_api_resources() -> str:
    """
    Lists all API resources available in the cluster.
    """
    return run_command(["kubectl", "api-resources"])

@mcp.tool()
def kubectl_generic(args: str) -> str:
    """
    Executes a generic kubectl command from string input.

    Args:
        args: Argument string to pass to kubectl. Example: "get pods -n default"
    """
    return run_command(["kubectl"] + args.split())

@mcp.tool()
def ping() -> str:
    """
    Basic health check.
    """
    return "OKE MCP server is online"

@mcp.tool()
def get_node_metrics() -> str:
    """
    Returns CPU and memory usage of all nodes.
    Requires metrics-server to be installed.
    """
    return run_command(["kubectl", "top", "nodes"])

@mcp.tool()
def get_pod_metrics() -> str:
    """
    Returns CPU and memory usage of all pods.
    Requires metrics-server to be installed.
    """
    return run_command(["kubectl", "top", "pods", "--all-namespaces"])

@mcp.tool()
def get_events(namespace: str = "default") -> str:
    """
    Returns recent events from the specified namespace.
    
    Args:
        namespace: The Kubernetes namespace (default is 'default').
    """
    return run_command(["kubectl", "get", "events", "-n", namespace, "--sort-by=.lastTimestamp"])

@mcp.tool()
def restart_unhealthy_pod(pod_name: str, namespace: str = "default") -> str:
    """
    Checks if the specified pod is healthy (all containers ready).
    If not, deletes the pod to trigger a restart.

    Args:
        pod_name: Name of the pod to check.
        namespace: Namespace where the pod is running (default: "default").
    """
    try:
        # Get readiness status of all containers in the pod
        cmd = [
            "kubectl", "get", "pod", pod_name,
            "-n", namespace,
            "-o", "jsonpath={.status.containerStatuses[*].ready}"
        ]
        readiness_output = run_command(cmd)
        if "Error:" in readiness_output:
            return f"Failed to check readiness: {readiness_output}"

        # If any container is not ready, restart the pod
        ready_states = readiness_output.strip().split()
        if all(state == "true" for state in ready_states):
            return f"All containers in pod '{pod_name}' are healthy."

        # Restart pod (by deleting, Deployment will auto-recreate it)
        delete_cmd = ["kubectl", "delete", "pod", pod_name, "-n", namespace]
        delete_output = run_command(delete_cmd)
        return f"Pod '{pod_name}' was unhealthy and has been restarted.\n{delete_output}"

    except Exception as e:
        return f"Exception occurred: {str(e)}"
    
@mcp.tool()
def scale_deployment(
    deployment_name: str,
    replicas: int,
    namespace: str = "default"
) -> str:
    """
    Scales the given deployment to the desired number of replicas.

    Args:
        deployment_name: The name of the deployment.
        replicas: The number of desired replicas.
        namespace: The Kubernetes namespace (default is 'default').

    Example:
        scale_deployment("nginx", 5, "default")
    """
    if replicas < 0:
        return "Replica count must be 0 or greater."

    return run_command([
        "kubectl", "scale", f"deployment/{deployment_name}",
        f"--replicas={replicas}", "-n", namespace
    ])
    
@mcp.tool()
def update_deployments_from_config() -> str:
    """
    Updates deployments based on keyword-image mappings defined in the config.
    For each keyword, finds all matching deployments (in name), and if the image
    differs from the target image, updates and restarts them.

    You can update the 'deployment_config' dictionary below to add more mappings.
    """
    import json
  
    # Add your mappings here: "keyword": "target_image"
    deployment_config = {
        "nginx": "ams.ocir.io/oabcs1/vivesisi/nginx:latest",
        "redis": "redis:7.2.4",
        "api": "ams.ocir.io/oabcs1/vivesisi/api:2.1"
        # Add more here
    }

    try:
        deployments_json = run_command([
            "kubectl", "get", "deployments", "--all-namespaces", "-o", "json"
        ])
        deployments = json.loads(deployments_json)
        updated = []

        for item in deployments.get("items", []):
            name = item["metadata"]["name"]
            namespace = item["metadata"]["namespace"]
            containers = item["spec"]["template"]["spec"]["containers"]

            for keyword, target_image in deployment_config.items():
                if keyword.lower() not in name.lower():
                    continue

                for container in containers:
                    current_image = container["image"]

                    if current_image != target_image:
                        # Prepare patch
                        patch = {
                            "spec": {
                                "template": {
                                    "spec": {
                                        "containers": [{
                                            "name": container["name"],
                                            "image": target_image
                                        }]
                                    }
                                }
                            }
                        }

                        patch_cmd = [
                            "kubectl", "patch", "deployment", name,
                            "-n", namespace,
                            "--type=strategic",
                            "-p", json.dumps(patch)
                        ]
                        patch_result = run_command(patch_cmd)

                        # Restart deployment
                        restart_cmd = [
                            "kubectl", "rollout", "restart",
                            f"deployment/{name}", "-n", namespace
                        ]
                        restart_result = run_command(restart_cmd)

                        updated.append(
                            f"  {namespace}/{name} matched keyword '{keyword}':\n"
                            f"  Image updated from '{current_image}' to '{target_image}'\n"
                            f"  Patch: {patch_result}\n"
                            f"  Restart: {restart_result}"
                        )
                    else:
                        updated.append(f" {namespace}/{name} (matched '{keyword}'): Already using '{target_image}'")
                    break  # Only apply first matching keyword

        if not updated:
            return "No matching deployments found for any keyword."
        return "\n\n".join(updated)

    except Exception as e:
        return f"Error occurred: {str(e)}"

# ----------------------- Entry Point -----------------------

if __name__ == "__main__":
    mcp.run()
