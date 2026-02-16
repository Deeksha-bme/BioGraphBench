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

        # Load data
        truth_df = pd.read_csv(io.StringIO(labels_raw))
        sub_df = pd.read_csv(csv_files[0])

        # Align by graph_index to ensure we compare the right rows
        merged = pd.merge(truth_df, sub_df, on='graph_index', suffixes=('_true', '_pred'))
        
        if merged.empty:
            score = 0.0
        else:
            score = f1_score(merged['target_true'].astype(int), 
                             merged['target_pred'].astype(int), 
                             average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception as e:
        print(f"Error: {e}")
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
