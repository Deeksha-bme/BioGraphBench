import os
import glob
from sklearn.metrics import f1_score

def extract_raw_numbers(text):
    lines = text.strip().split("\n")
    targets = []
    # line[1:] skips the header row
    for line in lines[1:]:  
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 2:
            try:
                # Convert to float then int handles cases like "1.0"
                val = int(float(parts[1]))
                targets.append(val)
            except (ValueError, IndexError):
                continue
    return targets

def evaluate():
    try:
        labels_raw = os.getenv("TEST_LABELS", "").strip()
        csv_files = glob.glob("submissions/*.csv")

        if not labels_raw or not csv_files:
            print("Missing labels or submission file!")
            with open("score.txt", "w") as f: f.write("0.0000")
            return

        y_true = extract_raw_numbers(labels_raw)
        
        with open(csv_files[0], "r") as f:
            y_pred = extract_raw_numbers(f.read())

        print(f"DEBUG: True values found: {len(y_true)}")
        print(f"DEBUG: Pred values found: {len(y_pred)}")

        # If lengths match (should be 4), calculate F1
        if len(y_true) == len(y_pred) and len(y_true) > 0:
            score = f1_score(y_true, y_pred, average="macro")
        else:
            # If they don't match, we force a 0.0000 to show there is a format error
            print("Length mismatch! Check your CSV headers and rows.")
            score = 0.0000

        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")

    except Exception as e:
        print(f"Critical Error: {e}")
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
