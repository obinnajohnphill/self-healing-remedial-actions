#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from pycaret.classification import setup, compare_models, evaluate_model, pull

# Function to perform analysis with Multinomial Naive Bayes
def mnb_self_healing(data, labels, system_name):
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)
    mnb_model = MultinomialNB()
    mnb_model.fit(data_scaled, labels)
    predicted_labels = mnb_model.predict(data_scaled)
    accuracy = accuracy_score(labels, predicted_labels)
    print(f"{system_name} MNB Accuracy:", accuracy)
    plot_results(data, labels, predicted_labels, system_name, 'Multinomial Naive Bayes')

# Logistic Regression Analysis
def lr_self_healing(data, labels, system_name):
    lr_model = LogisticRegression(max_iter=1000)
    lr_model.fit(data, labels)
    predicted_labels = lr_model.predict(data)
    accuracy = accuracy_score(labels, predicted_labels)
    print(f"{system_name} LR Accuracy:", accuracy)
    plot_results(data, labels, predicted_labels, system_name, 'Logistic Regression')

# Linear Discriminant Analysis
def lda_self_healing(data, labels, system_name):
    lda_model = LinearDiscriminantAnalysis()
    lda_model.fit(data, labels)
    predicted_labels = lda_model.predict(data)
    accuracy = accuracy_score(labels, predicted_labels)
    print(f"{system_name} LDA Accuracy:", accuracy)
    plot_results(data, labels, predicted_labels, system_name, 'Linear Discriminant Analysis')

# Gradient Boosting Classifier
def gbc_self_healing(data, labels, system_name):
    gbc_model = GradientBoostingClassifier()
    gbc_model.fit(data, labels)
    predicted_labels = gbc_model.predict(data)
    accuracy = accuracy_score(labels, predicted_labels)
    print(f"{system_name} GBC Accuracy:", accuracy)
    plot_results(data, labels, predicted_labels, system_name, 'Gradient Boosting Classifier')

# Function to plot results
def plot_results(data, labels, predicted_labels, system_name, model_name):
    plt.figure(figsize=(10, 6))
    plt.scatter(data[:, 0], data[:, 1], c=labels, cmap='viridis', alpha=0.5, label='Actual Labels')
    plt.scatter(data[:, 0], data[:, 1], c=predicted_labels, cmap='coolwarm', alpha=0.2, marker='x', label='Predicted Labels')
    plt.title(f'{system_name} - {model_name}')
    plt.xlabel('Error')
    plt.ylabel('Warning')
    plt.legend()
    plt.show()

# Prepare the data for PyCaret analysis
datasets = {
    'Android': 'dataset/system-logs/multiple-system-log-dataset/preprocessed-data/Android_preprocessed.csv',
    'Linux': 'dataset/system-logs/multiple-system-log-dataset/preprocessed-data/Linux_preprocessed.csv',
    'Mac': 'dataset/system-logs/multiple-system-log-dataset/preprocessed-data/Mac_preprocessed.csv',
    'Windows': 'dataset/system-logs/multiple-system-log-dataset/preprocessed-data/Windows_preprocessed.csv'
}

# Assuming the CSV files are structured with 'Error', 'Warning', and 'Label' columns
for system_name, csv_file in datasets.items():
    print(f"\nRunning analysis for {system_name}")
    df = pd.read_csv(csv_file)  # Load your dataset here
    
    # Check class distribution before filtering
    print(f"Class distribution for {system_name} before filtering:")
    print(df['Label'].value_counts())
    
    # Combine infrequent classes into a single 'Other' category
    min_class_count = 2
    value_counts = df['Label'].value_counts()
    to_replace = value_counts[value_counts < min_class_count].index
    df['Label'] = df['Label'].replace(to_replace, 'Other')
    
    # Check class distribution after handling infrequent classes
    print(f"Class distribution for {system_name} after handling infrequent classes:")
    print(df['Label'].value_counts())
    
    # Use the dataframe directly for PyCaret setup
    clf_setup = setup(data=df, target='Label', session_id=42, verbose=False)
    top4_models = compare_models(n_select=4, sort='Accuracy')
    
    # Pulling the performance result of the top 4 models
    results = pull()
    print(f"Top 4 Models for {system_name}:")
    print(results.head(4))  # Displaying the top 4 models based on Accuracy
    
    # Example data generation (replace with actual data loading)
    np.random.seed(42)
    num_samples = 2000
    data = np.random.randn(num_samples, 2)
    labels = np.random.randint(0, 3, num_samples)
    
    # Scaling data for MNB
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)
    
    # Call each analysis function
    mnb_self_healing(data_scaled, labels, system_name)
    lr_self_healing(data, labels, system_name)
    lda_self_healing(data, labels, system_name)
    gbc_self_healing(data, labels, system_name)


# In[ ]:





# In[ ]:




