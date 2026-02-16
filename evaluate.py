import pandas as pd
import os
import io
import glob
from sklearn.metrics import f1_score

def evaluate():
    try:
        # Load Secret
        labels_raw = os.getenv("TEST_LABELS")
        if not labels_raw:
            print("❌ Secret TEST_LABELS is missing!")
            return

        # Load Submission
        csv_files = glob.glob("submissions/*.csv")
        if not csv_files:
            print("❌ No CSV found in submissions/ folder!")
            return
        
        truth_df = pd.read_csv(io.StringIO(labels_raw))
        sub_df = pd.read_csv(csv_files[0])
        
        # --- DEBUG INFO ---
        print(f"Secret Rows: {len(truth_df)}")
        print(f"Submission Rows: {len(sub_df)}")
        # ------------------

        # Check for matching length before calculating
        if len(truth_df) != len(sub_df):
            print(f"❌ MATCH ERROR: Secret has {len(truth_df)} rows, but Submission has {len(sub_df)} rows.")
            exit(1)

        # Calculate Score
        score = f1_score(truth_df['target'], sub_df['target'], average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
        print(f"✅ Success! F1 Score: {score:.4f}")

    except Exception as e:
        print(f"❌ Python Error: {e}")
        exit(1)

if __name__ == "__main__":
    evaluate()
