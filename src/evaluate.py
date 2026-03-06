# src/evaluate.py
"""
Evaluation module for AI Intrusion Detection System.
Generates classification metrics, ROC curve, confusion matrix, and feature importance plots.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_curve,
    auc,
)

def evaluate_model(model, X_test, y_test, feature_names):
    print("\nEvaluating model performance...")

    # Model predictions
    y_probs = model.predict_proba(X_test)[:, 1]

    # Threshold tuning
    thresholds = np.arange(0.4, 0.76, 0.05)
    best_accuracy = 0
    best_threshold = 0.5

    for thresh in thresholds:
        y_pred = (y_probs >= thresh).astype(int)
        acc = np.mean(y_pred == y_test)
        print(f"Threshold: {thresh:.2f} | Accuracy: {acc:.4f}")
        if acc > best_accuracy:
            best_accuracy = acc
            best_threshold = thresh

    print(f"\nBest Threshold Found: {best_threshold}")
    print(f"Best Accuracy: {best_accuracy}")

    # Final predictions using best threshold
    y_pred_final = (y_probs >= best_threshold).astype(int)

    # Classification report
    print("\nFinal Classification Report:\n")
    print(classification_report(y_test, y_pred_final))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred_final)
    print("Final Confusion Matrix:\n")
    print(cm)

    # AUC score
    fpr, tpr, _ = roc_curve(y_test, y_probs)
    auc_score = auc(fpr, tpr)
    print(f"\nAUC Score: {auc_score:.4f}")

    # Ensure results directory exists
    os.makedirs("results", exist_ok=True)

    # ---------------- ROC Curve ----------------
    plt.figure(figsize=(8,6))
    plt.plot(fpr, tpr, label=f"AUC = {auc_score:.3f}")
    plt.plot([0,1], [0,1], '--', color='gray')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve - AI Intrusion Detection System")
    plt.legend(loc="lower right")
    roc_path = "results/roc_curve.png"
    plt.savefig(roc_path)
    plt.close()
    print(f"ROC Curve saved to: {roc_path}")

    # ---------------- Confusion Matrix ----------------
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    cm_path = "results/confusion_matrix.png"
    plt.savefig(cm_path)
    plt.close()
    print(f"Confusion Matrix saved to: {cm_path}")

    # ---------------- Feature Importance ----------------
    if hasattr(model, "feature_importances_"):
        importance = model.feature_importances_
        sorted_idx = np.argsort(importance)[::-1]
        plt.figure(figsize=(10,6))
        plt.bar(
            [feature_names[i] for i in sorted_idx],
            importance[sorted_idx]
        )
        plt.xticks(rotation=90)
        plt.title("Feature Importance")
        plt.tight_layout()
        fi_path = "results/feature_importance.png"
        plt.savefig(fi_path)
        plt.close()
        print(f"Feature Importance saved to: {fi_path}")

    return best_threshold, best_accuracy, auc_score