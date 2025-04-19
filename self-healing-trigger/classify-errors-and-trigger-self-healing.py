#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import subprocess
from flask import Flask
from prometheus_client import Counter, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Initialize Flask App for Prometheus Metrics
app = Flask(__name__)

# Define Prometheus Metrics
ERRORS_DETECTED = Counter("errors_detected", "Number of errors detected", ["system"])
WARNINGS_DETECTED = Counter("warnings_detected", "Number of warnings detected", ["system"])
REMEDIAL_ACTIONS_TRIGGERED = Counter("remedial_actions_triggered", "Number of remedial actions taken", ["system"])

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
    return subprocess.call(["which", tool_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

@register_os_action("Android")
def remedial_actions_android(system_name):
    print(f"Performing remedial actions for {system_name}...")
    REMEDIAL_ACTIONS_TRIGGERED.labels(system=system_name).inc()
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

@register_os_action("Linux")
def remedial_actions_linux(system_name):
    print(f"Performing remedial actions for {system_name}...")
    REMEDIAL_ACTIONS_TRIGGERED.labels(system=system_name).inc()
    try:
        subprocess.run(["apt-get", "update", "-y"], check=True)
        subprocess.run(["apt-get", "upgrade", "-y"], check=True)
        if is_tool_available("systemctl"):
            subprocess.run(["systemctl", "restart", "ssh"], check=True)
        elif is_tool_available("service"):
            subprocess.run(["service", "ssh", "restart"], check=True)
        if os.path.isdir("/var/tmp") and os.access("/var/tmp", os.W_OK):
            subprocess.run(["rm", "-rf", "/var/tmp/*"], check=True)
    except Exception as e:
        print(f"Error performing {system_name} remedial actions: {e}")

@register_os_action("Mac")
def remedial_actions_mac(system_name):
    print(f"Performing remedial actions for {system_name}...")
    REMEDIAL_ACTIONS_TRIGGERED.labels(system=system_name).inc()
    try:
        if is_tool_available("apachectl"):
            subprocess.run(["sudo", "apachectl", "restart"], check=True)
        subprocess.run(["rm", "-rf", "/tmp/*"], check=True)
    except Exception as e:
        print(f"Error performing {system_name} remedial actions: {e}")

@register_os_action("Windows")
def remedial_actions_windows(system_name):
    print(f"Performing remedial actions for {system_name}...")
    REMEDIAL_ACTIONS_TRIGGERED.labels(system=system_name).inc()
    try:
        if is_tool_available("powershell"):
            subprocess.run(["powershell", "-Command", "Install-WindowsUpdate -AcceptAll"], check=True)
            subprocess.run(["powershell", "-Command", "Restart-Service -Name 'W3SVC'"], check=True)
            subprocess.run(["powershell", "-Command", "cleanmgr /sagerun:1"], check=True)
        else:
            raise Exception("PowerShell not available.")
    except Exception as e:
        print(f"Error performing {system_name} remedial actions: {e}")
        print("Simulated: PowerShell commands")

def remedial_actions_fallback(system_name):
    print(f"No specific remedial actions defined for {system_name}.")

def perform_remedial_actions(system_name):
    action_handler = OS_REMEDIAL_ACTIONS.get(system_name, remedial_actions_fallback)
    action_handler(system_name)

def process_logs():
    print("Starting the self-healing application...")
    preprocessed_dir = '/app/self-healing-trigger/dataset/system-logs/multiple-system-log-dataset/preprocessed-data'
    if not os.path.exists(preprocessed_dir):
        print(f"Error: The directory {preprocessed_dir} does not exist.")
        exit(1)

    system_dfs = {}
    for filename in os.listdir(preprocessed_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(preprocessed_dir, filename)
            try:
                df = pd.read_csv(filepath)
                system_name = os.path.splitext(filename)[0].replace("_preprocessed", "")
                system_dfs[system_name] = df
            except Exception as e:
                print(f"Error loading {filename}: {e}")

    error_threshold = 100
    warning_threshold = 500

    for system_name, df in system_dfs.items():
        try:
            num_errors = df['error'].sum()
            num_warnings = df['warning'].sum()
            ERRORS_DETECTED.labels(system=system_name).inc(num_errors)
            WARNINGS_DETECTED.labels(system=system_name).inc(num_warnings)
            if num_errors > error_threshold:
                perform_remedial_actions(system_name)
            elif num_warnings > warning_threshold:
                perform_remedial_actions(system_name)
            else:
                print(f"No remedial actions required for {system_name}.")
        except Exception as e:
            print(f"Error processing data for {system_name}: {e}")

app.wsgi_app = DispatcherMiddleware(app, {"/metrics": make_wsgi_app()})

if __name__ == "__main__":
    process_logs()
    app.run(host="0.0.0.0", port=8000)