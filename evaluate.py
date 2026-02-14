import pandas as pd

# Paths
submission_path = "submission.csv"        # participant submission
hidden_labels_path = "hidden_labels.csv"  # your internal test labels

# Load CSVs
submission = pd.read_csv(submission_path)
hidden_labels = pd.read_csv(hidden_labels_path)

# Compute accuracy
accuracy = (submission['predicted_label'] == hidden_labels['label']).mean()
print(f"Test Accuracy: {accuracy:.4f}")
