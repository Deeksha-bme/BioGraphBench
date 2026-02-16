import pandas as pd
import os
import io
from sklearn.metrics import f1_score

def evaluate():
    labels_raw = os.getenv("TEST_LABELS")
    if not labels_raw:
        print("❌ Secret TEST_LABELS not found!")
        return

    # 1. Load Truth Labels
    truth_df = pd.read_csv(io.StringIO(labels_raw))
    truth_values = truth_df['target'].values

    # 2. Load Submissions (Ensure files exist in /submissions)
    try:
        ideal_df = pd.read_csv("submissions/ideal.csv")
        pert_df = pd.read_csv("submissions/perturbed.csv")
        
        # 3. Calculate Macro F1
        f1_ideal = f1_score(truth_values, ideal_df['target'].values, average='macro')
        f1_pert = f1_score(truth_values, pert_df['target'].values, average='macro')
        
        # 4. Calculate Robustness Gap
        gap = abs(f1_ideal - f1_pert)
        
        # Save primary score (Ideal F1) for the leaderboard
        with open("score.txt", "w") as f:
            f.write(f"{f1_ideal:.4f}")
            
        print(f"✅ Success! Ideal: {f1_ideal:.4f}, Perturbed: {f1_pert:.4f}, Gap: {gap:.4f}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    evaluate()
