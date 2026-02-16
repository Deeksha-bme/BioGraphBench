import csv
import os
from datetime import datetime

def main():
    if not os.path.exists("score.txt"):
        return

    with open("score.txt", "r") as f:
        score = f.read().strip()

    team = os.getenv("PARTICIPANT", "Unknown")
    date = datetime.now().strftime("%Y-%m-%d")

    # Update CSV
    file_exists = os.path.isfile("leaderboard.csv")
    with open("leaderboard.csv", "a", newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["team", "score", "date"])
        writer.writerow([team, score, date])

    # Re-generate Markdown Table
    rows = []
    with open("leaderboard.csv", "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    rows.sort(key=lambda x: float(x['score']), reverse=True)
    
    md_content = "# Leaderboard\n\n| Rank | Team | Score | Date |\n|---|---|---|---|\n"
    for i, r in enumerate(rows, 1):
        md_content += f"| {i} | {r['team']} | {r['score']} | {r['date']} |\n"
        
    with open("leaderboard.md", "w") as f:
        f.write(md_content)

if __name__ == "__main__":
    main()
