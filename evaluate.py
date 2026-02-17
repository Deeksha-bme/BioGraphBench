import pandas as pd
import os
import io
import glob
from sklearn.metrics import f1_score

def evaluate():
    try:
        labels_raw = os.getenv("TEST_LABELS", "").strip()
        csv_files = glob.glob("submissions/*.csv")
        
        if not labels_raw or not csv_files:
            with open("score.txt", "w") as f: f.write("0.0000")
            return

        # FORCE IGNORE HEADERS: This is the 0.2 fix.
        # We load without headers and skip the first line manually.
        truth_df = pd.read_csv(io.StringIO(labels_raw), header=None, skiprows=1)
        sub_df = pd.read_csv(csv_files[0], header=None, skiprows=1)

        # Rename columns to be sure
        truth_df.columns = ['idx', 'val']
        sub_df.columns = ['idx', 'val']

        # Clean everything to pure Integers
        for df in [truth_df, sub_df]:
            df['idx'] = pd.to_numeric(df['idx'], errors='coerce')
            df['val'] = pd.to_numeric(df['val'], errors='coerce')
            df.dropna(inplace=True)
            df['idx'] = df['idx'].astype(int)
            df['val'] = df['val'].astype(int)

        # Merge on the ID
        merged = pd.merge(truth_df, sub_df, on='idx', suffixes=('_true', '_pred'))
        
        # MATH CHECK:
        # If merged has 4 rows, and we are comparing 4 rows of data:
        if len(merged) == 0:
            score = 0.0000
        else:
            # Macro F1 on the 4 data points
            score = f1_score(merged['val_true'], merged['val_pred'], average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception as e:
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
