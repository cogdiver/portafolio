# GCP QuickStart Templates

GCP QuickStart Templates is a comprehensive collection of project initialization templates designed to streamline the creation of Google Cloud Platform applications. Each template within the repository follows standard architectural practices and is tailored for specific use-cases. The templates provide a consistent structure and set of best practices to ensure a smooth and efficient development process, enabling developers to quickly start and deploy scalable, robust, and maintainable GCP services.


---

## Getting Started

This section describes how to use the provided script to build a Docker image and run a container for initiating a template creation with Cookiecutter.

### Prerequisites

- Docker must be installed on your system.
- Ensure that the `Dockerfile` and the `requirements.txt` file are present in the current directory.

### Script Execution

The script `start_template.sh` automates the creation of a Docker image and the execution of a container that will run Cookiecutter on the current directory.

Here's what the script does:
1. **Builds a Docker image** based on the provided `Dockerfile`, which specifies a Python environment and the command to run Cookiecutter.
2. **Runs a container** based on the built image, attaching the terminal for user interaction with Cookiecutter.

To execute the script, follow these steps:

```bash
# Make the script executable (if it's not already)
chmod +x scripts/start_template.sh

# Run the script
./scripts/start_template.sh
```

The script will build the Docker image and start the container, allowing you to interact with Cookiecutter to create your template. Follow the on-screen prompts to complete the template creation. Once completed, you can see the new project created in the current folder.

----


## Developing a New Template

This section guides you through the process of developing a new template in the repository using `create_new_template.sh` script and Docker Compose. Docker Compose automates the setup of the environment, making it easy to test and execute the new template.

**1. Create the Template Structure:** To start developing a new template, you can execute the `create_new_template.sh` script. This script will guide you through the process of defining the directory structure for the template and will create the required files and folders.

```bash
# Execute the script
./create_new_template.sh
```

**2. Build and Start the Docker Container:** Once you have created the template structure, you can build and start the Docker container to work with the templates.

```bash
# Build the Docker image and start the container
docker-compose up templates -d
```

**3. Connect to the Running Container:** After starting the container, you can connect to it to interact with the dependencies and the template files.

```bash
# Connect to the running container
docker exec -it dev_env_templates bash
```

**4. Work on the Template:** Inside the container, navigate to the directory of the new template and use the `cookiecutter` command to perform tests and execute the new template.

```bash
# Change to the template directory
cd /service/path/to/your/template

# Run Cookiecutter for the template
cookiecutter .
```

Follow the on-screen prompts to customize and generate the template. Any changes to the files in the `/service` directory inside the container will be synchronized with the host, enabling real-time development and testing.


---

## Cleaning Up the Environment

After developing and testing your template, you may wish to clean up the Docker environment to remove all containers, networks, volumes, and images associated with the project. This helps to reset the state and free up resources on your system.

Follow these steps to clean up the environment:

```bash
# Run the Cleanup Script
./scripts/cleanup.sh
```

>Be cautious when running these commands, as they will remove specific resources related to this project. Make sure you understand what will be removed before executing them.
