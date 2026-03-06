# src/parser.py
"""
Handles Zeek log parsing
"""

import pandas as pd
import os

def parse_conn_log(log_path):
    """
    Parse Zeek conn.log and return a pandas DataFrame
    """
    if not os.path.exists(log_path):
        print(f"File not found: {log_path}")
        return pd.DataFrame()
    
    df = pd.read_csv(log_path, sep='\t', comment='#')
    print(f"Parsed {len(df)} rows from {log_path}")
    return df