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

        # 1. Load ground truth from Secrets
        # .strip() handles the extra line 5 seen in your image
        truth_df = pd.read_csv(io.StringIO(labels_raw.strip()))
        
        # 2. Load the uploaded submission
        sub_df = pd.read_csv(csv_files[0])

        # 3. Clean and Cast: This ensures '1' (text) becomes 1 (number)
        # This is the secret to moving from 0.2000 to 1.0000
        truth_df = truth_df.dropna().astype(int)
        sub_df = sub_df.dropna().astype(int)

        # 4. Merge on graph_index to ensure rows align perfectly
        merged = pd.merge(truth_df, sub_df, on='graph_index', suffixes=('_true', '_pred'))
        
        # 5. Calculate Score
        if merged.empty:
            score = 0.0000
        else:
            score = f1_score(merged['target_true'], merged['target_pred'], average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception as e:
        print(f"Evaluation Error: {e}")
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
