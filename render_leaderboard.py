import csv
import os
from datetime import datetime
from pathlib import Path

def main():
    base_path = Path(__file__).resolve().parent
    score_path = base_path / "score.txt"
    csv_path = base_path / "leaderboard.csv"
    md_path = base_path / "leaderboard.md"

    if not score_path.exists(): return

    score = score_path.read_text().strip()
    team = os.getenv("PARTICIPANT", "Anonymous")
    model = os.getenv("MODEL_TYPE", "Baseline") 
    date = datetime.now().strftime("%Y-%m-%d")

    # Read existing rows and FILTER OUT blank ones
    rows = []
    if csv_path.exists():
        with open(csv_path, "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Only keep rows that actually have a team name
                if row.get('team') and row['team'].strip():
                    rows.append(row)

    # Add the new result
    rows.append({"team": team, "score": score, "model": model, "date": date})
    
    # Sort by score
    rows.sort(key=lambda x: float(x.get('score', 0)), reverse=True)
    
    # Write back to CSV - 'newline=""' prevents those blank lines!
    with open(csv_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["team", "score", "model", "date"])
        writer.writeheader()
        writer.writerows(rows)
    
    # Rebuild Markdown Table
    md_content = "# Leaderboard\n\n| Rank | Team | Score | Model | Date |\n|---|---|---|---|---|\n"
    for i, r in enumerate(rows, 1):
        md_content += f"| {i} | {r['team']} | {float(r['score']):.4f} | {r['model']} | {r['date']} |\n"
    md_path.write_text(md_content, encoding='utf-8')

if __name__ == "__main__":
    main()
