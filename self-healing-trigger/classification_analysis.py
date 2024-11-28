#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import re
from pycaret.classification import setup, compare_models

# Define the log file paths
log_files = [
    'dataset/system-logs/multiple-system-log-dataset/extracted-data/Mac_extracted.csv',
    'dataset/system-logs/multiple-system-log-dataset/extracted-data/Windows_extracted.csv',
    'dataset/system-logs/multiple-system-log-dataset/extracted-data/Android_extracted.csv',
    'dataset/system-logs/multiple-system-log-dataset/extracted-data/Linux_extracted.csv'
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

# Preprocess the text data
df_logs['tokens'] = df_logs['tokens'].apply(lambda x: re.sub(r'\W+', ' ', x.lower()))

# Preprocess the text data using TF-IDF vectorization
vectorizer = TfidfVectorizer()
text_features = vectorizer.fit_transform(df_logs['tokens'])
text_features_df = pd.DataFrame(text_features.toarray(), columns=vectorizer.get_feature_names_out())

# Reset the index of the 'df_logs' dataframe before concatenating
df_logs.reset_index(drop=True, inplace=True)

# Drop the 'tokens' column before concatenating
df_logs.drop('tokens', axis=1, inplace=True)

# Concatenate the text features with the original dataframe
df_logs = pd.concat([df_logs, text_features_df], axis=1)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    df_logs.drop('Label', axis=1),
    df_logs['Label'],
    test_size=0.2,
    random_state=123
)

# Separate the numerical features from the TF-IDF vectors
numeric_features = X_train.select_dtypes(include=['number'])
text_features = X_train.drop(numeric_features.columns, axis=1)

# Scale the numerical features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(numeric_features)
X_test_scaled = scaler.transform(X_test.select_dtypes(include=['number']))

# Concatenate the scaled numerical features with the text features
X_train_final = pd.concat([pd.DataFrame(X_train_scaled, columns=numeric_features.columns), text_features], axis=1)
X_test_final = pd.concat([
    pd.DataFrame(X_test_scaled, columns=numeric_features.columns),
    X_test.drop(numeric_features.columns, axis=1)
], axis=1)


# Check for duplicate column names
duplicate_columns = df_logs.columns[df_logs.columns.duplicated()]
if len(duplicate_columns) > 0:
    # Handle duplicate column names
    # Option 1: Remove duplicate columns
    df_logs = df_logs.loc[:, ~df_logs.columns.duplicated()]
    
    # Option 2: Rename duplicate columns
    # df_logs = df_logs.rename(columns={'duplicate_column': 'new_column_name'})

# Setup the classification task
s = setup(df_logs, target='Label', session_id=123)

# Compare baseline models
best = compare_models()


print('\n')
print("The best 5 performing classification models")
# Get the best 5 performing models
best_five_models = compare_models(n_select=5)

# Display the performance of the best 5 models
for model in best_five_models:
    print(model)
    print('\n')
    
print('\n')
print("The best performing classification model")
# Get the best 5 performing models
best_model = compare_models(n_select=1)

# Display the performance of the best model
print(best_model)
print('\n')


# In[ ]:




