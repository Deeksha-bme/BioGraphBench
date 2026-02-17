import csv
import os
from datetime import datetime

def main():
    score_path = "score.txt"
    csv_path = "leaderboard.csv"
    md_path = "leaderboard.md"

    if not os.path.exists(score_path): return

    score = open(score_path).read().strip()
    
    # FIX: These MUST match your YAML 'participant_name' and 'model_name'
    team = os.getenv("PARTICIPANT", "Unknown")
    model = os.getenv("MODEL_TYPE", "Baseline") 
    date = datetime.now().strftime("%Y-%m-%d")

    rows = []
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('team'): rows.append(row)

    rows.append({"team": team, "score": score, "model": model, "date": date})
    rows.sort(key=lambda x: float(x.get('score', 0)), reverse=True)

    # newline='' prevents the blank lines you found earlier
    with open(csv_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["team", "score", "model", "date"])
        writer.writeheader()
        writer.writerows(rows)

    md = "# Leaderboard\n\n| Rank | Team | Score | Model | Date |\n|---|---|---|---|---|\n"
    for i, r in enumerate(rows, 1):
        md += f"| {i} | {r['team']} | {float(r['score']):.4f} | {r['model']} | {r['date']} |\n"
    with open(md_path, "w", encoding='utf-8') as f: f.write(md)

if __name__ == "__main__":
    main()
