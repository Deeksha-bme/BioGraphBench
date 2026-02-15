import csv
import os
from pathlib import Path
from datetime import datetime

# This ensures the script finds the files no matter where it runs
ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "leaderboard.csv"
MD_PATH = ROOT / "leaderboard.md"
SCORE_FILE = ROOT / "score.txt"

def main():
    # 1. Check if evaluate.py actually finished
    if not SCORE_FILE.exists():
        print("❌ No new score.txt found. Did evaluate.py fail?")
        return

    new_score = SCORE_FILE.read_text().strip()
    team_name = os.getenv("GITHUB_ACTOR", "Participant")
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 2. Add the score to the CSV
    with open(CSV_PATH, "a", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        # If file is empty, you might need writer.writerow(["team", "model_type", "score", "date"])
        writer.writerow([team_name, "GNN-Model", new_score, date_now])
    
    print(f"✅ Added {new_score} to CSV for {team_name}")

    # 3. Re-read everything to sort it
    rows = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Sort: Highest score first
    rows.sort(key=lambda x: float(x.get("score", 0)), reverse=True)

    # 4. Update the Markdown (The Website View)
    lines = ["# Leaderboard\n\n| Rank | Team | Score | Date |\n|---:|---|---:|---|\n"]
    for i, r in enumerate(rows, start=1):
        lines.append(f"| {i} | {r['team']} | {r['score']} | {r['date']} |\n")

    MD_PATH.write_text("".join(lines), encoding="utf-8")
    print("✅ Leaderboard.md updated!")

if __name__ == "__main__":
    main()
