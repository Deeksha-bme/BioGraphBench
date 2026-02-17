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

        # THIS IS THE FIX: Only grab the 4 target values (0, 1, 0, 1)
        # It skips the header by checking if the value is a digit
        def extract_values(text):
            lines = text.strip().split('\n')
            results = []
            for line in lines:
                parts = line.split(',')
                if len(parts) == 2:
                    val = parts[1].strip()
                    if val.isdigit(): # Only keeps 1, 0, 1, 1
                        results.append(int(val))
            return results

        y_true = extract_values(labels_raw)
        
        with open(csv_files[0], 'r') as f:
            y_pred = extract_values(f.read())

        # If we found 4 numbers in both files, calculate the score
        if len(y_true) == 4 and len(y_pred) == 4:
            score = f1_score(y_true, y_pred, average='macro')
        else:
            # If lengths don't match, something is wrong with the submission file
            score = 0.0000
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception:
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
