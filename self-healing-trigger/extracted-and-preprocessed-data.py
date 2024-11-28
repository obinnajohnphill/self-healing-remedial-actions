#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import os
import matplotlib.pyplot as plt

# Read in the log files
df_mac = pd.read_csv('dataset/system-logs/multiple-system-log-dataset/extracted-data/Mac_extracted.csv')
df_win = pd.read_csv('dataset/system-logs/multiple-system-log-dataset/extracted-data/Windows_extracted.csv')
df_android = pd.read_csv('dataset/system-logs/multiple-system-log-dataset/extracted-data/Android_extracted.csv')
df_linux = pd.read_csv('dataset/system-logs/multiple-system-log-dataset/extracted-data/Linux_extracted.csv')

# Concatenate the dataframes into a single dataframe
df_logs = pd.concat([df_mac, df_win, df_android, df_linux])

# Drop any rows with missing timestamps or tokens
df_logs = df_logs.dropna(subset=['timestamp', 'tokens'])

# Convert tokens column to string type
df_logs['tokens'] = df_logs['tokens'].astype(str)

# Fill missing error and warning values using forward fill
df_logs['error'] = df_logs['error'].fillna(method='ffill')
df_logs['warning'] = df_logs['warning'].fillna(method='ffill')

# Extract only the columns we need
df_logs = df_logs[['timestamp', 'tokens', 'error', 'warning']]

# Save preprocessed data to CSV files for each system
preprocessed_dir = 'dataset/system-logs/multiple-system-log-dataset/preprocessed-data'
os.makedirs(preprocessed_dir, exist_ok=True)

df_android.to_csv(os.path.join(preprocessed_dir, 'Android_preprocessed.csv'), index=False)
df_linux.to_csv(os.path.join(preprocessed_dir, 'Linux_preprocessed.csv'), index=False)
df_mac.to_csv(os.path.join(preprocessed_dir, 'Mac_preprocessed.csv'), index=False)
df_win.to_csv(os.path.join(preprocessed_dir, 'Windows_preprocessed.csv'), index=False)

# Define the bar chart data for the extracted data
systems_extracted = ['Android', 'Linux', 'Mac', 'Windows']
num_errors_extracted = [df_android[df_android['error'].notnull()].shape[0],
                        df_linux[df_linux['error'].notnull()].shape[0],
                        df_mac[df_mac['error'].notnull()].shape[0],
                        df_win[df_win['error'].notnull()].shape[0]]
num_warnings_extracted = [df_android[df_android['warning'].notnull()].shape[0],
                          df_linux[df_linux['warning'].notnull()].shape[0],
                          df_mac[df_mac['warning'].notnull()].shape[0],
                          df_win[df_win['warning'].notnull()].shape[0]]

# Set the plot style
plt.style.use('ggplot')

# Create the first bar chart for extracted data
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(systems_extracted, num_errors_extracted, color='#E74C3C', alpha=0.7, label='Errors')
ax.bar(systems_extracted, num_warnings_extracted, bottom=num_errors_extracted, color='#F39C12', alpha=0.7, label='Warnings')
ax.set_yscale('log')
#ax.set_title('Number of Errors and Warnings by System in Extracted Data')
ax.set_xlabel('System')
ax.set_ylabel('Number of Errors and Warnings (log scale)')
ax.legend(loc='upper right', bbox_to_anchor=(1.20, 1))

# Read in the preprocessed data
df_android_preprocessed = pd.read_csv(os.path.join(preprocessed_dir, 'Android_preprocessed.csv'))
df_linux_preprocessed = pd.read_csv(os.path.join(preprocessed_dir, 'Linux_preprocessed.csv'))
df_mac_preprocessed = pd.read_csv(os.path.join(preprocessed_dir, 'Mac_preprocessed.csv'))
df_win_preprocessed = pd.read_csv(os.path.join(preprocessed_dir, 'Windows_preprocessed.csv'))

# Calculate the number of errors and warnings for each system in the preprocessed data
num_errors_preprocessed = [df_android_preprocessed['error'].sum(),
                           df_linux_preprocessed['error'].sum(),
                           df_mac_preprocessed['error'].sum(),
                           df_win_preprocessed['error'].sum()]
num_warnings_preprocessed = [df_android_preprocessed['warning'].sum(),
                             df_linux_preprocessed['warning'].sum(),
                             df_mac_preprocessed['warning'].sum(),
                             df_win_preprocessed['warning'].sum()]

# Create the second bar chart for preprocessed data
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(systems_extracted, num_errors_preprocessed, color='#3498DB', alpha=0.7, label='Errors')
ax.bar(systems_extracted, num_warnings_preprocessed, bottom=num_errors_preprocessed, color='#2ECC71', alpha=0.7, label='Warnings')
ax.set_yscale('log')
#ax.set_title('Number of Errors and Warnings by System in Preprocessed Data')
ax.set_xlabel('System')
ax.set_ylabel('Number of Errors and Warnings (log scale)')
ax.legend(loc='upper right', bbox_to_anchor=(1.20, 1))

# Display both plots
plt.tight_layout()
plt.show()


# In[ ]:





# In[ ]:




