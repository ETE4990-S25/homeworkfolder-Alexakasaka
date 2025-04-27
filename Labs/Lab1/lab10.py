import docker

# Set up the Docker client
client = docker.from_env()

container_name = "nginx"

try:
    container = client.containers.get(container_name)

    # Make sure the container is running
    if container.status != "running":
        print(f"Notice: {container_name} is not running. Restarting...")
        container.restart()
        container.reload()  # Update status after restart
        was_restarted = True
    else:
        was_restarted = False

    print(f"\nContainer: {container.name}")
    print(f"Status: {container.status}")
    print(f"Restarted during check: {was_restarted}")

    networks = container.attrs.get("NetworkSettings", {}).get("Networks", {})

    #added a failsafe (autofilled by copilot)
    if container.status != "running":
        print(f"Container '{container_name}' is not running. Restarting...")
        container.restart()
        container.reload()
        was_restarted = True
    else:
        was_restarted = False
    
    if networks:
        print("Connected networks:")
        for network_name, network_data in networks.items():
            ip_address = network_data.get("IPAddress", "Unavailable")
            print(f" - {network_name}: {ip_address}")
    else:
        print("No network connections found.")

except docker.errors.NotFound:
    print(f"Error: Couldn't find a container named '{container_name}'.")
except Exception as e:
    print(f"Unexpected error: {e}") 

