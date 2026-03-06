# src/explain.py

import shap


def explain_model(model, X_sample):

    print("Generating SHAP explainability...")

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(X_sample)

    shap.summary_plot(shap_values, X_sample)