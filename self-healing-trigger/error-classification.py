#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from datetime import datetime
import re

# Define the log file paths
log_files = ['dataset/system-logs/multiple-system-log-dataset/extracted-data/Mac_extracted.csv', 
             'dataset/system-logs/multiple-system-log-dataset/extracted-data/Windows_extracted.csv', 
             'dataset/system-logs/multiple-system-log-dataset/extracted-data/Android_extracted.csv',
             'dataset/system-logs/multiple-system-log-dataset/extracted-data/Linux_extracted.csv',
            ]

# Define the timestamp regex pattern
timestamp_regex = r'(?:\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})|(?:\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})|(?:\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})'

# Load preprocessed log data
df_logs = pd.DataFrame()
for file in log_files:
    try:
        df = pd.read_csv(file, usecols=['timestamp', 'tokens', 'error', 'warning'])
        df['Label'] = file.split('/')[-1].split('_')[0]
        df_logs = pd.concat([df_logs, df])
    except ValueError as e:
        print(f"Error: {e}. Skipping this file.")

# Extract timestamp from the tokens column and convert to datetime object
df_logs['timestamp'] = df_logs['tokens'].str.extract(f'({timestamp_regex})', expand=False)
df_logs['timestamp'] = pd.to_datetime(df_logs['timestamp'], errors='coerce')

# Summarize the log data
for system, df in df_logs.groupby('Label'):
    num_errors = df['error'].sum()
    num_warnings = df['warning'].sum()
    print("")
    print(f"System: {system}")
    print(f"Number of errors: {num_errors}")
    print(f"Number of warnings: {num_warnings}")
    print("")

    


# In[ ]:





# In[ ]:




