import docker

# Set up Docker client connection
client = docker.from_env()

# Define the name of the container we're checking
container_name = "nginx"

try:
    # Attempt to get the container (used a generic name here but you can change it)
    # This assumes the container is named "nginx" for this lab
    container = client.containers.get(container_name)

    # Check the current status of the container
    status = container.status
    is_running = status == "running"
    needs_restart = not is_running

    # Restart the container if it's not running
    was_restarted = False
    was_restarted = container.restart() is None if needs_restart else False

    # Refresh container information
    container.reload()

    # Gather network information
    network_data = container.attrs.get("NetworkSettings", {})
    network_list = network_data.get("Networks", {})
    has_network = len(network_list) > 0

    # Print diagnostic information using flags
    print("Container name:", container_name)
    print("Is running:", is_running)
    print("Was restarted:", was_restarted)
    print("Has network:", has_network)

    for network_name in network_list:
        ip_address = network_list[network_name].get("IPAddress")
        print("Network:", network_name)
        print("IP Address:", ip_address)

#added try except to catch errors(autofilled by copilot)
except docker.errors.NotFound:
    print("Container not found:", container_name)
except Exception as error:
    print("Unexpected error:", str(error))

