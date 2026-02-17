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

        # 1. Load data but SKIP the header row entirely
        # This prevents the "0.2000" (1/5) header-match trap
        truth_df = pd.read_csv(io.StringIO(labels_raw), header=None, skiprows=1)
        sub_df = pd.read_csv(csv_files[0], header=None, skiprows=1)

        # 2. Assign standard column names
        truth_df.columns = ['idx', 'val']
        sub_df.columns = ['idx', 'val']

        # 3. Force clean integers (this is the most important part)
        for df in [truth_df, sub_df]:
            df['idx'] = pd.to_numeric(df['idx'], errors='coerce')
            df['val'] = pd.to_numeric(df['val'], errors='coerce')
            df.dropna(inplace=True)
            df['idx'] = df['idx'].astype(int)
            df['val'] = df['val'].astype(int)

        # 4. Merge on the index
        merged = pd.merge(truth_df, sub_df, on='idx', suffixes=('_true', '_pred'))
        
        # 5. Calculate Score based ONLY on the 4 data points
        if len(merged) == 0:
            score = 0.0000
        else:
            # Macro F1 comparing only the data, not the headers
            score = f1_score(merged['val_true'], merged['val_pred'], average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception as e:
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
