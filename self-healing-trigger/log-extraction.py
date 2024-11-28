#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import re

# Function to parse log file and extract relevant information
def parse_log_file(log_file_path):
    # Open log file
    with open(log_file_path, 'r', encoding="utf8", errors='ignore') as f:
        log_lines = f.readlines()

    # Extract relevant information from log lines
    log_entries = []
    for line in log_lines:
        # Skip lines that don't contain errors or warnings
        if 'ERROR' not in line and 'WARNING' not in line:
            continue

        # Extract timestamp and log message
        timestamp_regex = r'(?:\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})|(?:\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})|(?:\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})'
        timestamp = re.search(timestamp_regex, line)
        if not timestamp:
            continue
        timestamp = timestamp.group(0)

        log_message = re.sub(r'^.*?:\s', '', line.strip())

        # Add log entry to list
        log_entries.append((timestamp, log_message))

    # Convert log entries into a Pandas DataFrame
    log_df = pd.DataFrame(log_entries, columns=['timestamp', 'log_message'])

    return log_df

# Function to preprocess log data for machine learning classification
def preprocess_logs(log_df):
    # Tokenize log messages
    log_df['tokens'] = log_df['log_message'].str.split()

    # Extract relevant features
    log_df['error'] = log_df['log_message'].apply(lambda x: 1 if 'ERROR' in x else 0)
    log_df['warning'] = log_df['log_message'].apply(lambda x: 1 if 'WARNING' in x else 0)

    # Drop irrelevant columns
    log_df = log_df.drop(columns=['log_message'])

    return log_df

# Define log files to process
log_files = ['dataset/system-logs/Mac.log', 'dataset/system-logs/Windows.log', 'dataset/system-logs/Android.log']

# Process each log file and save results as CSV file
for log_file in log_files:
    # Determine output file name based on input file name
    file_name = os.path.basename(log_file)
    output_file_name = f"dataset/system-logs/multiple-system-log-dataset/extracted-data/{os.path.splitext(file_name)[0]}_extracted.csv"

    # Parse log file and preprocess data
    log_df = parse_log_file(log_file)
    processed_df = preprocess_logs(log_df)

    # Save processed data as CSV file
    processed_df.to_csv(output_file_name, index=False)

    # Print information about the generated dataset
    print(f"{output_file_name} generated with {len(processed_df)} entries")
    
# For Linux extraction
# Function to parse log entry and extract relevant information
def parse_log_entry(log_entry, severity_levels):
    timestamp_regex = r'(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})'
    log_match = re.search(timestamp_regex, log_entry)
    if log_match:
        timestamp = log_match.group(1)
        log_message = log_entry[log_match.end():].strip()
        tokens = log_message.split()  # Tokenize the log_message

        # Set initial error and warning values to 0
        error = 0
        warning = 0

        # Check for severity levels and assign labels
        for pattern, label in severity_levels.items():
            if re.search(pattern, log_message, re.IGNORECASE):  # Make the search case-insensitive
                if label in ['error', 'emergency', 'critical']:
                    error = 1
                elif label == 'warning':
                    warning = 1
                elif label == 'alert':
                    warning = 1
                break

        return timestamp, tokens, error, warning
    else:
        return None, None, None, None

# Define the severity level keywords and their corresponding labels
severity_levels = {
    r'(EMERG|PANIC)': 'emergency',
    r'\b(ALERT|alert)\b': 'alert',           # Make 'ALERT' a whole word match (case-insensitive)
    r'(CRIT|CRITICAL)': 'critical',
    r'(ERR|ERROR|FAILED)': 'error', # Make 'FAILED' case-sensitive
    r'(WARNING|WARN)': 'warning',
    r'NOTICE': 'notice',
    r'(INFO|INFORMATIONAL)': 'info',
    r'DEBUG': 'debug',
}

# Define log file to process - make sure it points to the correct file path
log_file = 'dataset/system-logs/Linux.log'

# Read log entries from the file using a regex pattern
with open(log_file, 'r', encoding='utf8', errors='ignore') as f:
    log_content = f.read()
    log_entries = re.findall(r'\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2} .*', log_content)

# Create a list to store all log entries
all_log_entries = []

# Process each log entry and store results in the list
for log_entry in log_entries:
    # Parse log entry and extract relevant information
    timestamp, tokens, error, warning = parse_log_entry(log_entry, severity_levels)

    # Check if timestamp and tokens are None (no relevant data found in the log entry)
    if timestamp is None or tokens is None:
        continue  # Skip processing this log entry

    # Find 'ALERT' in tokens and set the corresponding warning flag to 1
    if 'ALERT' in tokens:
        warning = 1

    # Append the log entry to the list
    all_log_entries.append({
        'timestamp': timestamp,
        'tokens': tokens,
        'error': error,
        'warning': warning
    })

# Convert the list of log entries into a DataFrame
all_log_entries_df = pd.DataFrame(all_log_entries, columns=['timestamp', 'tokens', 'error', 'warning'])

# Determine output file name based on input file name
file_name = os.path.basename(log_file)
output_directory = "dataset/system-logs/multiple-system-log-dataset/extracted-data/"
os.makedirs(output_directory, exist_ok=True)  # Create output directory if it doesn't exist
output_file_name = os.path.join(output_directory, f"{os.path.splitext(file_name)[0]}_extracted.csv")

# Save all log entries as CSV file
all_log_entries_df.to_csv(output_file_name, index=False)

# Print information about the generated dataset
print(f"{output_file_name} generated with {len(all_log_entries_df)} entries")


# In[ ]:





# In[ ]:




