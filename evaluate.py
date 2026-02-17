import os
import glob
from sklearn.metrics import f1_score

def evaluate():
    try:
        # Get labels from GitHub Secrets
        labels_raw = os.getenv("TEST_LABELS", "").strip()
        csv_files = glob.glob("submissions/*.csv")
        
        if not labels_raw or not csv_files:
            with open("score.txt", "w") as f: f.write("0.0000")
            return

        def get_only_numbers(text):
            data = []
            # Split into lines and look at each one
            for line in text.strip().split('\n'):
                # Clean the line and split by comma
                parts = [p.strip() for p in line.split(',')]
                # IF the second part is a number, we keep it. 
                # This AUTOMATICALLY skips the word "target"
                if len(parts) >= 2 and parts[1].isdigit():
                    data.append(int(parts[1]))
            return data

        # Extract just the 1s and 0s
        y_true = get_only_numbers(labels_raw)
        
        with open(csv_files[0], 'r') as f:
            y_pred = get_only_numbers(f.read())

        # Check: Do we have exactly 4 numbers to compare?
        if len(y_true) == 4 and len(y_pred) == 4:
            score = f1_score(y_true, y_pred, average='macro')
        else:
            # This triggers if your submission doesn't have 4 rows of data
            score = 0.0000
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception:
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
