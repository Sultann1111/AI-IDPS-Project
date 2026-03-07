"""
Explainability module using SHAP
"""

import os
import shap
import matplotlib.pyplot as plt


def explain_model(model, X_test, feature_names):

    os.makedirs("results", exist_ok=True)

    sample = X_test.sample(500, random_state=42)

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(sample)

    plt.figure()

    shap.summary_plot(
        shap_values,
        sample,
        feature_names=feature_names,
        show=False
    )

    plt.savefig("results/shap_summary.png")

    plt.close()

    print("SHAP summary plot saved to results/shap_summary.png")