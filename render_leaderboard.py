import csv
import os
from pathlib import Path
from datetime import datetime

def main():
    if not os.path.exists("score.txt"): return
    
    new_score = open("score.txt").read().strip()
    user = os.getenv("GITHUB_ACTOR", "Participant")
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Update CSV
    with open("leaderboard.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([user, "GNN-Model", new_score, date_now])

    # Update Markdown for website
    rows = []
    with open("leaderboard.csv", "r") as f:
        reader = csv.DictReader(f)
        rows = sorted(list(reader), key=lambda x: float(x['score']), reverse=True)

    md_content = "# Leaderboard\n\n| Rank | Team | Score | Date |\n|---:|---|---:|---|\n"
    for i, r in enumerate(rows, start=1):
        md_content += f"| {i} | {r['team']} | {r['score']} | {r['date']} |\n"
    
    with open("leaderboard.md", "w") as f:
        f.write(md_content)

if __name__ == "__main__":
    main()
