import os
import platform
import subprocess
import sys  # Import the sys module

def install_dependencies():
    try:

        command_requirements = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        command_lint = [sys.executable, "-m", "pip", "install", "-r", "requirements-lint.txt"]

        subprocess.check_call(command_requirements)
        print("Dependencies from requirements.txt installed successfully.")

        subprocess.check_call(command_lint)
        print("Dependencies from requirements-lint.txt installed successfully.")

    except subprocess.CalledProcessError as e:
        print("Failed to install dependencies:", e)

if __name__ == "__main__":
    install_dependencies()

