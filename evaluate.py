import os
import glob

def evaluate():
    try:
        # Find the file you uploaded
        csv_files = glob.glob("submissions/*.csv")
        
        if not csv_files:
            print("No file found in submissions/ folder!")
            with open("score.txt", "w") as f: f.write("0.0000")
            return

        # The 'Truth' labels for your 4 test rows
        truth = [1, 0, 1, 1] 
        
        with open(csv_files[0], 'r') as f:
            lines = f.readlines()
            # This logic finds the 'target' column even if you add extra spaces
            preds = []
            for line in lines[1:]: # Skip the header row
                if ',' in line:
                    val = line.split(',')[1].strip()
                    if val.isdigit():
                        preds.append(int(val))

        # Check if the number of rows matches
        if len(truth) == len(preds):
            matches = sum(1 for t, p in zip(truth, preds) if t == p)
            score = matches / len(truth)
        else:
            print(f"Row mismatch: Expected 4, got {len(preds)}")
            score = 0.0000

        # Save the result for the GitHub Action to see
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
        print(f"Calculated Score: {score}")

    except Exception as e:
        print(f"Error: {e}")
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
