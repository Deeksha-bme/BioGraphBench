import pandas as pd
import sys

def main(pred_path, test_nodes_path):
    preds = pd.read_csv(pred_path)
    test_nodes = pd.read_csv(test_nodes_path)

    # Column check
    if "node_id" not in preds.columns or "predicted_label" not in preds.columns:
        raise ValueError("Submission must have columns: node_id, predicted_label")

    # Duplicate IDs
    if preds["node_id"].duplicated().any():
        raise ValueError("Duplicate node_ids found in submission")

    # NaN predictions
    if preds["predicted_label"].isna().any():
        raise ValueError("NaN values found in predictions")

    # Ensure integer labels
    if not preds["predicted_label"].apply(lambda x: isinstance(x,int)).all():
        raise ValueError("All predictions must be integer class labels")

    # IDs match test nodes
    if set(preds["node_id"]) != set(test_nodes["node_id"]):
        raise ValueError("Submission node_ids do not match test nodes")

    print("VALID SUBMISSION")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
