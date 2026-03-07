"""
Model training module
"""

import os
import joblib
from lightgbm import LGBMClassifier


def train_model(X_train, y_train):

    model = LGBMClassifier(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=-1,
        num_leaves=64,
        random_state=42
    )

    model.fit(X_train, y_train)

    return model


def save_model(model):

    os.makedirs("models", exist_ok=True)

    path = "models/ids_model.pkl"

    joblib.dump(model, path)

    print("Model saved to:", path)