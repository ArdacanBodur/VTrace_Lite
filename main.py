# Version 1.9 (Modular - COPILOT - CHECKPOINT) 07.05 21:00

from vm_finder import find_vmx_files
from vm_status import get_vm_status
from vm_manager import (
    start_vm, stop_vm, suspend_vm, resume_vm,
    create_snapshot, revert_to_snapshot, delete_snapshot, clone_vm
)
from vm_scheduler import schedule_vm_operation, list_scheduled_tasks, cancel_scheduled_task, run_scheduled_tasks
from logger_config import logger
from vm_monitor import get_host_resource_usage, get_vm_resource_usage
from resource_logger import log_resource_usage
from auth import authenticate_user, set_password
import threading
import os
import time


def list_virtual_machines():
    logger.info("Starting to list virtual machines.")
    vmx_files = find_vmx_files()
    if not vmx_files:
        logger.info("No virtual machines found.")
        print("\n⚠️ No virtual machines found.")
        return []

    print("\n🔍 Virtual Machines:")
    for idx, vmx in enumerate(vmx_files, start=1):
        try:
            vm_name = vmx.split("\\")[-2]
            status = get_vm_status(vmx)
            size_bytes = sum(
                os.path.getsize(os.path.join(root, file))
                for root, _, files in os.walk(os.path.dirname(vmx))
                for file in files
            )
            size_gb = size_bytes / (1024 ** 3)
            logger.debug(f"VM Details: Name={vm_name}, Status={status}, Size={size_gb:.2f} GB")
            print(f"{idx}. {vm_name} | Status: {status} | Size: {size_gb:.2f} GB")
        except Exception as e:
            logger.error(f"Error processing VM {vmx}: {e}")
    logger.info("Completed listing virtual machines.")
    return vmx_files


def snapshot_and_clone_menu():
    logger.info("Entering Snapshot and Clone Menu.")
    vmx_files = list_virtual_machines()
    if not vmx_files:
        return

    try:
        choice = int(input("\nSelect a VM to manage (number): ")) - 1
        if choice < 0 or choice >= len(vmx_files):
            logger.warning("User made an invalid selection in Snapshot and Clone Menu.")
            print("❗ Invalid selection.")
            return
        vmx = vmx_files[choice]

        print("\n📸 Snapshot and Clone Menu")
        print("1. Create Snapshot")
        print("2. Revert to Snapshot")
        print("3. Delete Snapshot")
        print("4. Clone VM")
        action = input("Select an action: ")

        if action == '1':
            snapshot_name = input("Enter snapshot name: ")
            create_snapshot(vmx, snapshot_name)
            logger.info(f"Snapshot '{snapshot_name}' created for VM: {vmx}")
            print(f"✅ Snapshot '{snapshot_name}' created successfully.")
        elif action == '2':
            snapshot_name = input("Enter snapshot name to revert: ")
            revert_to_snapshot(vmx, snapshot_name)
            logger.info(f"Reverted to snapshot '{snapshot_name}' for VM: {vmx}")
            print(f"✅ Reverted to snapshot '{snapshot_name}' successfully.")
        elif action == '3':
            snapshot_name = input("Enter snapshot name to delete: ")
            delete_snapshot(vmx, snapshot_name)
            logger.info(f"Snapshot '{snapshot_name}' deleted for VM: {vmx}")
            print(f"✅ Snapshot '{snapshot_name}' deleted successfully.")
        elif action == '4':
            destination_folder = input("Enter destination folder for the cloned VM: ")
            new_vm_name = input("Enter a name for the cloned VM: ")
            clone_vm(vmx, destination_folder, new_vm_name)
            logger.info(f"VM cloned successfully from '{vmx}' to '{destination_folder}' with name '{new_vm_name}'.")
            print(f"✅ VM cloned successfully to '{destination_folder}' with name '{new_vm_name}'.")
        else:
            logger.warning("User selected an invalid action in Snapshot and Clone Menu.")
            print("❗ Invalid action.")
    except ValueError as e:
        logger.error(f"Invalid input in Snapshot and Clone Menu: {e}")
        print("❗ Invalid input.")
    except Exception as e:
        logger.error(f"Unexpected error in Snapshot and Clone Menu: {e}")
    logger.info("Exiting Snapshot and Clone Menu.")


