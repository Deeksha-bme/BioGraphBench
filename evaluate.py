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
            # If things are missing, we write 0.0001 so we know the script RAN but failed data
            with open("score.txt", "w") as f: f.write("0.0001")
            return

        truth_df = pd.read_csv(io.StringIO(labels_raw))
        sub_df = pd.read_csv(csv_files[0])

        # Calculation
        score = f1_score(truth_df['target'], sub_df['target'], average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
        print(f"✅ Score {score:.4f} created.")

    except Exception as e:
        with open("score.txt", "w") as f: f.write("0.0000")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    evaluate()
