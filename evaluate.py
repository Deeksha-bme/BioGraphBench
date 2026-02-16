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

        # .strip() removes that hidden empty line 5
        truth_df = pd.read_csv(io.StringIO(labels_raw.strip())).dropna()
        sub_df = pd.read_csv(csv_files[0]).dropna()

        # FORCE everything to integer so '1' matches 1
        truth_df = truth_df.astype(int)
        sub_df = sub_df.astype(int)

        # Merge ensures we compare row 0 to row 0, row 1 to row 1
        merged = pd.merge(truth_df, sub_df, on='graph_index')
        
        # Calculate Macro F1
        score = f1_score(merged['target_x'], merged['target_y'], average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception as e:
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
