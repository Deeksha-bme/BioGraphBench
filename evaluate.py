import os
import glob
from sklearn.metrics import f1_score


def extract_raw_numbers(text):
    lines = text.strip().split("\n")
    targets = []

    for line in lines[1:]:  # skip header
        parts = line.strip().split(",")
        if len(parts) >= 2:
            try:
                targets.append(int(parts[1].strip()))
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

        y_true = extract_raw_numbers(labels_raw)

        with open(csv_files[0], "r") as f:
            y_pred = extract_raw_numbers(f.read())

        if len(y_true) == len(y_pred) and len(y_true) > 0:
            score = f1_score(y_true, y_pred, average="macro")
        else:
            score = 0.0

        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")

    except Exception:
        with open("score.txt", "w") as f:
            f.write("0.0000")


if __name__ == "__main__":
    evaluate()
