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

        # Load Truth and Submission
        truth_df = pd.read_csv(io.StringIO(labels_raw.strip()))
        sub_df = pd.read_csv(csv_files[0])

        # CLEANING: This is vital for any number of rows
        # It removes empty lines and ensures numbers are treated as numbers
        truth_df = truth_df.apply(pd.to_numeric, errors='coerce').dropna().astype(int)
        sub_df = sub_df.apply(pd.to_numeric, errors='coerce').dropna().astype(int)

        # Ensure column names match
        truth_df.columns = ['graph_index', 'target']
        sub_df.columns = ['graph_index', 'target']

        # MERGE: This automatically scales to however many rows you have
        merged = pd.merge(truth_df, sub_df, on='graph_index', suffixes=('_true', '_pred'))
        
        if len(merged) == 0:
            score = 0.0000
        else:
            # Macro F1 handles multiple classes and large datasets perfectly
            score = f1_score(merged['target_true'], merged['target_pred'], average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception as e:
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
