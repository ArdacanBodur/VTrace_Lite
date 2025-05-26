# Version 1.7 (Modular - COPILOT - CHECKPOINT) 07.05 12:00 (Compatible with 1.8, 1.8.1, 1.9)

import csv
import os
from datetime import datetime

LOG_FILE = "web\\resource_usage.csv"

def log_resource_usage(resource_name, usage):
    
    # Logs resource usage data to a CSV file.

    # Args:
        # resource_name (str): The name of the resource (e.g., "Host" or VM path).
        # usage (dict): A dictionary of resource usage metrics.
    
    log_exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not log_exists:
            # Write header if file doesn't exist
            writer.writerow(["Timestamp", "Resource", *usage.keys()])
        writer.writerow([datetime.now().isoformat(), resource_name, *usage.values()])