import pandas as pd
import os
import io
import glob
from sklearn.metrics import f1_score

def evaluate():
    try:
        # 1. Load Labels from Secret
        labels_raw = os.getenv("TEST_LABELS")
        if not labels_raw:
            print("❌ Secret TEST_LABELS not found!")
            return

        truth_df = pd.read_csv(io.StringIO(labels_raw))
        
        # 2. Find any CSV in the submissions folder
        submission_files = glob.glob("submissions/*.csv")
        if not submission_files:
            # If your file is .enc, pandas can't read it. It MUST be a .csv
            print("❌ No .csv file found in submissions/ folder!")
            exit(1)
            
        # Take the first CSV found
        sub_df = pd.read_csv(submission_files[0])
        
        # 3. Calculate Score
        # Ensure column names match your CSV (usually 'target')
        f1 = f1_score(truth_df['target'], sub_df['target'], average='macro')
        
        # 4. Save score
        with open("score.txt", "w") as f:
            f.write(f"{f1:.4f}")
            
        print(f"✅ Success! Evaluated {submission_files[0]} with score: {f1:.4f}")

    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

if __name__ == "__main__":
    evaluate()
