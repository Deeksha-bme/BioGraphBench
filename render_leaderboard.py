import csv
import os
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "leaderboard.csv"
MD_PATH = ROOT / "leaderboard.md"
SCORE_FILE = ROOT / "score.txt"

def update_csv():
    # 1. Read the new score from evaluate.py's output
    if not SCORE_FILE.exists():
        print("No new score to add.")
        return
    
    new_score = SCORE_FILE.read_text().strip()
    # Get the username of whoever uploaded the file
    team_name = os.getenv("GITHUB_ACTOR", "Participant")
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 2. Append to CSV
    file_is_empty = not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0
    with CSV_PATH.open("a", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["team", "model_type", "score", "date"])
        if file_is_empty:
            writer.writeheader()
        writer.writerow({
            "team": team_name,
            "model_type": "GNN-Submission",
            "score": new_score,
            "date": date_str
        })
    print(f"Added score {new_score} for {team_name} to CSV.")

def read_rows():
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [r for r in reader if (r.get("team") or "").strip()]

def main():
    # FIRST: Move the score from the text file into the CSV
    update_csv()
    
    # SECOND: Generate the Markdown as you did before
    rows = read_rows()
    
    def score_key(r):
        try: return float(r.get("score", "0"))
        except: return 0.0
    
    # Sort: Highest score first
    rows.sort(key=score_key, reverse=True)

    lines = [
        "# Leaderboard\n",
        "This leaderboard is **auto-updated** via GitHub Actions.\n\n",
        "| Rank | Team | Model | Score | Date |\n",
        "|---:|---|---|---:|---|\n"
    ]

    for i, r in enumerate(rows, start=1):
        team = r.get("team", "Unknown").strip()
        model = r.get("model_type", "N/A").strip()
        score = r.get("score", "0").strip()
        date = r.get("date", "").strip()
        lines.append(f"| {i} | {team} | `{model}` | {score} | {date} |\n")

    MD_PATH.write_text("".join(lines), encoding="utf-8")
    print(f"Successfully updated {MD_PATH}")

if __name__ == "__main__":
    main()
