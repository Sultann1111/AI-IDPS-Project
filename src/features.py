# src/features.py
"""
Feature extraction from Zeek logs
"""

def extract_features(df):
    """
    Convert Zeek DataFrame to ML-ready features
    """
    features = pd.DataFrame()
    if df.empty:
        return features
    
    # Example features
    features['duration'] = df.get('duration', 0)
    features['orig_bytes'] = df.get('orig_bytes', 0)
    features['resp_bytes'] = df.get('resp_bytes', 0)
    return features