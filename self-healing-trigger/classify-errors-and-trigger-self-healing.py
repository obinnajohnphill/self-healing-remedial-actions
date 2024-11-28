#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import subprocess

# OS-specific remedial action registry
OS_REMEDIAL_ACTIONS = {}

# Decorator to register OS-specific remedial actions
def register_os_action(os_name):
    def decorator(func):
        OS_REMEDIAL_ACTIONS[os_name] = func
        return func
    return decorator

# Function to check if a tool exists
def is_tool_available(tool_name):
    """Check if a tool is available in the environment."""
    return subprocess.call(["which", tool_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

# Android-specific actions
@register_os_action("Android")
def remedial_actions_android(system_name):
    print(f"Performing remedial actions for {system_name}...")
    try:
        if is_tool_available("adb"):
            print("Clearing app data...")
            result = subprocess.run(
                ["adb", "shell", "pm", "clear", "com.example.app"],
                check=True,
                capture_output=True,
                text=True
            )
            if "no devices/emulators found" in result.stderr:
                raise Exception("No devices/emulators connected.")
            print("Rebooting device...")
            subprocess.run(["adb", "reboot"], check=True)
        else:
            raise Exception("adb tool not available.")
    except Exception as e:
        print(f"Error performing {system_name} remedial actions: {e}")
        print("Simulated: adb shell pm clear com.example.app")
        print("Simulated: adb reboot")

# Linux-specific actions
@register_os_action("Linux")
def remedial_actions_linux(system_name):
    print(f"Performing remedial actions for {system_name}...")
    try:
        print("Applying system updates...")
        subprocess.run(["apt-get", "update", "-y"], check=True)
        subprocess.run(["apt-get", "upgrade", "-y"], check=True)

        print("Restarting SSH service...")
        if is_tool_available("service"):
            result = subprocess.run(
                ["service", "ssh", "restart"],
                check=True,
                capture_output=True,
                text=True
            )
            if "unrecognized service" in result.stderr:
                print("Simulated: SSH service restart (unrecognized service)")
        else:
            print("Simulated: service ssh restart")

        print("Performing disk clean-up...")
        subprocess.run(["rm", "-rf", "/var/tmp/*"], check=True)

        print(f"{system_name} remedial actions completed successfully.")
    except Exception as e:
        print(f"Error performing {system_name} remedial actions: {e}")

# Mac-specific actions
@register_os_action("Mac")
def remedial_actions_mac(system_name):
    print(f"Performing remedial actions for {system_name}...")
    try:
        print("Simulated: softwareupdate -i -a")
        if is_tool_available("apachectl"):
            print("Restarting services (example for Apache)...")
            subprocess.run(["sudo", "apachectl", "restart"], check=True)
        else:
            print("Simulated: apachectl restart")
        print("Performing disk clean-up...")
        subprocess.run(["rm", "-rf", "/tmp/*"], check=True)

        print(f"{system_name} remedial actions completed successfully.")
    except Exception as e:
        print(f"Error performing {system_name} remedial actions: {e}")

# Windows-specific actions
@register_os_action("Windows")
def remedial_actions_windows(system_name):
    print(f"Performing remedial actions for {system_name}...")
    try:
        if is_tool_available("powershell"):
            # System Update
            print("Applying updates...")
            subprocess.run(["powershell", "-Command", "Install-WindowsUpdate -AcceptAll"], check=True)

            # Service Restart
            print("Restarting IIS service...")
            subprocess.run(["powershell", "-Command", "Restart-Service -Name 'W3SVC'"], check=True)

            # Disk Cleanup
            print("Performing disk clean-up...")
            subprocess.run(["powershell", "-Command", "cleanmgr /sagerun:1"], check=True)
        else:
            raise Exception("PowerShell not available.")
    except Exception as e:
        print(f"Error performing {system_name} remedial actions: {e}")
        print("Simulated: Install-WindowsUpdate -AcceptAll")
        print("Simulated: Restart-Service -Name 'W3SVC'")
        print("Simulated: cleanmgr /sagerun:1")

# Fallback for unsupported systems
def remedial_actions_fallback(system_name):
    print(f"No specific remedial actions defined for {system_name}.")

# Main remedial actions handler
def perform_remedial_actions(system_name):
    action_handler = OS_REMEDIAL_ACTIONS.get(system_name, remedial_actions_fallback)
    action_handler(system_name)

# Load and process system logs
def process_logs():
    print("Starting the self-healing application...")

    # Define the preprocessed log directory
    preprocessed_dir = '/app/self-healing-trigger/dataset/system-logs/multiple-system-log-dataset/preprocessed-data'

    # Check if the directory exists
    if not os.path.exists(preprocessed_dir):
        print(f"Error: The directory {preprocessed_dir} does not exist.")
        exit(1)

    print(f"Preprocessed directory found: {preprocessed_dir}")

    # Create a dictionary to store dataframes for each system
    system_dfs = {}

    # Load the preprocessed log files and create separate dataframes for each system
    for filename in os.listdir(preprocessed_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(preprocessed_dir, filename)
            print(f"Loading file: {filepath}")
            try:
                df = pd.read_csv(filepath)
                system_name = os.path.splitext(filename)[0].replace("_preprocessed", "")
                system_dfs[system_name] = df
                print(f"Loaded data for system: {system_name}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")

    # Define thresholds
    error_threshold = 100
    warning_threshold = 500

    # Process each system
    for system_name, df in system_dfs.items():
        print(f"\nProcessing data for {system_name}...")
        try:
            num_errors = df['error'].sum()
            num_warnings = df['warning'].sum()

            print(f"Errors: {num_errors}, Warnings: {num_warnings}")
            if num_errors > error_threshold:
                print(f"Triggering self-healing for {system_name} due to high errors.")
                perform_remedial_actions(system_name)
            elif num_warnings > warning_threshold:
                print(f"Triggering self-healing for {system_name} due to high warnings.")
                perform_remedial_actions(system_name)
            else:
                print(f"No remedial actions required for {system_name}.")
        except Exception as e:
            print(f"Error processing data for {system_name}: {e}")

    print("Self-healing application completed successfully.")

# Main function
if __name__ == "__main__":
    process_logs()
