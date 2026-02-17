import os
import glob
from sklearn.metrics import f1_score

def evaluate():
    try:
        # 1. Get labels from GitHub Secrets
        labels_raw = os.getenv("TEST_LABELS", "").strip()
        # 2. Find the submission file
        csv_files = glob.glob("submissions/*.csv")
        
        if not labels_raw or not csv_files:
            with open("score.txt", "w") as f: f.write("0.0000")
            return

        # Helper to extract ONLY numbers (skips text like 'target')
        def get_numbers(text):
            nums = []
            for line in text.strip().split('\n'):
                parts = [p.strip() for p in line.split(',')]
                # Only keep if the second part is a digit
                # This is the "secret sauce" that ignores the header
                if len(parts) >= 2 and parts[1].isdigit():
                    nums.append(int(parts[1]))
            return nums

        y_true = get_numbers(labels_raw)
        with open(csv_files[0], 'r') as f:
            y_pred = get_numbers(f.read())

        # CRITICAL: We only calculate if we found exactly 4 data points
        if len(y_true) == 4 and len(y_pred) == 4:
            # This is the real competition score
            score = f1_score(y_true, y_pred, average='macro')
        else:
            # If we don't find 4 numbers, the file format is wrong
            score = 0.0000
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception:
        # Safety fallback
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
