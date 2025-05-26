# Version 1.8 (Modular - COPILOT - CHECKPOINT) 07.05 12:30 (Compatible with 1.8.1, 1.9)

import os
from logger_config import logger
from encryption_utils import decrypt_config

# Decrypt configuration
try:
    CONFIG = decrypt_config()
except Exception as e:
    logger.critical(f"Failed to load configuration: {e}")
    raise

VMWARE_VM_DIRS = CONFIG.get("VMWARE_VM_DIRS", [])

def find_vmx_files(paths=VMWARE_VM_DIRS):
    
    # Searches for .vmx files in the specified directories.

    # Args:
        # paths (list): List of directories to search for .vmx files.

    # Returns:
        # list: List of .vmx file paths found.
    
    vmx_files = []
    for path in paths:
        if not os.path.exists(path):
            logger.warning(f"Specified directory not found: {path}")
            continue
        try:
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".vmx"):
                        vmx_files.append(os.path.join(root, file))
        except Exception as e:
            logger.error(f"An error occurred while searching in directory {path}: {e}")
    if not vmx_files:
        logger.info("No .vmx files found.")
    else:
        logger.info(f"Found {len(vmx_files)} .vmx files.")
    return vmx_files