def show_resource_menu():
    logger.info("Entering Resource Usage Menu.")
    print("\n📊 Resource Usage Menu")
    print("1. Host Resources")
    print("2. Virtual Machine Resources")
    choice = input("Your choice: ")

    if choice == '1':
        usage = get_host_resource_usage()
        log_resource_usage("Host", usage)
        print("\n💻 Host Resource Usage:")
        for metric, value in usage.items():
            print(f"{metric}: {value}")
    elif choice == '2':
        vmx_files = list_virtual_machines()
        if not vmx_files:
            return
        try:
            selection = int(input("\nSelect a VM to view resources (number): ")) - 1
            if 0 <= selection < len(vmx_files):
                vmx = vmx_files[selection]
                usage = get_vm_resource_usage(vmx)
                if usage:
                    log_resource_usage(vmx, usage)
                    print("\n🧠 Virtual Machine Resource Usage:")
                    for metric, value in usage.items():
                        print(f"{metric}: {value}")
                else:
                    print("⚠️ VM is not running or resource info is unavailable.")
            else:
                logger.warning("Invalid VM selection in Resource Usage Menu.")
                print("❗ Invalid selection.")
        except ValueError:
            logger.error("Invalid input in Resource Usage Menu.")
            print("❗ Invalid input.")
    else:
        logger.warning("Invalid choice in Resource Usage Menu.")
        print("❗ Invalid choice.")
    logger.info("Exiting Resource Usage Menu.")


def manage_vm_menu():
    logger.info("Entering VM Management Menu.")
    vmx_files = list_virtual_machines()
    if not vmx_files:
        return

    try:
        choice = int(input("\nSelect a VM to manage (number): ")) - 1
        if choice < 0 or choice >= len(vmx_files):
            logger.warning("User made an invalid selection in VM Management Menu.")
            print("❗ Invalid selection.")
            return
        vmx = vmx_files[choice]

        print("\n📦 VM Management Menu")
        print("1. Start")
        print("2. Stop")
        print("3. Suspend")
        print("4. Resume")
        operation = input("Select an operation: ")

        if operation == '1':
            start_vm(vmx)
            logger.info(f"VM started: {vmx}")
        elif operation == '2':
            stop_vm(vmx)
            logger.info(f"VM stopped: {vmx}")
        elif operation == '3':
            suspend_vm(vmx)
            logger.info(f"VM suspended: {vmx}")
        elif operation == '4':
            resume_vm(vmx)
            logger.info(f"VM resumed: {vmx}")
        else:
            logger.warning("User selected an invalid operation in VM Management Menu.")
            print("❗ Invalid operation.")
    except ValueError:
        logger.error("Invalid input in VM Management Menu.")
        print("❗ Invalid input.")
    except Exception as e:
        logger.error(f"Unexpected error in VM Management Menu: {e}")
    logger.info("Exiting VM Management Menu.")


