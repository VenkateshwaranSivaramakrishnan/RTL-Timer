import os
import subprocess
import shutil
import sys

def main():
    # Check if yosys is available in PATH
    if shutil.which("yosys") is None:
        print("Error: 'yosys' is not found in your PATH.")
        print("Please source the OpenROAD environment script first:")
        print("source <OpenROAD-install-path>/env.sh")
        sys.exit(1)

    # Define the relative path to the target directory
    target_dir = "./register_oriented_processing/vlg2bog"

    # Check that the directory exists
    if not os.path.isdir(target_dir):
        print(f"Error: Directory '{target_dir}' does not exist.")
        sys.exit(1)

    # Change the current working directory
    os.chdir(target_dir)
    print(f"Changed directory to {os.getcwd()}")

    # Execute the Python script
    try:
        subprocess.run(["python3", "auto_run.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error: auto_run.py failed to execute successfully.")
        print(f"Exit code: {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
