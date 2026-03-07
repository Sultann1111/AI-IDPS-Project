import streamlit as st
import pandas as pd
import joblib
import os
from pcap_feature_extractor import extract_features_from_pcap

st.set_page_config(page_title="AI Intrusion Detection System", layout="wide")

st.title("AI-Powered Intrusion Detection System")

# -------------------------
# Load Model
# -------------------------

MODEL_PATH = os.path.join("models", "ids_model.pkl")

@st.cache_resource
def load_model():
    model = joblib.load(MODEL_PATH)
    return model

model = load_model()

# -------------------------
# PCAP Input
# -------------------------

DEFAULT_PCAP = "2026-02-28-traffic-analysis-exercise.pcap"

uploaded_file = st.file_uploader("Upload PCAP File", type=["pcap"])

if uploaded_file is None:

    st.info("No PCAP uploaded. Using default sample traffic.")

    pcap_path = DEFAULT_PCAP

else:

    with open("temp.pcap", "wb") as f:
        f.write(uploaded_file.read())

    pcap_path = "temp.pcap"

# -------------------------
# Feature Extraction
# -------------------------

df = extract_features_from_pcap(pcap_path)

st.subheader("Extracted Network Features")
st.dataframe(df.head())

# -------------------------
# Match Model Feature Size
# -------------------------

expected_features = 42
current_features = df.shape[1]

if current_features < expected_features:

    for i in range(expected_features - current_features):

        df[f"dummy_{i}"] = 0

# -------------------------
# Prediction
# -------------------------

probs = model.predict_proba(df)[:,1]

preds = []

for p in probs:

    if p > 0.6:
        preds.append(1)
    else:
        preds.append(0)

attack_count = sum(preds)
normal_count = len(preds) - attack_count

# -------------------------
# Threat Level Indicator
# -------------------------

attack_ratio = attack_count / len(preds)

if attack_ratio < 0.1:
    threat_level = "LOW"
    color = "green"

elif attack_ratio < 0.3:
    threat_level = "MEDIUM"
    color = "orange"

else:
    threat_level = "HIGH"
    color = "red"

st.subheader("Network Threat Level")

st.markdown(
    f"""
    <h2 style='color:{color};'>
    {threat_level} THREAT LEVEL
    </h2>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Dashboard Results
# -------------------------

st.subheader("Traffic Analysis Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Packets", len(preds))
col2.metric("Normal Traffic", normal_count)
col3.metric("Suspicious Traffic", attack_count)

# -------------------------
# Visualization
# -------------------------

summary_df = pd.DataFrame({

    "Traffic Type": ["Normal", "Attack"],
    "Count": [normal_count, attack_count]

})

st.subheader("Traffic Distribution")

st.bar_chart(summary_df.set_index("Traffic Type"))

# -------------------------
# Probability Distribution
# -------------------------

st.subheader("Attack Probability Distribution")

prob_df = pd.DataFrame({

    "Attack Probability": probs

})

st.line_chart(prob_df)

st.success("Detection Complete")