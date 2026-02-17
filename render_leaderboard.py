import csv
import os
from datetime import datetime
from pathlib import Path

def main():
    base_path = Path(__file__).resolve().parent.parent
    score_path = base_path / "score.txt"
    csv_path = base_path / "leaderboard.csv"
    md_path = base_path / "leaderboard.md"

    if not score_path.exists():
        return

    score = score_path.read_text().strip()
    
    # These MUST match the 'env' keys in your GitHub Actions YAML
    team = os.getenv("PARTICIPANT", "Anonymous")
    model = os.getenv("MODEL_TYPE", "Baseline") 
    date = datetime.now().strftime("%Y-%m-%d")

    # Read existing entries and filter out any empty lines
    rows = []
    if csv_path.exists():
        with open(csv_path, "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('team') and row['team'].strip():
                    rows.append(row)

    # Add the new entry
    rows.append({"team": team, "score": score, "model": model, "date": date})
    
    # Sort by score descending
    rows.sort(key=lambda x: float(x.get('score', 0)), reverse=True)
    
    # Write to CSV using newline='' to prevent blank rows
    with open(csv_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["team", "score", "model", "date"])
        writer.writeheader()
        writer.writerows(rows)
    
    # Build Markdown table
    md_content = "# Leaderboard\n\n| Rank | Team | Score | Model | Date |\n|---|---|---|---|---|\n"
    for i, r in enumerate(rows, 1):
        md_content += f"| {i} | {r['team']} | {float(r['score']):.4f} | {r['model']} | {r['date']} |\n"
    
    md_path.write_text(md_content, encoding='utf-8')

if __name__ == "__main__":
    main()
