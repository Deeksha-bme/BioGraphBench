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

        # 1. Load the data, specifically telling it to skip any weird empty rows
        # header=0 tells it the first row is names, not data
        truth_df = pd.read_csv(io.StringIO(labels_raw), header=0).dropna()
        sub_df = pd.read_csv(csv_files[0], header=0).dropna()

        # 2. Force conversion to ensure we aren't comparing "1" (text) to 1 (number)
        # We rename columns just in case the submission uses different names
        truth_df.columns = ['idx', 'val']
        sub_df.columns = ['idx', 'val']

        for df in [truth_df, sub_df]:
            df['idx'] = pd.to_numeric(df['idx'], errors='coerce')
            df['val'] = pd.to_numeric(df['val'], errors='coerce')
            df.dropna(inplace=True)
            df['idx'] = df['idx'].astype(int)
            df['val'] = df['val'].astype(int)

       # 3. Use a merge to find where the indices match perfectly
        # suffixes help us identify which 'val' is which
        merged = pd.merge(truth_df, sub_df, on='idx', suffixes=('_true', '_pred'))
        
        # 4. Calculate Score
        if len(merged) == 0:
            score = 0.0000
        else:
            # Explicitly call the columns by name to avoid indexing errors
            score = f1_score(merged['val_true'], merged['val_pred'], average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception as e:
        # If anything crashes, we write 0.0000 so the leaderboard doesn't break
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
