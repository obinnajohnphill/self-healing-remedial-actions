#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import time

print("Starting the self-healing application...")

# Define the preprocessed log directory
preprocessed_dir = '/app/self-healing-trigger/dataset/system-logs/multiple-system-log-dataset/preprocessed-data'

# Check if the directory exists
if not os.path.exists(preprocessed_dir):
    print(f"Error: The directory {preprocessed_dir} does not exist.")
    exit(1)  # Exit the application if the directory is missing

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
            # Extract system name from the filename and remove "_preprocessed" suffix
            system_name = os.path.splitext(filename)[0].replace("_preprocessed", "")
            # Add the dataframe to the dictionary with the system name as the key
            system_dfs[system_name] = df
            print(f"Loaded data for system: {system_name}")
        except Exception as e:
            print(f"Error loading {filename}: {e}")

# Function to calculate the number of words in a list of tokens
def count_words(tokens_list):
    try:
        return sum(len(token.split()) for token in tokens_list)
    except Exception as e:
        print(f"Error in count_words function: {e}")
        return 0

# Create a new dataframe to store the summary for each system
summary_df = pd.DataFrame(columns=['error', 'warning', 'tokens', 'Label'])

# Loop through each system dataframe, calculate the summary statistics, and append to the summary_df
for system_name, df in system_dfs.items():
    start_time = time.time()
    print(f"Processing data for system: {system_name}")
    try:
        # Debug prints for each step
        print(f"Calculating number of errors for {system_name}...")
        num_errors = df['error'].sum()
        print(f"Number of errors: {num_errors}")

        print(f"Calculating number of warnings for {system_name}...")
        num_warnings = df['warning'].sum()
        print(f"Number of warnings: {num_warnings}")

        print(f"Calculating tokens for {system_name}...")
        num_tokens = df['tokens'].apply(eval).apply(count_words).mean()
        print(f"Number of tokens: {num_tokens}")

        print(f"Summing labels for {system_name}...")
        # Debug the Label column
        print(f"Label column values (sample): {df['Label'].head()}")
        print(f"Label column data type: {df['Label'].dtype}")

        # Convert non-numeric data to 0
        df['Label'] = pd.to_numeric(df['Label'], errors='coerce').fillna(0)

        # Measure summation time
        start_sum_time = time.time()
        sum_labels = np.sum(df['Label'])
        print(f"Summing labels took {time.time() - start_sum_time:.2f} seconds.")

        # Append to summary_df
        summary_df.loc[system_name] = [num_errors, num_warnings, num_tokens, sum_labels]
        print(f"Finished processing data for {system_name} in {time.time() - start_time:.2f} seconds.")
    except Exception as e:
        print(f"Error processing data for {system_name}: {e}")

# Define the error and warning thresholds for triggering self-healing action
error_threshold = 100
warning_threshold = 500

# Print feature table
print("\nFeaturised Data Summary:")
print(summary_df)

# Check for each system if the number of errors or warnings exceeds the thresholds
print("\nSelf-Healing Triggers:")
for system_name, df in system_dfs.items():
    try:
        num_errors = summary_df.loc[system_name, 'error']
        num_warnings = summary_df.loc[system_name, 'warning']

        if num_errors > error_threshold:
            print(f"Number of errors ({num_errors}) exceeds threshold ({error_threshold}). Triggering self-healing action for {system_name}...")
            # Add your code for self-healing action here

        elif num_warnings > warning_threshold:
            print(f"Number of warnings ({num_warnings}) exceeds threshold ({warning_threshold}). Triggering self-healing action for {system_name}...")
            # Add your code for self-healing action here

        else:
            print(f"No errors or warnings exceeded the thresholds for {system_name}. No self-healing action triggered.")
    except Exception as e:
        print(f"Error triggering self-healing for {system_name}: {e}")

# Create a scatter chart with different colors for each system and lines connecting the points
print("Generating scatter chart...")
try:
    plt.figure(figsize=(10, 6))
    color_map = plt.get_cmap('tab10')

    for i, system_name in enumerate(summary_df.index):
        plt.scatter(summary_df.loc[system_name, 'error'], summary_df.loc[system_name, 'warning'],
                    s=summary_df.loc[system_name, 'tokens'] * 5, c=[color_map(i)], label=system_name, alpha=0.7)
        plt.plot(summary_df.loc[system_name, 'error'], summary_df.loc[system_name, 'warning'],
                 color=color_map(i), linestyle='-', alpha=0.7)

    plt.colorbar(label='Sum of Labels')
    plt.xlabel('Number of Errors', fontsize=12)
    plt.ylabel('Number of Warnings', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='dotted', alpha=0.5)
    plt.tight_layout()
    plt.savefig('featurised_scatter_chart.png', dpi=600)
    plt.show()
except Exception as e:
    print(f"Error generating scatter chart: {e}")

# Plot horizontal bar charts for errors and warnings based on system type
print("Generating bar charts...")
try:
    plt.figure(figsize=(12, 6))
    bar_width = 0.35
    index = np.arange(len(summary_df))

    plt.barh(index, summary_df['error'], bar_width, label='Errors', color='#FF5733')
    plt.barh(index + bar_width, summary_df['warning'], bar_width, label='Warnings', color='#FFA033')

    plt.ylabel('System', fontsize=12)
    plt.xlabel('Count', fontsize=12)
    plt.xscale('log')
    plt.yticks(index + bar_width / 2, summary_df.index, fontsize=10)
    plt.xticks(fontsize=10)
    plt.legend(fontsize=12, loc='upper right', bbox_to_anchor=(1.20, 1))
    plt.grid(True, linestyle='dotted', alpha=0.5)
    plt.tight_layout()
    plt.savefig('errors_warnings_by_system.png', dpi=600)
    plt.show()
except Exception as e:
    print(f"Error generating bar charts: {e}")

print("Self-healing application completed successfully.")
