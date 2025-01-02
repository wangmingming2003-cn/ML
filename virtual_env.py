import os
import subprocess
import shutil

# Prompt the user for the Python version
python_version = input("Enter the Python version you want to use (e.g., 3.8, 3.9): ")

# Check if the specified Python version is installed using pyenv
version_check = subprocess.run(["pyenv", "versions", "--bare"], capture_output=True, text=True)
installed_versions = version_check.stdout.splitlines()

if python_version not in installed_versions:
    print(f"Python {python_version} is not installed. Installing...")
    install_result = subprocess.run(["pyenv", "install", python_version])
    if install_result.returncode != 0:
        print(f"Failed to install Python {python_version}. Proceeding without additional python installation.")
else:
    print(f"Python {python_version} is already installed.")

# Define the name of the virtual environment directory
env_name = "venv"

# Check if the virtual environment already exists
if os.path.exists(env_name):
    action = input(f"Virtual environment '{env_name}' already exists. Do you want to replace it or create a new one? (replace/new): ")
    if action.lower() == 'replace':
        shutil.rmtree(env_name)
        print(f"Existing virtual environment '{env_name}' has been removed.")
    elif action.lower() == 'new':
        env_name = input("Enter a new name for the virtual environment: ")
    else:
        print("Invalid option. Exiting.")
        exit(1)

# Create the virtual environment using the specified Python version
venv_creation = subprocess.run([f"python{python_version}", "-m", "venv", env_name])
if venv_creation.returncode != 0:
    print(f"Failed to create virtual environment '{env_name}'. Exiting.")
    exit(1)

print(f"Virtual environment '{env_name}' has been created successfully.")

# Install the packages from requirements.txt
requirements_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'requirements.txt'))
subprocess.run([os.path.join(env_name, 'bin', 'pip'), 'install', '-r', requirements_path])
print("Packages from requirements.txt have been installed.")

# Check if ipykernel is installed
ipykernel_check = subprocess.run([os.path.join(env_name, 'bin', 'pip'), 'show', 'ipykernel'], capture_output=True, text=True)
if 'Name: ipykernel' not in ipykernel_check.stdout:
    # Install ipykernel for Jupyter support
    subprocess.run([os.path.join(env_name, 'bin', 'pip'), 'install', 'ipykernel'])
    subprocess.run([os.path.join(env_name, 'bin', 'python'), '-m', 'ipykernel', 'install', '--user', '--name', env_name])
    print("ipykernel has been installed and registered.")
else:
    print("ipykernel is already installed.")

# Create the 'workspace' directory inside the virtual environment directory
workspace_dir = os.path.join(env_name, "workspace")
os.makedirs(workspace_dir, exist_ok=True)

# Set the 'workspace' directory as the current working directory
os.chdir(workspace_dir)
print(f"Changed working directory to '{workspace_dir}'.")