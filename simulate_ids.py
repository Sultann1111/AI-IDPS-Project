"""
Simulate real-time IDS predictions
"""

import pandas as pd
from src.predict import predict_traffic

# Load small traffic sample
data = pd.read_csv("data/UNSW_NB15_testing-set.csv")

# Prepare sample
sample = data.sample(10)

# Drop non-feature columns
columns_to_drop = ["id", "attack_cat", "label"]

for col in columns_to_drop:
    if col in sample.columns:
        sample.drop(columns=[col], inplace=True)

# Encode categorical
categorical_cols = ["proto", "service", "state"]

for col in categorical_cols:
    if col in sample.columns:
        sample[col] = sample[col].astype("category").cat.codes


results = predict_traffic(sample)

print("\n=== Intrusion Detection Results ===\n")

for r in results:
    print(r)