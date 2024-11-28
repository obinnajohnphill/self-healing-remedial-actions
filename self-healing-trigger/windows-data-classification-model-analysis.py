#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pycaret.classification import setup, compare_models, finalize_model, predict_model, pull
import gc

# Function to free up memory
def free_memory():
    gc.collect()

# Load Windows dataset
file_path = 'dataset/system-logs/multiple-system-log-dataset/preprocessed-data/Windows_preprocessed.csv'
df = pd.read_csv(file_path)

# Reduce the dataset size significantly for faster processing (if necessary)
df = df.sample(frac=0.05, random_state=42)  # Use 5% of the data

# Check class distribution
print("Class distribution in Windows:")
print(df['error'].value_counts())

# Setup the data in PyCaret with reduced verbosity and fewer folds
try:
    setup_data = setup(data=df, target='error', session_id=42, fold=3, fix_imbalance=False, verbose=False)
except MemoryError:
    print("Memory error during setup. Please try reducing the data size further.")
    exit()

# Compare all models
try:
    best_models = compare_models(n_select=3)  # Select top 3 models
except MemoryError:
    print("Memory error during model comparison. Exiting.")
    exit()

# Iterate through each model, finalize, and make predictions
for model in best_models:
    try:
        # Finalize the model
        final_model = finalize_model(model)

        # Free memory before making predictions
        free_memory()

        # Display the final model performance
        print(f"Final tuned model performance for {model}:")
        predictions = predict_model(final_model)
        print(predictions)
        
        # Pull and print the metrics
        metrics = pull()
        print(metrics)

    except MemoryError:
        print(f"Memory error during processing model {model}. Skipping.")
        continue

# Additional memory management
free_memory()


# In[ ]:




