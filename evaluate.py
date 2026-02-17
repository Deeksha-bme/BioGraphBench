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

        truth_df = pd.read_csv(io.StringIO(labels_raw.strip()))
        sub_df = pd.read_csv(csv_files[0])

        # Convert to integers to ensure '1' == 1
        truth_df = truth_df.apply(pd.to_numeric, errors='coerce').dropna().astype(int)
        sub_df = sub_df.apply(pd.to_numeric, errors='coerce').dropna().astype(int)

        # Merge on graph_index
        merged = pd.merge(truth_df, sub_df, on='graph_index')
        
        if len(merged) == 0:
            score = 0.0000
        else:
            # Calculate F1 score
            score = f1_score(merged.iloc[:, 1], merged.iloc[:, 2], average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception as e:
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
