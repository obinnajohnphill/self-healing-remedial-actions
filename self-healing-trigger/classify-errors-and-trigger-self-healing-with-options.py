import pandas as pd
import os
import subprocess
from flask import Flask
from prometheus_client import Counter, generate_latest, REGISTRY, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Initialize Flask App for Prometheus Metrics
app = Flask(__name__)

# Define Prometheus Metrics
ERRORS_DETECTED = Counter("errors_detected", "Number of errors detected", ["system"])
WARNINGS_DETECTED = Counter("warnings_detected", "Number of warnings detected", ["system"])
REMEDIAL_ACTIONS_TRIGGERED = Counter("remedial_actions_triggered", "Number of remedial actions taken", ["system"])

# Taxonomy of remedial actions
TAXONOMY = {
    "System Updates": ["Apply OS updates", "Upgrade installed packages"],
    "Service Restart": ["Restart SSH", "Restart Apache/IIS"],
    "Disk Cleanup": ["Clear temporary files", "Clean up logs"],
    "Device Reboot": ["Reboot device", "Restart services"],
}

# OS-specific remedial action registry
OS_REMEDIAL_ACTIONS = {}

def register_os_action(os_name):
    def decorator(func):
        OS_REMEDIAL_ACTIONS[os_name] = func
        return func
    return decorator

# Function to check if a tool exists
def is_tool_available(tool_name):
    return subprocess.call(["which", tool_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

# Function to let users select actions
def get_user_selected_actions():
    print("Available remedial actions:")
    available_actions = {}
    count = 1
    
    for category, actions in TAXONOMY.items():
        print(f"\n{category}:")
        for action in actions:
            print(f"  {count}. {action}")
            available_actions[count] = action
            count += 1
    
    selected_indices = input("Enter the numbers of the actions to perform (comma-separated): ")
    selected_actions = [available_actions[int(idx)] for idx in selected_indices.split(",") if idx.strip().isdigit() and int(idx) in available_actions]
    
    return selected_actions

# Android remedial actions
@register_os_action("Android")
def remedial_actions_android(system_name):
    selected_actions = get_user_selected_actions()
    REMEDIAL_ACTIONS_TRIGGERED.labels(system=system_name).inc()
    try:
        if "Reboot device" in selected_actions and is_tool_available("adb"):
            print("Rebooting device...")
            subprocess.run(["adb", "reboot"], check=True)
        if "Clear temporary files" in selected_actions and is_tool_available("adb"):
            print("Clearing app data...")
            subprocess.run(["adb", "shell", "pm", "clear", "com.example.app"], check=True)
    except Exception as e:
        print(f"Error performing {system_name} remedial actions: {e}")

# Linux remedial actions
@register_os_action("Linux")
def remedial_actions_linux(system_name):
    selected_actions = get_user_selected_actions()
    REMEDIAL_ACTIONS_TRIGGERED.labels(system=system_name).inc()
    try:
        if "Apply OS updates" in selected_actions:
            subprocess.run(["apt-get", "update", "-y"], check=True)
            subprocess.run(["apt-get", "upgrade", "-y"], check=True)
        if "Restart SSH" in selected_actions and is_tool_available("service"):
            subprocess.run(["service", "ssh", "restart"], check=True)
        if "Clear temporary files" in selected_actions:
            subprocess.run(["rm", "-rf", "/var/tmp/*"], check=True)
    except Exception as e:
        print(f"Error performing {system_name} remedial actions: {e}")

# Mac remedial actions
@register_os_action("Mac")
def remedial_actions_mac(system_name):
    selected_actions = get_user_selected_actions()
    REMEDIAL_ACTIONS_TRIGGERED.labels(system=system_name).inc()
    try:
        if "Apply OS updates" in selected_actions:
            print("Simulated: softwareupdate -i -a")
        if "Restart Apache/IIS" in selected_actions and is_tool_available("apachectl"):
            subprocess.run(["sudo", "apachectl", "restart"], check=True)
        if "Clear temporary files" in selected_actions:
            subprocess.run(["rm", "-rf", "/tmp/*"], check=True)
    except Exception as e:
        print(f"Error performing {system_name} remedial actions: {e}")

# Windows remedial actions
@register_os_action("Windows")
def remedial_actions_windows(system_name):
    selected_actions = get_user_selected_actions()
    REMEDIAL_ACTIONS_TRIGGERED.labels(system=system_name).inc()
    try:
        if "Apply OS updates" in selected_actions and is_tool_available("powershell"):
            subprocess.run(["powershell", "-Command", "Install-WindowsUpdate -AcceptAll"], check=True)
        if "Restart Apache/IIS" in selected_actions and is_tool_available("powershell"):
            subprocess.run(["powershell", "-Command", "Restart-Service -Name 'W3SVC'"], check=True)
        if "Clear temporary files" in selected_actions and is_tool_available("powershell"):
            subprocess.run(["powershell", "-Command", "cleanmgr /sagerun:1"], check=True)
    except Exception as e:
        print(f"Error performing {system_name} remedial actions: {e}")

# Default action handler
def remedial_actions_fallback(system_name):
    print(f"No specific remedial actions defined for {system_name}.")

def perform_remedial_actions(system_name):
    action_handler = OS_REMEDIAL_ACTIONS.get(system_name, remedial_actions_fallback)
    action_handler(system_name)

if __name__ == "__main__":
    system_name = input("Enter the system name (Android/Linux/Mac/Windows): ")
    perform_remedial_actions(system_name)
    app.run(host="0.0.0.0", port=8000)
