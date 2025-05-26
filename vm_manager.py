# Version 1.6 (Modular - COPILOT - CHECKPOINT) 07.05 11:20 (Compatible with 1.6.1, 1.7, 1.8, 1.8.1, 1.9)

import subprocess
import os
import json
from logger_config import logger
import shutil

# Load configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, 'config.json')

try:
    with open(CONFIG_PATH) as config_file:
        CONFIG = json.load(config_file)
except FileNotFoundError:
    logger.critical(f"Config file not found at {CONFIG_PATH}. Please ensure it exists.")
    raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}. Please ensure it exists.")
except json.JSONDecodeError as e:
    logger.critical(f"Error parsing config.json: {e}")
    raise ValueError(f"Error parsing config.json: {e}")

VMRUN_PATH = CONFIG.get("VMRUN_PATH", "")

def run_vm_command(command, vmx_path, additional_args=""):
    
    # Executes a vmrun command for the specified virtual machine.

    # Args:
        # command (str): The vmrun command to execute (e.g., "start", "stop").
        # vmx_path (str): The path to the .vmx file of the virtual machine.
        # additional_args (str): Additional arguments to pass to the command.
    
    if not os.path.exists(VMRUN_PATH):
        logger.error(f"'vmrun' tool not found. Please check the path: {VMRUN_PATH}")
        return

    full_cmd = f'"{VMRUN_PATH}" {command} "{vmx_path}" {additional_args}'

    try:
        result = subprocess.run(full_cmd, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"Command succeeded: {command} for VM: {vmx_path}")
        logger.debug(f"Command Output: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {command} for VM: {vmx_path}. Error: {e.stderr.strip()}")
    except FileNotFoundError:
        logger.critical(f"'vmrun' tool not found. Please ensure VMware Workstation is installed.")
    except Exception as e:
        logger.error(f"Unexpected error occurred during '{command}': {e}")

# Snapshot Management
def create_snapshot(vmx_path, snapshot_name):
    run_vm_command("snapshot", vmx_path, snapshot_name)

def revert_to_snapshot(vmx_path, snapshot_name):
    run_vm_command("revertToSnapshot", vmx_path, snapshot_name)

def delete_snapshot(vmx_path, snapshot_name):
    run_vm_command("deleteSnapshot", vmx_path, snapshot_name)

# VM Cloning
def clone_vm(source_vmx_path, destination_folder, new_vm_name):
    
    # Clones a virtual machine.

    # Args:
        # source_vmx_path (str)   : The path to the source .vmx file of the virtual machine.
        # destination_folder (str): The folder where the cloned VM should be stored.
        # new_vm_name (str)       : The name for the cloned virtual machine.
    
    try:
        if not os.path.exists(source_vmx_path):
            logger.error(f"Source VMX file not found: {source_vmx_path}")
            return

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
            logger.info(f"Created destination folder: {destination_folder}")

        # Copy the VM files to the new location
        shutil.copytree(os.path.dirname(source_vmx_path), destination_folder)
        logger.info(f"Cloned VM files from {os.path.dirname(source_vmx_path)} to {destination_folder}")

        # Update the VMX file with the new VM name
        cloned_vmx_path = os.path.join(destination_folder, os.path.basename(source_vmx_path))
        with open(cloned_vmx_path, 'r') as vmx_file:
            vmx_data = vmx_file.readlines()

        new_vmx_data = []
        for line in vmx_data:
            if line.startswith('displayName'):
                new_vmx_data.append(f'displayName = "{new_vm_name}"\n')
            else:
                new_vmx_data.append(line)

        with open(cloned_vmx_path, 'w') as vmx_file:
            vmx_file.writelines(new_vmx_data)

        logger.info(f"Updated VMX file for cloned VM: {cloned_vmx_path}")
    except Exception as e:
        logger.error(f"Failed to clone VM: {e}")

# Individual VM Commands
def start_vm(vmx_path):
    run_vm_command("start", vmx_path)

def stop_vm(vmx_path):
    run_vm_command("stop", vmx_path)

def suspend_vm(vmx_path):
    run_vm_command("suspend", vmx_path)

def resume_vm(vmx_path):
    run_vm_command("reset", vmx_path)