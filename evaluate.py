import pandas as pd
import os
import io
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def evaluate():
    if not os.path.exists("submissions"): return
    files = [f for f in os.listdir("submissions") if f.endswith('.enc')]
    if not files: return
    
    private_key_text = os.getenv("COMPETITION_PRIVATE_KEY")
    hidden_labels_text = os.getenv("TEST_LABELS")
    
    # Decrypting
    private_key = serialization.load_pem_private_key(private_key_text.encode(), password=None)
    with open(os.path.join("submissions", files[0]), "rb") as f:
        decrypted_data = private_key.decrypt(
            f.read(),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
    
    # Calculate Accuracy
    sub_df = pd.read_csv(io.StringIO(decrypted_data.decode())).reset_index(drop=True)
    truth_df = pd.read_csv(io.StringIO(hidden_labels_text)).reset_index(drop=True)
    accuracy = (sub_df['predicted_label'] == truth_df['label']).mean()
    
    # Write score for the next script to find
    with open("score.txt", "w") as f:
        f.write(str(accuracy))

if __name__ == "__main__":
    evaluate()
