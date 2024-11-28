#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from pycaret.classification import setup, compare_models, tune_model, finalize_model, predict_model

# Load Android dataset
file_path = 'dataset/system-logs/multiple-system-log-dataset/preprocessed-data/Android_preprocessed.csv'
df = pd.read_csv(file_path)

# Check class distribution
print("Class distribution in Android:")
print(df['error'].value_counts())

# Setup the data in PyCaret without automatic imbalance handling
setup_data = setup(data=df, target='error', session_id=42, fold=10, fix_imbalance=False, verbose=True)

# Compare and evaluate models
best_model = compare_models()
tuned_best_model = tune_model(best_model, optimize='AUC', n_iter=30)
final_model = finalize_model(tuned_best_model)

# Displaying the final model
print("Final tuned model performance for Android:")
predict_model(final_model)


# In[ ]:




