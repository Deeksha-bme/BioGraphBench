import csv
import os
from datetime import datetime

def main():
    score_path = "score.txt"
    csv_path = "leaderboard.csv"
    md_path = "leaderboard.md"

    if not os.path.exists(score_path): return

    score = open(score_path).read().strip()
    team = os.getenv("PARTICIPANT", "Unknown")
    model = os.getenv("MODEL_TYPE", "Baseline") # Matches the YAML env
    date = datetime.now().strftime("%Y-%m-%d")

    # Read existing entries, skipping blank lines
    rows = []
    if os.path.exists(csv_path):
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('team'): rows.append(row)

    # Add and Sort
    rows.append({"team": team, "score": score, "model": model, "date": date})
    rows.sort(key=lambda x: float(x['score']), reverse=True)

    # Write CSV (newline='' stops the blank lines!)
    with open(csv_path, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["team", "score", "model", "date"])
        writer.writeheader()
        writer.writerows(rows)

    # Write Markdown
    md = "# Leaderboard\n\n| Rank | Team | Score | Model | Date |\n|---|---|---|---|---|\n"
    for i, r in enumerate(rows, 1):
        md += f"| {i} | {r['team']} | {r['score']} | {r['model']} | {r['date']} |\n"
    with open(md_path, "w") as f: f.write(md)

if __name__ == "__main__":
    main()
