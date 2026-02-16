import csv
import os
import glob
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
    team = os.getenv("PARTICIPANT", "Unknown")
    # We add a default model type since it's not in your workflow yet
    model = "Baseline" 
    date = datetime.now().strftime("%Y-%m-%d")

    # Update CSV with the correct columns
    file_exists = csv_path.exists()
    with open(csv_path, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists or os.stat(csv_path).st_size == 0:
            writer.writerow(["team", "score", "model", "date"])
        writer.writerow([team, score, model, date])
    
    # Sort and Render
    rows = []
    with open(csv_path, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['score'] = float(row['score'])
                rows.append(row)
            except: continue
    
    rows.sort(key=lambda x: x['score'], reverse=True)
    
    md_content = "# Leaderboard\n\n| Rank | Team | Score | Model | Date |\n|---|---|---|---|---|\n"
    for i, r in enumerate(rows, 1):
        md_content += f"| {i} | {r['team']} | {r['score']:.4f} | {r['model']} | {r['date']} |\n"
        
    md_path.write_text(md_content, encoding='utf-8')
    
    # Cleanup files for next run
    if score_path.exists(): os.remove(score_path)
    for f in glob.glob("submissions/*.csv"): os.remove(f)

if __name__ == "__main__":
    main()
