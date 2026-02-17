import os
import glob
from sklearn.metrics import f1_score

def evaluate():
    try:
        # 1. Get labels from GitHub Secrets
        labels_raw = os.getenv("TEST_LABELS", "").strip()
        # 2. Find any CSV in the submissions folder
        csv_files = glob.glob("submissions/*.csv")
        
        if not labels_raw or not csv_files:
            with open("score.txt", "w") as f: f.write("0.0000")
            return

        # THIS IS THE KEY: We manually find the 1s and 0s
        def extract_raw_numbers(text):
            lines = text.strip().split('\n')
            targets = []
            for line in lines:
                parts = line.split(',')
                if len(parts) >= 2:
                    val = parts[1].strip()
                    # We ONLY keep the value if it's a number. 
                    # This skips the word "target" (the 0.2000 trap)
                    if val.isdigit():
                        targets.append(int(val))
            return targets

        y_true = extract_raw_numbers(labels_raw)
        
        with open(csv_files[0], 'r') as f:
            y_pred = extract_raw_numbers(f.read())

        # If we have exactly 4 values, we calculate the F1 score
        if len(y_true) == 4 and len(y_pred) == 4:
            score = f1_score(y_true, y_pred, average='macro')
        else:
            # If we match 0 data points, score is 0
            score = 0.0000
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception:
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
