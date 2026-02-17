import os
import glob
from sklearn.metrics import f1_score

def evaluate():
    try:
        labels_raw = os.getenv("TEST_LABELS", "").strip()
        csv_files = glob.glob("submissions/*.csv")
        
        if not labels_raw or not csv_files:
            with open("score.txt", "w") as f: f.write("0.0000")
            return

        # Helper function to get ONLY the targets (the second number in each line)
        def get_targets(text):
            lines = text.strip().split('\n')
            targets = []
            for line in lines:
                parts = line.split(',')
                # Only take it if it's a number (ignores the 'target' header)
                if len(parts) == 2 and parts[1].strip().isdigit():
                    targets.append(int(parts[1].strip()))
            return targets

        # Get targets from Secret and Submission
        y_true = get_targets(labels_raw)
        with open(csv_files[0], 'r') as f:
            y_pred = get_targets(f.read())

        # If we have 4 matches, calculate F1. If 0 matches, score is 0.
        if len(y_true) == len(y_pred) and len(y_true) > 0:
            score = f1_score(y_true, y_pred, average='macro')
        else:
            # This is a fallback if the lengths don't match
            score = 0.0000
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception:
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
