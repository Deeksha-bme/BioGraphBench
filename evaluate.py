import os
import glob
from sklearn.metrics import f1_score

def extract_raw_numbers(text):
    lines = text.strip().split('\n')
    targets = []

    # Skip header safely
    for line in lines[1:]:
        parts = line.strip().split(',')
        if len(parts) >= 2:
            try:
                targets.append(int(parts[1].strip()))
            except ValueError:
                pass

    return targets


def evaluate():
    try:
        # 1. Get labels from GitHub Secrets
        labels_raw = os.getenv("TEST_LABELS", "").strip()

        # 2. Find submission CSV
        csv_files = glob.glob("submissions/*.csv")

        if not labels_raw or not csv_files:
            with open("score.txt", "w") as f:
                f.write("0.0000")
            return

        # Extract true labels
        y_true = extract_raw_numbers(labels_raw)

        # Extract predictions
        with open(csv_files[0], 'r') as f:
            y_pred = extract_raw_numbers(f.read())
