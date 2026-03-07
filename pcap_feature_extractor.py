# Minimal extractor: returns a dummy DataFrame with 42 features
import pandas as pd
import numpy as np

def extract_features_from_pcap(pcap_file):
    # Dummy implementation: returns random features
    num_packets = 20  # example
    features = np.random.rand(num_packets, 42)
    df = pd.DataFrame(features, columns=[f"f{i}" for i in range(42)])
    return df