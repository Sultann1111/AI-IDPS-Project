# src/data_loader.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder


def load_data(train_path, test_path):
    """
    Load UNSW-NB15 dataset
    """

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    print("Training Data Shape:", train_df.shape)
    print("Testing Data Shape:", test_df.shape)

    return train_df, test_df


def preprocess_data(df):
    """
    Clean dataset and encode categorical features
    """

    df = df.copy()

    # Remove columns that cause data leakage
    if "attack_cat" in df.columns:
        df = df.drop(columns=["attack_cat"])

    if "id" in df.columns:
        df = df.drop(columns=["id"])

    # Encode categorical columns
    categorical_cols = df.select_dtypes(include=["object"]).columns

    for col in categorical_cols:
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col])

    return df


def prepare_datasets():

    train_path = "UNSW_NB15_training-set.csv"
    test_path = "UNSW_NB15_testing-set.csv"

    train_df, test_df = load_data(train_path, test_path)

    train_df = preprocess_data(train_df)
    test_df = preprocess_data(test_df)

    y_train = train_df["label"]
    X_train = train_df.drop(columns=["label"])

    y_test = test_df["label"]
    X_test = test_df.drop(columns=["label"])

    feature_names = X_train.columns.tolist()

    print("X_train shape:", X_train.shape)
    print("X_test shape:", X_test.shape)

    return X_train, X_test, y_train, y_test, feature_names