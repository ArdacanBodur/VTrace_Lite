# Version 1.7 (Modular - COPILOT) 07.05 12:00 (Compatible with 1.8, 1.8.1, 1.9)

import psutil
from logger_config import logger

# Predefined resource alert thresholds
ALERT_THRESHOLDS = {
    "cpu_percent": 90,  # CPU usage percentage
    "ram_percent": 90,  # RAM usage percentage
    "disk_read_bytes": 50 * 1024 * 1024,  # 50 MB/s
    "disk_write_bytes": 50 * 1024 * 1024,  # 50 MB/s
    "network_sent_bytes": 10 * 1024 * 1024,  # 10 MB/s
    "network_recv_bytes": 10 * 1024 * 1024,  # 10 MB/s
}

def get_host_resource_usage():
    
    # Fetches the CPU, RAM, Disk I/O, and Network usage of the host machine.

    # Returns:
        # dict: A dictionary containing resource usage metrics.
    
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk_io = psutil.disk_io_counters()
        net_io = psutil.net_io_counters()

        usage = {
            "cpu_percent": cpu_percent,
            "ram_percent": ram.percent,
            "ram_total_MB": ram.total // (1024**2),
            "ram_used_MB": ram.used // (1024**2),
            "disk_read_bytes": disk_io.read_bytes,
            "disk_write_bytes": disk_io.write_bytes,
            "network_sent_bytes": net_io.bytes_sent,
            "network_recv_bytes": net_io.bytes_recv,
        }

        # Check for resource alerts
        check_resource_alerts(usage, "Host")

        return usage
    except Exception as e:
        logger.error(f"Error fetching host resource usage: {e}")
        return {}

def get_vm_resource_usage(vmx_path):
    
    # Estimates the CPU, RAM, Disk I/O, and Network usage of a virtual machine based on its running processes.

    # Args:
        # vmx_path (str): The path to the .vmx file of the virtual machine.

    # Returns:
        # dict or None: A dictionary containing resource usage metrics, or None if no matching process is found.
    
    vm_process_names = ["vmware-vmx.exe"]
    total_cpu_percent = 0.0
    total_ram_used_MB = 0
    total_disk_read_bytes = 0
    total_disk_write_bytes = 0
    total_network_sent_bytes = 0
    total_network_recv_bytes = 0
    matched_processes = 0

    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info', 'io_counters', 'num_threads']):
            try:
                if proc.info['name'] in vm_process_names:
                    cmdline = ' '.join(proc.info['cmdline']).lower()
                    if vmx_path.lower().replace('\\', '/') in cmdline.replace('\\', '/'):
                        matched_processes += 1
                        total_cpu_percent += proc.cpu_percent(interval=1)
                        total_ram_used_MB += proc.memory_info().rss // (1024 ** 2)

                        # Disk I/O
                        if proc.io_counters():
                            total_disk_read_bytes += proc.io_counters().read_bytes
                            total_disk_write_bytes += proc.io_counters().write_bytes

                        # Network I/O (Optional: Requires more advanced setup)
                        # Network usage would typically require additional tools or integration with VMware APIs.

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        if matched_processes > 0:
            usage = {
                "cpu_percent": total_cpu_percent,
                "ram_used_MB": total_ram_used_MB,
                "disk_read_bytes": total_disk_read_bytes,
                "disk_write_bytes": total_disk_write_bytes,
                "network_sent_bytes": total_network_sent_bytes,
                "network_recv_bytes": total_network_recv_bytes,
            }

            # Check for resource alerts
            check_resource_alerts(usage, vmx_path)

            return usage
        else:
            logger.warning(f"No running processes found for VM: {vmx_path}")
            return None
    except Exception as e:
        logger.error(f"Error fetching VM resource usage for {vmx_path}: {e}")
        return None

def check_resource_alerts(usage, resource_name):
    
    # Checks resource usage against predefined thresholds and logs an alert if exceeded.

    # Args:
        # usage (dict): A dictionary of resource usage metrics.
        # resource_name (str): The name of the resource (e.g., "Host" or VM path).
    
    for metric, value in usage.items():
        if metric in ALERT_THRESHOLDS and value > ALERT_THRESHOLDS[metric]:
            logger.warning(f"⚠️ ALERT: {metric} usage for {resource_name} exceeded threshold! Current: {value}, Threshold: {ALERT_THRESHOLDS[metric]}")