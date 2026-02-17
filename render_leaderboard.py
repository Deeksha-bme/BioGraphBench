import csv
import os
from datetime import datetime
from pathlib import Path

def main():
    base_path = Path(__file__).resolve().parent
    score_path = base_path / "score.txt"
    csv_path = base_path / "leaderboard.csv"
    md_path = base_path / "leaderboard.md"

    if not score_path.exists():
        return

    score = score_path.read_text().strip()
    
    # GRAB INPUTS: These names must match your .yml file exactly
    team = os.getenv("PARTICIPANT", "Anonymous")
    model = os.getenv("MODEL_TYPE", "Baseline") 
    date = datetime.now().strftime("%Y-%m-%d")

    # Append to the CSV file
    file_exists = csv_path.exists()
    with open(csv_path, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists or os.stat(csv_path).st_size == 0:
            writer.writerow(["team", "score", "model", "date"])
        writer.writerow([team, score, model, date])
    
    # Sort data by score (highest first)
    rows = []
    with open(csv_path, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['score'] = float(row['score'])
                rows.append(row)
            except:
                continue
    
    rows.sort(key=lambda x: x['score'], reverse=True)
    
    # Rebuild the Markdown table for the website
    md_content = "# Leaderboard\n\n| Rank | Team | Score | Model | Date |\n|---|---|---|---|---|\n"
    for i, r in enumerate(rows, 1):
        md_content += f"| {i} | {r['team']} | {r['score']:.4f} | {r['model']} | {r['date']} |\n"
    
    md_path.write_text(md_content, encoding='utf-8')

if __name__ == "__main__":
    main()
