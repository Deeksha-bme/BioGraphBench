import pandas as pd
import os
import io
import glob
from sklearn.metrics import f1_score

def evaluate():
    try:
        labels_raw = os.getenv("TEST_LABELS")
        csv_files = glob.glob("submissions/*.csv")
        
        if not labels_raw or not csv_files:
            with open("score.txt", "w") as f: f.write("0.0000")
            return

        # Load and strip whitespace from headers and values immediately
        truth_df = pd.read_csv(io.StringIO(labels_raw.strip())).rename(columns=lambda x: x.strip())
        sub_df = pd.read_csv(csv_files[0]).rename(columns=lambda x: x.strip())

        # Force column names to be exactly 'graph_index' and 'target'
        truth_df.columns = ['graph_index', 'target']
        sub_df.columns = ['graph_index', 'target']

        # Convert to numeric, handle errors, and force to INT
        for df in [truth_df, sub_df]:
            df['graph_index'] = pd.to_numeric(df['graph_index'], errors='coerce')
            df['target'] = pd.to_numeric(df['target'], errors='coerce')
            df.dropna(subset=['graph_index', 'target'], inplace=True)
            df['graph_index'] = df['graph_index'].astype(int)
            df['target'] = df['target'].astype(int)

        # Merge on graph_index - suffixes ensure we distinguish the two
        merged = pd.merge(truth_df, sub_df, on='graph_index', how='inner')
        
        if len(merged) < 4:
            # If we don't have 4 matches, we show the partial match count
            score = len(merged) / 4.0 
        else:
            # The real competition calculation
            score = f1_score(merged['target_x'], merged['target_y'], average='macro')
        
        with open("score.txt", "w") as f:
            f.write(f"{score:.4f}")
            
    except Exception as e:
        with open("score.txt", "w") as f: f.write("0.0000")

if __name__ == "__main__":
    evaluate()
