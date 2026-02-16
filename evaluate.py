import pandas as pd
import os
import io
import glob
from sklearn.metrics import f1_score

def evaluate():
    try:
        labels_raw = os.getenv("TEST_LABELS")
        csv_files = glob.glob("submissions/*.csv")
        
        if not labels_raw or not csv_files:
            with open("score.txt", "w") as f: f.write("0.0000")
            return

        # Load and clean data
        truth_df = pd.read_csv(io.StringIO(labels_raw.strip())).dropna()
        sub_df = pd.read_csv(csv_files[0]).dropna()

        # Force everything to integer to prevent 0.2000 errors
        truth_df['graph_index'] = truth_df['graph_index'].astype(int)
        truth_df['target'] = truth_df['target'].astype(int)
        sub_df['graph_index'] = sub_df['graph_index'].astype(int)
        sub_df['target'] = sub_df['target'].astype(int)

        # Merge on index to ensure we are comparing the right rows
        merged = pd.merge(truth_df, sub_df, on='graph_index', how='inner')
        
        # Calculate Simple Accuracy first to test, then F1
        score = f1_score(merged['target_x'], merged['target_y'], average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception as e:
        with open("score.txt", "w") as f: f.write("0.0000")
