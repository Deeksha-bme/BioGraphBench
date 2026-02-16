import pandas as pd
import os
import io

def evaluate():
    # 1. Get Secret Data
    labels_raw = os.getenv("TEST_LABELS")
    if not labels_raw:
        print("Error: TEST_LABELS secret is empty")
        return

    # Load truth labels
    truth_df = pd.read_csv(io.StringIO(labels_raw))
    truth_values = truth_df['target'].values # Matches your "target" column name

    # 2. Look for the two submission files
    # Expecting: submissions/ideal.csv and submissions/perturbed.csv
    ideal_path = "submissions/ideal.csv"
    perturbed_path = "submissions/perturbed.csv"

    try:
        ideal_df = pd.read_csv(ideal_path)
        pert_df = pd.read_csv(perturbed_path)
        
        # Calculate F1 or Accuracy (using your .values fix from yesterday!)
        acc_ideal = (ideal_df['target'].values == truth_values).mean()
        acc_pert = (pert_df['target'].values == truth_values).mean()
        
        # Robustness Gap
        gap = abs(acc_ideal - acc_pert)
        
        # Final Score (Example: Average of both)
        final_score = (acc_ideal + acc_pert) / 2

        # Save to score.txt for the renderer
        with open("score.txt", "w") as f:
            f.write(f"{final_score:.4f}")
            
        print(f"Scoring Complete: Ideal={acc_ideal}, Perturbed={acc_pert}, Gap={gap}")

    except Exception as e:
        print(f"Error during scoring: {e}")

if __name__ == "__main__":
    evaluate()
