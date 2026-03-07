"""
Real-time intrusion prediction module
"""

import joblib
import pandas as pd


def load_model(model_path="models/ids_model.pkl"):

    model = joblib.load(model_path)

    return model


def predict_traffic(sample_data):

    model = load_model()

    predictions = model.predict(sample_data)

    probabilities = model.predict_proba(sample_data)[:,1]

    results = []

    for i in range(len(predictions)):

        if predictions[i] == 1:
            label = "ATTACK"
        else:
            label = "NORMAL"

        results.append({
            "prediction": label,
            "attack_probability": float(probabilities[i])
        })

    return results