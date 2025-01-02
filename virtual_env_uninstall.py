import os
import shutil

# List directories in the current directory
envs = [d for d in os.listdir('.') if os.path.isdir(d)]

def remove_pycache_dirs(env_path):
    for root, dirs, files in os.walk(env_path):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                pycache_path = os.path.join(root, dir_name)
                shutil.rmtree(pycache_path)
                print(f"Deleted: {pycache_path}")

if not envs:
    print("No virtual environments found.")
    exit(1)

# Display available environments
print("Available virtual environments:")
for i, env in enumerate(envs, start=1):
    print(f"{i}. {env}")

# Prompt the user to select an environment to delete
choice = input("Enter the number of the virtual environment you want to delete: ")

try:
    env_index = int(choice) - 1
    if 0 <= env_index < len(envs):
        env_name = envs[env_index]
        confirmation = input(f"Are you sure you want to delete the virtual environment '{env_name}'? (yes/no): ")
        if confirmation.lower() == 'yes':
            # Remove __pycache__ directories
            remove_pycache_dirs(env_name)
            
            # Remove the virtual environment directory
            if os.path.exists(env_name):
                shutil.rmtree(env_name)
                print(f"Virtual environment '{env_name}' has been deleted.")
            else:
                print(f"Virtual environment '{env_name}' does not exist.")
        else:
            print("Operation cancelled.")
    else:
        print("Invalid selection.")
except ValueError:
    print("Invalid input. Please enter a number.")