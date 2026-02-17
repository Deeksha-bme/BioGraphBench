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

        # Load ground truth and submission
        truth_df = pd.read_csv(io.StringIO(labels_raw.strip()))
        sub_df = pd.read_csv(csv_files[0])

        # THE CRITICAL FIX: Convert both columns to numeric integers
        # This ensures '1' (text) is treated exactly like 1 (number)
        for df in [truth_df, sub_df]:
            df.columns = ['graph_index', 'target'] # Force column names to match
            df['graph_index'] = pd.to_numeric(df['graph_index'], errors='coerce')
            df['target'] = pd.to_numeric(df['target'], errors='coerce')
            df.dropna(inplace=True)
            df['graph_index'] = df['graph_index'].astype(int)
            df['target'] = df['target'].astype(int)

        # Merge ensures we only compare rows with matching graph_index
        merged = pd.merge(truth_df, sub_df, on='graph_index', suffixes=('_true', '_pred'))
        
        if len(merged) == 0:
            score = 0.0000
        else:
            # Calculate Macro F1
            score = f1_score(merged['target_true'], merged['target_pred'], average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception as e:
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
