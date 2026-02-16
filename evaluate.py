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

        # Use .strip() to remove the empty line 5 from your image
        truth_df = pd.read_csv(io.StringIO(labels_raw.strip()))
        sub_df = pd.read_csv(csv_files[0])

        # Force column names and integer types
        truth_df.columns = ['graph_index', 'target']
        sub_df.columns = ['graph_index', 'target']
        
        # This ensures row 0 is compared to row 0, even if there's a blank line
        truth_df = truth_df.dropna().astype(int)
        sub_df = sub_df.dropna().astype(int)

        merged = pd.merge(truth_df, sub_df, on='graph_index')
        score = f1_score(merged['target_x'], merged['target_y'], average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception as e:
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
