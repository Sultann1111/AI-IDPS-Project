"""
Model evaluation module
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_curve,
    roc_auc_score
)


def evaluate_model(model, X_test, y_test, feature_names):

    os.makedirs("results", exist_ok=True)

    y_prob = model.predict_proba(X_test)[:, 1]

    thresholds = np.arange(0.40, 0.80, 0.05)

    best_threshold = 0
    best_accuracy = 0

    print("\nThreshold Evaluation Results:\n")

    for t in thresholds:

        y_pred = (y_prob >= t).astype(int)

        acc = accuracy_score(y_test, y_pred)

        print(f"Threshold: {t:.2f} | Accuracy: {acc:.4f}")

        if acc > best_accuracy:
            best_accuracy = acc
            best_threshold = t

    print("\nBest Threshold Found:", best_threshold)
    print("Best Accuracy:", best_accuracy)

    y_pred = (y_prob >= best_threshold).astype(int)

    print("\nFinal Classification Report:\n")
    print(classification_report(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred)

    print("\nFinal Confusion Matrix:\n")
    print(cm)

    # Confusion Matrix Plot
    plt.figure(figsize=(6,6))
    plt.imshow(cm)
    plt.title("Confusion Matrix")
    plt.colorbar()
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.savefig("results/confusion_matrix.png")
    plt.close()

    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_prob)

    auc_score = roc_auc_score(y_test, y_prob)

    print("\nAUC Score:", auc_score)

    plt.figure(figsize=(8,6))
    plt.plot(fpr, tpr, label=f"AUC = {auc_score:.3f}")
    plt.plot([0,1],[0,1],'--')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend()

    plt.savefig("results/roc_curve.png")
    plt.close()

    # Feature Importance
    importances = model.feature_importances_

    indices = np.argsort(importances)[::-1][:15]

    plt.figure(figsize=(10,6))

    plt.bar(range(len(indices)), importances[indices])

    plt.xticks(range(len(indices)), [feature_names[i] for i in indices], rotation=90)

    plt.title("Top 15 Important Features")

    plt.tight_layout()

    plt.savefig("results/feature_importance.png")

    plt.close()

    return best_threshold, best_accuracy