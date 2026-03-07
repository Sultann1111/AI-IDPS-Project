📝 Overview

The AI-IDS is a Python-based intrusion detection system that processes PCAP network traffic and detects suspicious behavior using machine learning. It provides an interactive Streamlit dashboard for easy visualization.

⚠️ Note: Zeek (Bro) could not be used due to dependency conflicts on Kali Linux (missing BIND, libc version issues). I replaced Zeek with Scapy for packet parsing, ensuring full pipeline functionality.

⚙️ Features

PCAP Analysis: Supports custom PCAP file uploads

ML-based Detection: LightGBM model classifies traffic as NORMAL or SUSPICIOUS

Interactive Dashboard: Visualizes packet summaries, attack probability, and counts

Automated Pipeline: Upload → Extract → Predict → Visualize

🏗️ Project Structure
AI_IDPS_Project/
│
├── dashboard.py                 # Streamlit dashboard
├── pcap_ids.py                  # ML inference pipeline
├── pcap_feature_extractor.py    # Packet parsing & feature extraction
├── models/
│   ├── ids_model.pkl            # LightGBM IDS model
│   └── igbm_model.pkl           # Optional additional model
├── sample_pcaps/
│   └── 2026-02-28-traffic-analysis-exercise.pcap
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
🖥️ Screenshots
<details> <summary>Click to expand dashboard screenshots</summary>
Default/Uploading PCAP file


![alt text](image.png)

Predictions and attack probabilities

![alt text](image.png)

</details>


💻 Installation
<details> <summary>Step-by-step instructions</summary>
1️⃣ Clone Repository
git clone https://github.com/yourusername/AI_IDPS_Project.git
cd AI_IDPS_Project
2️⃣ Create Virtual Environment
python -m venv venv

Activate:

Windows: venv\Scripts\activate

Linux/macOS: source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

Dependencies include:

streamlit

scapy

pandas & numpy

lightgbm

joblib

</details>
▶️ Running the Dashboard
streamlit run dashboard.py

Opens a browser interface

Upload your PCAP file or use the sample

Visualize predictions, packet counts, and attack probabilities

🧩 How AI-IDS Works
<details> <summary>Click to expand system workflow</summary>

+---------------------+
|  Network Traffic    |  (PCAP files)
+---------------------+
          |
          v
+---------------------+
| Feature Extraction  |  (Scapy)
+---------------------+
          |
          v
+---------------------+
| Machine Learning    |  (LightGBM)
+---------------------+
          |
          v
+---------------------+
| Prediction & Output |
+---------------------+
          |
          v
+---------------------+
| Streamlit Dashboard |
+---------------------+

Scapy: Reads packets, extracts protocol, size, flags, and other features

LightGBM: Classifies traffic and calculates attack probability

Streamlit: Provides interactive visualization

</details>
⚠️ Why Zeek Was Not Used
<details> <summary>Click to expand</summary>

Zeek 6.0.0 requires strict dependencies (BIND library, libc < 2.38)

Attempting to install on Kali Linux resulted in:

Missing prerequisites

Compilation errors

Dependency conflicts

Solution:

Replaced Zeek with Scapy for packet parsing

Fully compatible with Python ML pipeline

Allows extracting all necessary features for LightGBM prediction

</details>
🔬 Machine Learning Model

Type: LightGBM classifier

Input: Extracted features from PCAPs

Output: NORMAL or SUSPICIOUS + probability

Handling Missing Features: Automatically padded to match model input


</details>
🚀 Future Enhancements

Real-time network capture

Additional ML features for higher detection accuracy

Cloud deployment for live monitoring

Reintroduce Zeek or Suricata when dependencies allow

📜 License

For educational and research purposes only

🙏 Acknowledgements

Research in ML for cybersecurity

Open-source projects: Scapy, LightGBM, Streamlit

Academic references on network intrusion detection