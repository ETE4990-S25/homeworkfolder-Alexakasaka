import docker

# Connect to the local Docker daemon
client = docker.from_env()

# Name of the container to monitor
container_name = "nginx"

try:
    # Try to acsess the container
    container = client.containers.get(container_name)

    # Check if the container is running
    is_running = container.status == "running"

#added a failsafe (autofilled by copilot)
    if not is_running:
        print(f"Container '{container_name}' is not running. Restarting...")
        container.restart()
        container.reload()
        was_restarted = True
    else:
        was_restarted = False

    # Get network info
    network_info = container.attrs.get("NetworkSettings", {}).get("Networks", {})
    has_network = bool(network_info)

    # Print container status
    print(f"Container name: {container_name}")
    print(f"Is running: {container.status == 'running'}")
    print(f"Was restarted: {was_restarted}")
    print(f"Has network: {has_network}")

    for network_name, settings in network_info.items():
        ip_address = settings.get("IPAddress")
        print(f"Network: {network_name}, IP Address: {ip_address}")

except docker.errors.NotFound:
    print(f"Container '{container_name}' not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

