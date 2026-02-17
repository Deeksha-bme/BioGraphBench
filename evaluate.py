import os
import glob
from sklearn.metrics import f1_score

def extract_raw_numbers(text):
    lines = text.strip().split("\n")
    targets = []
    # Skip header
    for line in lines[1:]:  
        parts = line.strip().split(",")
        if len(parts) >= 2:
            try:
                # Get the second column (the label)
                targets.append(int(float(parts[1].strip())))
            except ValueError:
                pass
    return targets

def evaluate():
    try:
        labels_raw = os.getenv("TEST_LABELS", "").strip()
        csv_files = glob.glob("submissions/*.csv")

        if not labels_raw or not csv_files:
            with open("score.txt", "w") as f:
                f.write("0.0000")
            return

        # --- ALL THIS MUST BE INDENTED ---
        y_true = extract_raw_numbers(labels_raw)
        
        print(f"CSV files found: {csv_files}")

        with open(csv_files[0], "r") as f:
            content = f.read()
            print(f"Reading file: {csv_files[0]}")
            y_pred = extract_raw_numbers(content)

        print(f"y_true: {y_true}")
        print(f"y_pred: {y_pred}")

        if len(y_true) == len(y_pred) and len(y_true) > 0:
            score = f1_score(y_true, y_pred, average="macro")
        else:
            # If lengths don't match, this is why you get 0
            print(f"Mismatch! True len: {len(y_true)}, Pred len: {len(y_pred)}")
            score = 0.0

        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")

    except Exception as e:
        print(f"Error occurred: {e}")
        with open("score.txt", "w") as f:
            f.write("0.0000")

if __name__ == "__main__":
    evaluate()
