import pandas as pd
import os
import io
import glob
from sklearn.metrics import f1_score

def evaluate():
    try:
        labels_raw = os.getenv("TEST_LABELS", "")
        csv_files = glob.glob("submissions/*.csv")
        
        if not labels_raw or not csv_files:
            with open("score.txt", "w") as f: f.write("0.0000")
            return

        # Helper to clean and convert to dict {index: target}
        def get_clean_map(content):
            data_map = {}
            lines = content.strip().split('\n')
            for line in lines:
                parts = line.replace(',', ' ').split()
                if len(parts) >= 2:
                    try:
                        # Strip all hidden chars and force to int
                        idx = int("".join(filter(str.isdigit, parts[0])))
                        val = int("".join(filter(str.isdigit, parts[1])))
                        data_map[idx] = val
                    except: continue
            return data_map

        # Parse Truth
        truth_map = get_clean_map(labels_raw)
        
        # Parse Submission
        with open(csv_files[0], 'r') as f:
            sub_map = get_clean_map(f.read())

        # Compare
        y_true = []
        y_pred = []
        for idx in truth_map:
            if idx in sub_map:
                y_true.append(truth_map[idx])
                y_pred.append(sub_map[idx])

        if len(y_true) < 4:
            # If we still match less than 4, it's a mapping error
            score = len(y_true) / 5.0 
        else:
            score = f1_score(y_true, y_pred, average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception as e:
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
