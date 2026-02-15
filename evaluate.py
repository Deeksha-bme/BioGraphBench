import pandas as pd
import os
import io
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def evaluate():
    submission_folder = "submissions"
    files = [f for f in os.listdir(submission_folder) if f.endswith('.enc')]
    if not files:
        return
    
    encrypted_path = os.path.join(submission_folder, files[0])
    private_key_text = os.getenv("COMPETITION_PRIVATE_KEY")
    
    # --- DIAGNOSTIC SECTION ---
    with open(encrypted_path, "rb") as f:
        encrypted_data = f.read()
    
    print(f"DEBUG: Key Secret Found = {private_key_text is not None}")
    print(f"DEBUG: Encrypted File Size = {len(encrypted_data)} bytes")
    # --------------------------

    private_key = serialization.load_pem_private_key(private_key_text.encode(), password=None)
    
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    print("✅ Decryption successful!")

if __name__ == "__main__":
    evaluate()
