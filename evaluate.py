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
            print("❌ Missing labels or submission file.")
            with open("score.txt", "w") as f: f.write("0.0000")
            return

        truth_df = pd.read_csv(io.StringIO(labels_raw))
        sub_df = pd.read_csv(csv_files[0])

        # DEBUG: These prints show up in your GitHub Actions Log
        print("--- DEBUG INFO ---")
        print(f"Secret Head:\n{truth_df.head()}")
        print(f"Submission Head:\n{sub_df.head()}")
        
        # Ensure data types match (force them to be integers)
        truth_df['target'] = truth_df['target'].astype(int)
        sub_df['target'] = sub_df['target'].astype(int)

        score = f1_score(truth_df['target'], sub_df['target'], average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
        print(f"✅ Success! Calculated Score: {score:.4f}")

    except Exception as e:
        print(f"❌ Error: {e}")
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
