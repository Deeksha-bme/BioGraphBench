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

    # 1. Check if the evaluation script actually produced a score
    if not score_path.exists():
        print("Error: score.txt not found. Did evaluate.py run?")
        return

    # 2. Grab the data from GitHub environment variables
    score = score_path.read_text().strip()
    team = os.getenv("PARTICIPANT", "Unknown_Team")
    
    # This line fixes the "N/A" by grabbing your 'Model Type' input
    model = os.getenv("MODEL_TYPE", "Baseline") 
    date = datetime.now().strftime("%Y-%m-%d")

    # 3. Update the CSV file
    file_exists = csv_path.exists()
    with open(csv_path, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # If file is new, add the header first
        if not file_exists or os.stat(csv_path).st_size == 0:
            writer.writerow(["team", "score", "model", "date"])
        writer.writerow([team, score, model, date])
    
    # 4. Sort all results so the highest score is at the top
    rows = []
    with open(csv_path, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['score'] = float(row['score'])
                rows.append(row)
            except (ValueError, KeyError):
                continue
    
    # Sort by score (highest first)
    rows.sort(key=lambda x: x['score'], reverse=True)
    
    # 5. Create the Markdown table for the website
    md_content = "# Leaderboard\n\n| Rank | Team | Score | Model | Date |\n|---|---|---|---|---|\n"
    for i, r in enumerate(rows, 1):
        # Format score to 4 decimal places
        md_content += f"| {i} | {r['team']} | {r['score']:.4f} | {r['model']} | {r['date']} |\n"
        
    md_path.write_text(md_content, encoding='utf-8')
    
    # 6. Cleanup files so they don't interfere with the next run
    if score_path.exists(): 
        os.remove(score_path)
    
    # Remove the submission file after it's been processed
    for f in glob.glob("submissions/*.csv"): 
        os.remove(f)

if __name__ == "__main__":
    main()
