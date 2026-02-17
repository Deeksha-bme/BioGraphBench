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

        # Use skip_blank_lines=True to ignore those pesky empty rows
        truth_df = pd.read_csv(io.StringIO(labels_raw.strip()), skip_blank_lines=True)
        sub_df = pd.read_csv(csv_files[0], skip_blank_lines=True)

        # Force to numeric and drop any rows that failed to convert
        truth_df = truth_df.apply(pd.to_numeric, errors='coerce').dropna().astype(int)
        sub_df = sub_df.apply(pd.to_numeric, errors='coerce').dropna().astype(int)

        # Ensure column names match
        truth_df.columns = ['graph_index', 'target']
        sub_df.columns = ['graph_index', 'target']

        merged = pd.merge(truth_df, sub_df, on='graph_index', suffixes=('_true', '_pred'))
        
        if len(merged) == 0:
            score = 0.0000
        else:
            score = f1_score(merged['target_true'], merged['target_pred'], average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception as e:
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
