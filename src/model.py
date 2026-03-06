# src/model.py

import lightgbm as lgb
import joblib
import os


def train_model(X_train, y_train):
    """
    Train the LightGBM model
    """

    model = lgb.LGBMClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=8,
        random_state=42
    )

    model.fit(X_train, y_train)

    return model


def save_model(model, path):
    """
    Save trained model
    """

    os.makedirs(os.path.dirname(path), exist_ok=True)

    joblib.dump(model, path)

    print(f"Model saved to: {path}")