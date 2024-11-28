#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import os
import matplotlib.pyplot as plt

# Define the preprocessed log directory
preprocessed_dir = 'dataset/system-logs/multiple-system-log-dataset/preprocessed-data'

# Create a dictionary to store dataframes for each system
system_dfs = {}

# Load the preprocessed log files
for filename in os.listdir(preprocessed_dir):
    if filename.endswith('.csv'):
        filepath = os.path.join(preprocessed_dir, filename)
        df = pd.read_csv(filepath)
        df.columns = df.columns.str.lower()
        system_name = os.path.splitext(filename)[0].replace("_preprocessed", "")
        system_dfs[system_name] = df

# Data exploration to determine appropriate thresholds
error_describe = pd.DataFrame({name: df['error'].describe() for name, df in system_dfs.items()})
warning_describe = pd.DataFrame({name: df['warning'].describe() for name, df in system_dfs.items()})

print("Error Statistics across Systems:")
print(error_describe)
print("\nWarning Statistics across Systems:")
print(warning_describe)

# Modify thresholds based on data exploration
error_threshold = error_describe.loc['75%', :].mean()  # Setting threshold at 75th percentile average
warning_threshold = warning_describe.loc['75%', :].mean()  # Setting threshold at 75th percentile average

# Calculating triggers based on new thresholds
trigger_data = []
for system_name, df in system_dfs.items():
    df['trigger'] = ((df['error'] > error_threshold) | (df['warning'] > warning_threshold)).astype(int)
    num_errors = df['error'].sum()
    num_warnings = df['warning'].sum()
    trigger = df['trigger'].max()
    
    print("\n")

    # Self-healing logic placeholder
    if trigger == 1:
        # Self-healing logic will be implemented here in the future
        print(f"Self-healing triggered for {system_name}")

    trigger_data.append([system_name, num_errors, num_warnings, trigger])

trigger_df = pd.DataFrame(trigger_data, columns=['System', 'Errors', 'Warnings', 'Trigger'])

# Summary of trigger conditions
print("\nUpdated Trigger Conditions:")
print(trigger_df[['System', 'Trigger']])

# Print the placeholder comment
print("\nNOTE: Self-healing logic will be implemented in the future where the placeholder comment is.")

# Visualizing the updated thresholds and data points
plt.figure(figsize=(12, 6))
for system_name, df in system_dfs.items():
    plt.scatter(df['error'], df['warning'], label=system_name)
plt.axvline(x=error_threshold, color='r', linestyle='--', label='Error Threshold')
plt.axhline(y=warning_threshold, color='b', linestyle='--', label='Warning Threshold')
plt.xlabel('Errors')
plt.ylabel('Warnings')
plt.title('Error and Warning Levels with Thresholds')
plt.legend()
plt.grid(True)
plt.show()


# In[ ]:




