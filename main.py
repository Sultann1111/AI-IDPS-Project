from src.data_loader import prepare_datasets
from src.model import train_model, save_model
from src.evaluate import evaluate_model


def main():

    print("Loading and preparing dataset...")

    X_train, X_test, y_train, y_test, feature_names = prepare_datasets()

    print("\nTraining AI intrusion detection model...")

    model = train_model(X_train, y_train)

    evaluate_model(model, X_test, y_test, feature_names)

    print("\nSaving trained model...")

    save_model(model, "models/ids_model.pkl")


if __name__ == "__main__":
    main()