def schedule_menu():
    logger.info("Entering Schedule VM Operation Menu.")
    vmx_files = list_virtual_machines()
    if not vmx_files:
        logger.info("No virtual machines found.")
        return

    print("\n📅 Schedule VM Operation")
    print("Available VMs:")
    for idx, vmx in enumerate(vmx_files, start=1):
        print(f"{idx}. {vmx}")

    try:
        vm_choice = int(input("Select a VM (number): ")) - 1
        if vm_choice < 0 or vm_choice >= len(vmx_files):
            logger.warning("User made an invalid VM selection in Schedule Menu.")
            print("❗ Invalid selection.")
            return

        vmx_path = vmx_files[vm_choice]
        print("\nAvailable operations:")
        print("1. Start")
        print("2. Stop")
        print("3. Suspend")
        print("4. Resume")

        operation_choice = input("Select an operation: ")
        operations_map = {
            "1": "start",
            "2": "stop",
            "3": "suspend",
            "4": "resume"
        }
        operation = operations_map.get(operation_choice)
        if not operation:
            logger.warning("User selected an invalid operation in Schedule Menu.")
            print("❗ Invalid operation.")
            return

        schedule_time = input("Enter the time to perform the operation (HH:MM, 24-hour format): ")
        schedule_vm_operation(operation, vmx_path, schedule_time)
        logger.info(f"Scheduled operation '{operation}' for VM: {vmx_path} at {schedule_time}")
    except ValueError:
        logger.error("Invalid input in Schedule Menu.")
        print("❗ Invalid input.")
    except Exception as e:
        logger.error(f"Unexpected error in Schedule Menu: {e}")
    logger.info("Exiting Schedule VM Operation Menu.")


def cancel_scheduled_task_menu():
    logger.info("Entering Cancel Scheduled Task Menu.")
    tasks = list_scheduled_tasks()
    if not tasks:
        logger.info("No scheduled tasks found.")
        print("\n⚠️ No scheduled tasks found.")
        return

    print("\n📅 Scheduled Tasks:")
    for idx, (task_name, details) in enumerate(tasks.items(), start=1):
        print(f"{idx}. {task_name} - {details['operation']} for {details['vmx_path']} at {details['time']}")

    try:
        choice = int(input("\nSelect a task to cancel (number): ")) - 1
        if 0 <= choice < len(tasks):
            task_name = list(tasks.keys())[choice]
            cancel_scheduled_task(task_name)
            logger.info(f"Cancelled scheduled task: {task_name}")
            print(f"✅ Task '{task_name}' has been canceled.")
        else:
            logger.warning("User made an invalid selection in Cancel Scheduled Task Menu.")
            print("❗ Invalid selection.")
    except ValueError:
        logger.error("Invalid input in Cancel Scheduled Task Menu.")
        print("❗ Invalid input.")
    logger.info("Exiting Cancel Scheduled Task Menu.")


def main_menu():
    logger.info("Starting main menu.")
    scheduler_thread = threading.Thread(target=run_scheduled_tasks, daemon=True)
    scheduler_thread.start()

    time.sleep(1)

    while True:
        print("\n🎛️ Main Menu")
        print("1. List Virtual Machines")
        print("2. Show Resource Usage")
        print("3. Manage VM")
        print("4. Schedule VM Operation")
        print("5. List Scheduled Tasks")
        print("6. Cancel Scheduled Task")
        print("7. Manage Snapshots and Cloning")
        print("8. Set New Password")
        print("9. Exit")

        try:
            choice = input("Your choice: ")
            logger.debug(f"User selected option {choice} in Main Menu.")
            if choice == '1':
                list_virtual_machines()
            elif choice == '2':
                show_resource_menu()
            elif choice == '3':
                manage_vm_menu()
            elif choice == '4':
                schedule_menu()
            elif choice == '5':
                scheduled_tasks = list_scheduled_tasks()
                for task_name, details in scheduled_tasks.items():
                    print(f"{task_name}: {details}")
            elif choice == '6':
                cancel_scheduled_task_menu()
            elif choice == '7':
                snapshot_and_clone_menu()
            elif choice == '8':
                set_password()
            elif choice == '9':
                logger.info("User exited the application.")
                print("👋 Exiting...")
                break
            else:
                logger.warning(f"Invalid input in Main Menu: {choice}")
                print("❗ Invalid input.")
        except Exception as e:
            logger.error(f"Unexpected error in Main Menu: {e}")
    logger.info("Exiting main menu.")


if __name__ == "__main__":
    logger.info("🔒 Starting the Secure VM Management Tool.")
    print("🔒 Welcome to the Secure VM Management Tool!")
    if authenticate_user():
        main_menu()
    else:
        logger.error("Authentication failed. Exiting the program.")