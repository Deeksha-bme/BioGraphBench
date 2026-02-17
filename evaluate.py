import os
import glob
from sklearn.metrics import f1_score

def extract_labels(text):
    lines = text.strip().split("\n")
    data = []
    # Skip the header row (graph_index,target)
    for line in lines[1:]:
        parts = line.strip().split(",")
        if len(parts) >= 2:
            try:
                # Get the target value from the second column
                data.append(int(float(parts[1].strip())))
            except (ValueError, IndexError):
                continue
    return data

def evaluate():
    try:
        # 1. Pull the truth from your Secrets
        labels_raw = os.getenv("TEST_LABELS", "").strip()
        # 2. Find your submitted file
        csv_files = glob.glob("submissions/*.csv")

        if not labels_raw or not csv_files:
            print("Error: Missing Secret or Submission File")
            with open("score.txt", "w") as f: f.write("0.0000")
            return

        y_true = extract_labels(labels_raw)
        with open(csv_files[0], "r") as f:
            y_pred = extract_labels(f.read())

        # 3. Compare lengths (Must be 4 for your test set)
        if len(y_true) == len(y_pred) and len(y_true) > 0:
            score = f1_score(y_true, y_pred, average="macro")
            print(f"Success! Score: {score}")
        else:
            print(f"Mismatch: Truth has {len(y_true)} rows, Submission has {len(y_pred)}")
            score = 0.0000

        # 4. Save the score for the workflow to read
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")

    except Exception as e:
        print(f"Script Error: {e}")
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
