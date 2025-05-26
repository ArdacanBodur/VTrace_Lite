# Version 1.5 (Modular - COPILOT - CHECKPOINT) 05.05 21:05 (Compatible with 1.5.1, 1.5.2, 1.5.3, 1.6, 1.6.1, 1.7, 1.8, 1.8.1, 1.9)

import subprocess
import os
import json
from logger_config import logger

# Load configuration
with open('config.json') as config_file:
    CONFIG = json.load(config_file)
VMRUN_PATH = CONFIG.get("VMRUN_PATH", "")

def get_vm_status(vmx_path):
    
    # Determines the status of a virtual machine by checking if it is running.

    # Args:
        # vmx_path (str): The path to the .vmx file of the virtual machine.

    # Returns:
        # str: "Powered On" if the VM is running, "Powered Off" otherwise, or an error message.

    try:
        # Check if vmrun exists
        if not os.path.exists(VMRUN_PATH):
            logger.error(f"'vmrun' aracı bulunamadı. Lütfen {VMRUN_PATH} yolunu kontrol edin.")
            return f"❌ Hata: 'vmrun' aracı bulunamadı."

        # Run the vmrun list command
        result = subprocess.run(
            f'"{VMRUN_PATH}" list', shell=True, capture_output=True, text=True
        )

        # Check if command execution was successful
        if result.returncode != 0:
            logger.error(f"'vmrun list' komutu çalıştırılamadı. Çıktı: {result.stderr.strip()}")
            return f"❌ Hata: 'vmrun list' komutu çalıştırılamadı."

        # Parse the output of the command
        running_vms = result.stdout.splitlines()[1:]  # İlk satır "Total running VMs"
        if vmx_path in running_vms:
            logger.info(f"VM '{vmx_path}' çalışıyor.")
            return "Powered On"
        else:
            logger.info(f"VM '{vmx_path}' kapalı.")
            return "Powered Off"
    except FileNotFoundError:
        logger.critical("'vmrun' aracı bulunamadı. Lütfen VMware Workstation'un yüklü olduğundan emin olun.")
        return "❌ Hata: 'vmrun' aracı bulunamadı."
    except Exception as e:
        logger.error(f"Beklenmeyen bir hata oluştu: {e}")
        return f"❌ Beklenmeyen Hata: {e}"