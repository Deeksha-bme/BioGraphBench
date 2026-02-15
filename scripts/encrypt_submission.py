import sys
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def encrypt_submission(csv_file, public_key_file, output_file):
    # 1. Load the public "lock" you uploaded to GitHub
    with open(public_key_file, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # 2. Read the student's secret predictions
    with open(csv_file, "rb") as f:
        data = f.read()

    # 3. Encrypt the data so ONLY your private key can open it
    encrypted = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 4. Save the "locked" version
    with open(output_file, "wb") as f:
        f.write(encrypted)
    print(f"✅ Done! Created encrypted file: {output_file}")

if __name__ == "__main__":
    # Command: python encrypt_submission.py my_results.csv public_key.pem my_team.enc
    encrypt_submission(sys.argv[1], sys.argv[2], sys.argv[3])
