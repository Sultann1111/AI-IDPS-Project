"""
Dataset loading and preprocessing module
"""

import pandas as pd


def prepare_datasets(train_path, test_path):

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    print("Training Data Shape:", train_df.shape)
    print("Testing Data Shape:", test_df.shape)

    # Remove unnecessary columns
    columns_to_drop = ["id", "attack_cat"]

    for col in columns_to_drop:
        if col in train_df.columns:
            train_df.drop(columns=[col], inplace=True)

        if col in test_df.columns:
            test_df.drop(columns=[col], inplace=True)

    # Encode categorical features
    categorical_cols = ["proto", "service", "state"]

    for col in categorical_cols:
        if col in train_df.columns:
            train_df[col] = train_df[col].astype("category").cat.codes

        if col in test_df.columns:
            test_df[col] = test_df[col].astype("category").cat.codes

    # Split features and labels
    X_train = train_df.drop("label", axis=1)
    y_train = train_df["label"]

    X_test = test_df.drop("label", axis=1)
    y_test = test_df["label"]

    feature_names = X_train.columns.tolist()

    print("X_train shape:", X_train.shape)
    print("X_test shape:", X_test.shape)

    return X_train, X_test, y_train, y_test, feature_names