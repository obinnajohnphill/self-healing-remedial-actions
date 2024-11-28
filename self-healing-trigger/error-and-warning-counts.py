#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

# Read in the log files for extracted data
df_mac = pd.read_csv('dataset/system-logs/multiple-system-log-dataset/extracted-data/Mac_extracted.csv')
df_win = pd.read_csv('dataset/system-logs/multiple-system-log-dataset/extracted-data/Windows_extracted.csv')
df_android = pd.read_csv('dataset/system-logs/multiple-system-log-dataset/extracted-data/Android_extracted.csv')
df_linux = pd.read_csv('dataset/system-logs/multiple-system-log-dataset/extracted-data/Linux_extracted.csv')

# Extract the error and warning count in each dataset for extracted data
error_counts_extracted = [df_android['error'].count(), df_linux['error'].count(), df_mac['error'].count(), df_win['error'].count()]
warning_counts_extracted = [df_android['warning'].count(), df_linux['warning'].count(), df_mac['warning'].count(), df_win['warning'].count()]

# Define the dataset names for extracted data
datasets_extracted = ['Android', 'Linux', 'Mac', 'Windows']

# Set the Seaborn style
sns.set(style='whitegrid')

# Create subplots for extracted data
fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=600)

# Plot the error and warning counts as separate bar charts for extracted data
axes[0].bar(datasets_extracted, error_counts_extracted, color='#1f77b4', label='Errors')
axes[0].set_xlabel('System')
axes[0].set_ylabel('Error Count (log scale)')
axes[0].set_yscale('log')
#axes[0].set_title('Error Count in Extracted Data')
axes[0].legend()

axes[1].bar(datasets_extracted, warning_counts_extracted, color='#ff7f0e', label='Warnings')
axes[1].set_xlabel('System')
axes[1].set_ylabel('Warning Count (log scale)')
axes[1].set_yscale('log')
#axes[1].set_title('Warning Count in Extracted Data')
axes[1].legend()

# Print tables for error and warning counts in extracted data
table_extracted_errors = {
    'Dataset': datasets_extracted,
    'Error Count': error_counts_extracted
}
print("Extracted Data Error Count")
print(tabulate(table_extracted_errors, headers='keys', tablefmt='grid'))

table_extracted_warnings = {
    'Dataset': datasets_extracted,
    'Warning Count': warning_counts_extracted
}
print("\nExtracted Data Warning Count")
print(tabulate(table_extracted_warnings, headers='keys', tablefmt='grid'))

# Read in the preprocessed data
df_mac_preprocessed = pd.read_csv('dataset/system-logs/multiple-system-log-dataset/preprocessed-data/Mac_preprocessed.csv')
df_win_preprocessed = pd.read_csv('dataset/system-logs/multiple-system-log-dataset/preprocessed-data/Windows_preprocessed.csv')
df_android_preprocessed = pd.read_csv('dataset/system-logs/multiple-system-log-dataset/preprocessed-data/Android_preprocessed.csv')
df_linux_preprocessed = pd.read_csv('dataset/system-logs/multiple-system-log-dataset/preprocessed-data/Linux_preprocessed.csv')

# Calculate the error and warning count for each dataset in the preprocessed data
error_counts_preprocessed = [df_android_preprocessed['error'].sum(), df_linux_preprocessed['error'].sum(),
                            df_mac_preprocessed['error'].sum(), df_win_preprocessed['error'].sum()]
warning_counts_preprocessed = [df_android_preprocessed['warning'].sum(), df_linux_preprocessed['warning'].sum(),
                               df_mac_preprocessed['warning'].sum(), df_win_preprocessed['warning'].sum()]

# Define the dataset names for preprocessed data
datasets_preprocessed = ['Android', 'Linux', 'Mac', 'Windows']

# Create subplots for preprocessed data
fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=600)

# Plot the error and warning counts as separate bar charts for preprocessed data
axes[0].bar(datasets_preprocessed, error_counts_preprocessed, color='#2ca02c', label='Errors')
axes[0].set_xlabel('System')
axes[0].set_ylabel('Error Count (log scale)')
axes[0].set_yscale('log')
#axes[0].set_title('Error Count in Preprocessed Data')
axes[0].legend()

axes[1].bar(datasets_preprocessed, warning_counts_preprocessed, color='#9467bd', label='Warnings')
axes[1].set_xlabel('System')
axes[1].set_ylabel('Warning Count (log scale)')
axes[1].set_yscale('log')
#axes[1].set_title('Warning Count in Preprocessed Data')
axes[1].legend()

# Print tables for error and warning counts in preprocessed data
table_preprocessed_errors = {
    'Dataset': datasets_preprocessed,
    'Error Count': error_counts_preprocessed
}
print("\nPreprocessed Data Error Count")
print(tabulate(table_preprocessed_errors, headers='keys', tablefmt='grid'))

table_preprocessed_warnings = {
    'Dataset': datasets_preprocessed,
    'Warning Count': warning_counts_preprocessed
}
print("\nPreprocessed Data Warning Count")
print(tabulate(table_preprocessed_warnings, headers='keys', tablefmt='grid'))

# Display both plots
plt.tight_layout()
plt.show()


# In[ ]:





# In[ ]:




