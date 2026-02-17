import os
import glob

def get_data(text):
    # Extracts second column numbers, skipping the header
    lines = text.strip().split('\n')
    return [int(line.split(',')[1].strip()) for line in lines if line and line.split(',')[1].strip().isdigit()]

def evaluate():
    try:
        labels_raw = os.getenv("TEST_LABELS", "").strip()
        csv_files = glob.glob("submissions/*.csv")
        
        if not labels_raw or not csv_files:
            with open("score.txt", "w") as f: f.write("0.0000")
            return

        y_true = get_data(labels_raw)
        with open(csv_files[0], 'r') as f:
            y_pred = get_data(f.read())

        if len(y_true) == len(y_pred) and len(y_true) > 0:
            # Manual Accuracy Calculation (Since you want 1.0000)
            correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
            score = correct / len(y_true)
        else:
            score = 0.0000
            
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
    except Exception as e:
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
