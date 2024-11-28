#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import os

# Read in the log files for each system
df_mac = pd.read_csv('dataset/system-logs/multiple-system-log-dataset/extracted-data/Mac_extracted.csv')
df_win = pd.read_csv('dataset/system-logs/multiple-system-log-dataset/extracted-data/Windows_extracted.csv')
df_android = pd.read_csv('dataset/system-logs/multiple-system-log-dataset/extracted-data/Android_extracted.csv')
df_linux = pd.read_csv('dataset/system-logs/multiple-system-log-dataset/extracted-data/Linux_extracted.csv')

# Drop any rows with missing timestamps or tokens for each system
df_mac = df_mac.dropna(subset=['timestamp', 'tokens'])
df_win = df_win.dropna(subset=['timestamp', 'tokens'])
df_android = df_android.dropna(subset=['timestamp', 'tokens'])
df_linux = df_linux.dropna(subset=['timestamp', 'tokens'])

# Convert tokens column to string type for each system
df_mac['tokens'] = df_mac['tokens'].astype(str)
df_win['tokens'] = df_win['tokens'].astype(str)
df_android['tokens'] = df_android['tokens'].astype(str)
df_linux['tokens'] = df_linux['tokens'].astype(str)

# Fill missing error and warning values using forward fill for each system
df_mac['error'] = df_mac['error'].fillna(method='ffill')
df_mac['warning'] = df_mac['warning'].fillna(method='ffill')
df_win['error'] = df_win['error'].fillna(method='ffill')
df_win['warning'] = df_win['warning'].fillna(method='ffill')
df_android['error'] = df_android['error'].fillna(method='ffill')
df_android['warning'] = df_android['warning'].fillna(method='ffill')
df_linux['error'] = df_linux['error'].fillna(method='ffill')
df_linux['warning'] = df_linux['warning'].fillna(method='ffill')

# Extract only the columns we need for each system
df_mac = df_mac[['timestamp', 'tokens', 'error', 'warning']]
df_win = df_win[['timestamp', 'tokens', 'error', 'warning']]
df_android = df_android[['timestamp', 'tokens', 'error', 'warning']]
df_linux = df_linux[['timestamp', 'tokens', 'error', 'warning']]

# Add Label column based on file name for each system
df_mac['Label'] = df_mac.index.get_level_values(0).astype(str).str.split('/').str[-1].str.split('.').str[0]
df_win['Label'] = df_win.index.get_level_values(0).astype(str).str.split('/').str[-1].str.split('.').str[0]
df_android['Label'] = df_android.index.get_level_values(0).astype(str).str.split('/').str[-1].str.split('.').str[0]
df_linux['Label'] = df_linux.index.get_level_values(0).astype(str).str.split('/').str[-1].str.split('.').str[0]

# Save preprocessed data to CSV files for each system
df_mac.to_csv('dataset/system-logs/multiple-system-log-dataset/preprocessed-data/Mac_preprocessed.csv', index=False)
df_win.to_csv('dataset/system-logs/multiple-system-log-dataset/preprocessed-data/Windows_preprocessed.csv', index=False)
df_android.to_csv('dataset/system-logs/multiple-system-log-dataset/preprocessed-data/Android_preprocessed.csv', index=False)
df_linux.to_csv('dataset/system-logs/multiple-system-log-dataset/preprocessed-data/Linux_preprocessed.csv', index=False)

preprocessed_dir = 'dataset/system-logs/multiple-system-log-dataset/preprocessed-data'
print(os.listdir(preprocessed_dir))


# In[ ]:




