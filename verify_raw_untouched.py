import hashlib
import subprocess

def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

before = file_hash("data/raw/prices.csv")

subprocess.run(["python", "-m", "src.validate.profile"], check=True)
subprocess.run(["python", "-m", "src.transform.clean"], check=True)

after = file_hash("data/raw/prices.csv")

if before == after:
    print("Raw file untouched, hashes match:", before)
else:
    print("WARNING: raw file was modified!")