import pandas as pd
import os
import io
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def evaluate():
    # 1. Locate the submission
    submission_folder = "submissions"
    if not os.path.exists(submission_folder):
        print("❌ Submissions folder not found!")
        return

    files = [f for f in os.listdir(submission_folder) if f.endswith('.enc')]
    if not files:
        print("❌ No encrypted (.enc) file found in submissions/ folder.")
        return
    
    encrypted_path = os.path.join(submission_folder, files[0])

    # 2. Grab your Secret Key from GitHub Vault
    private_key_text = os.getenv("COMPETITION_PRIVATE_KEY")
    if not private_key_text:
        print("❌ Error: COMPETITION_PRIVATE_KEY secret is missing!")
        return

    # 3. Unlock the file
    private_key = serialization.load_pem_private_key(private_key_text.encode(), password=None)
    with open(encrypted_path, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    # 4. Load DataFrames
    submission = pd.read_csv(io.StringIO(decrypted_data.decode()))
    
    # Grab the hidden answers from your other Secret
    hidden_labels_text = os.getenv("TEST_LABELS")
    if not hidden_labels_text:
        print("❌ Error: TEST_LABELS secret is missing!")
        return
    hidden_labels = pd.read_csv(io.StringIO(hidden_labels_text))

    # 5. Calculate Accuracy
    accuracy = (submission['predicted_label'] == hidden_labels['label']).mean()
    print(f"✅ SCORE_SUCCESS: {accuracy:.4f}")
    
    # Save score to a file so the leaderboard script can read it
    with open("score.txt", "w") as f:
        f.write(str(accuracy))

if __name__ == "__main__":
    evaluate()
