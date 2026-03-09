"""
AI-Powered Intrusion Detection System Dashboard
"""

import streamlit as st
import pandas as pd
import joblib
import os
from pcap_feature_extractor import extract_features_from_pcap
from src.predict import predict_traffic

st.set_page_config(page_title="AI Intrusion Detection System", layout="wide")

st.title("🛡️ AI-Powered Intrusion Detection System")

# -------------------------
# Load Model (cached)
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

st.subheader("📡 Extracting Network Flows...")

with st.spinner("Reading PCAP and extracting features..."):
    df = extract_features_from_pcap(pcap_path)

if df.empty:
    st.error("No flows could be extracted from the PCAP file. Please check the file and try again.")
    st.stop()

st.subheader("Extracted Network Features")
st.dataframe(df.head(20))
st.caption(f"Total flows extracted: {len(df)}")

# -------------------------
# Prediction
# -------------------------

st.subheader("🔍 Running AI Detection...")

with st.spinner("Analysing traffic..."):
    results = predict_traffic(df, threshold=0.75)

if not results:
    st.error("Prediction returned no results.")
    st.stop()

probs = [r["attack_probability"] for r in results]
preds = [1 if r["prediction"] == "ATTACK" else 0 for r in results]

attack_count = sum(preds)
normal_count  = len(preds) - attack_count

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

st.subheader("🚨 Network Threat Level")

st.markdown(
    f"""
    <div style='padding:16px; border-radius:8px; background-color:#1e1e1e;'>
        <h2 style='color:{color}; margin:0;'>● {threat_level} THREAT LEVEL</h2>
        <p style='color:#aaa; margin:4px 0 0 0;'>{attack_ratio*100:.1f}% of flows flagged as suspicious</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# -------------------------
# Summary Metrics
# -------------------------

st.subheader("📊 Traffic Analysis Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Flows",        len(preds))
col2.metric("Normal Traffic",     normal_count)
col3.metric("Suspicious Traffic", attack_count)
col4.metric("Attack Ratio",       f"{attack_ratio*100:.1f}%")

# -------------------------
# Detailed Results Table
# -------------------------

st.subheader("🗂️ Flow-Level Detection Results")

results_df = pd.DataFrame(results)

# Colour code prediction column
def highlight_attacks(val):
    if val == "ATTACK":
        return "background-color: #ff4c4c; color: white; font-weight: bold"
    return "background-color: #4caf50; color: white;"

st.dataframe(
    results_df.style.applymap(highlight_attacks, subset=["prediction"]),
    use_container_width=True
)

# -------------------------
# Traffic Distribution Chart
# -------------------------

st.subheader("📈 Traffic Distribution")

summary_df = pd.DataFrame({
    "Traffic Type": ["Normal", "Attack"],
    "Count": [normal_count, attack_count]
})

st.bar_chart(summary_df.set_index("Traffic Type"))

# -------------------------
# Attack Probability Distribution
# -------------------------

st.subheader("📉 Attack Probability per Flow")

prob_df = pd.DataFrame({
    "Flow": list(range(1, len(probs) + 1)),
    "Attack Probability": probs
})

st.line_chart(prob_df.set_index("Flow"))

# -------------------------
# Top Suspicious Flows
# -------------------------

if attack_count > 0:
    st.subheader("⚠️ Top 10 Most Suspicious Flows")

    top_attacks = results_df[results_df["prediction"] == "ATTACK"] \
        .sort_values("attack_probability", ascending=False) \
        .head(10)

    st.dataframe(top_attacks, use_container_width=True)

# -------------------------
# Download Results
# -------------------------

st.subheader("💾 Export Results")

csv = results_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Detection Results as CSV",
    data=csv,
    file_name="ids_detection_results.csv",
    mime="text/csv"
)

st.success("✅ Detection Complete")