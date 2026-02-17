import os
import glob

def evaluate():
    try:
        # Find your uploaded file
        csv_files = glob.glob("submissions/*.csv")
        if not csv_files:
            with open("score.txt", "w") as f: f.write("0.0000")
            return

        # The 'Truth' labels (Required for 1.0000)
        truth = [1, 0, 1, 1] 
        
        with open(csv_files[0], 'r') as f:
            lines = f.readlines()[1:] # Skip header
            preds = [int(line.split(',')[1].strip()) for line in lines if ',' in line]

        # Calculate matches
        if len(truth) == len(preds):
            matches = sum(1 for t, p in zip(truth, preds) if t == p)
            score = matches / len(truth)
        else:
            score = 0.0000 # Length mismatch

        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")

    except Exception:
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
