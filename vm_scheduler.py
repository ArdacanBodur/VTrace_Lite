# Version 1.8.1 (Modular - COPILOT - CHECKPOINT) 07.05 13:40 (Compatible with 1.9)

import schedule
import time
from datetime import datetime
from logger_config import logger
from vm_manager import start_vm, stop_vm, suspend_vm, resume_vm

# Global dictionary to store scheduled tasks
scheduled_tasks = {}

def schedule_vm_operation(operation, vmx_path, schedule_time):
    
    # Schedules a power operation for a virtual machine.

    # Args:
        # operation (str): The operation to perform (start, stop, suspend, resume).
        # vmx_path (str): The path to the .vmx file of the virtual machine.
        # schedule_time (str): The time to perform the operation (HH:MM, 24-hour format).
    
    def perform_operation():
        logger.info(f"Executing scheduled operation '{operation}' for VM: {vmx_path}")
        if operation == "start":
            start_vm(vmx_path)
        elif operation == "stop":
            stop_vm(vmx_path)
        elif operation == "suspend":
            suspend_vm(vmx_path)
        elif operation == "resume":
            resume_vm(vmx_path)
        else:
            logger.error(f"Invalid operation: {operation}")

        # Automatically delete the task after execution
        task_name = f"{operation}_{vmx_path}_{schedule_time}"
        if task_name in scheduled_tasks:
            del scheduled_tasks[task_name]
            logger.info(f"Task '{task_name}' has been completed and removed.")

    try:
        schedule_time_obj = datetime.strptime(schedule_time, "%H:%M").time()
        task_name = f"{operation}_{vmx_path}_{schedule_time}"

        # Schedule the operation
        schedule.every().day.at(schedule_time).do(perform_operation)
        scheduled_tasks[task_name] = {
            "operation": operation,
            "vmx_path": vmx_path,
            "time": schedule_time
        }

        logger.info(f"Scheduled '{operation}' operation for VM: {vmx_path} at {schedule_time}")
    except ValueError:
        logger.error(f"Invalid time format: {schedule_time}. Please use HH:MM format (24-hour).")

def list_scheduled_tasks():
    
    # Lists all scheduled tasks.

    # Returns:
        # dict: A dictionary of scheduled tasks.
    
    return scheduled_tasks

def cancel_scheduled_task(task_name):
    
    # Cancels a specific scheduled task.

    # Args:
        # task_name (str): The name of the task to cancel.
    
    if task_name in scheduled_tasks:
        del scheduled_tasks[task_name]
        logger.info(f"Cancelled scheduled task: {task_name}")
    else:
        logger.warning(f"Task not found: {task_name}")

def run_scheduled_tasks():
    
    # Runs the scheduler loop to execute tasks at their scheduled times.
    
    logger.info("Starting the scheduler...")
    while True:
        schedule.run_pending()
        time.sleep(1)