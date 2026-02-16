import csv
import os
from datetime import datetime
from pathlib import Path

def main():
    # 1. Use Absolute Paths to ensure GitHub finds the files
    base_path = Path(__file__).resolve().parent
    score_path = base_path / "score.txt"
    csv_path = base_path / "leaderboard.csv"
    md_path = base_path / "leaderboard.md"

    # 2. Check if the score exists
    if not score_path.exists():
        print("❌ score.txt not found. Skipping update.")
        return

    score = score_path.read_text().strip()
    team = os.getenv("PARTICIPANT", "Unknown")
    date = datetime.now().strftime("%Y-%m-%d")

    # 3. Update CSV (Create it if it doesn't exist)
    file_exists = csv_path.exists()
    
    # We use 'a' to append the new score
    with open(csv_path, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists or os.stat(csv_path).st_size == 0:
            writer.writerow(["team", "score", "date"])
        writer.writerow([team, score, date])
    
    print(f"✅ Added {team} with score {score} to CSV.")

    # 4. Read CSV, Sort by Score, and Re-generate Markdown
    rows = []
    with open(csv_path, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Clean data to ensure it can be converted to float
            try:
                row['score'] = float(row['score'])
                rows.append(row)
            except ValueError:
                continue
    
    # Sort: Highest score at the top
    rows.sort(key=lambda x: x['score'], reverse=True)
    
    # 5. Build the Markdown table
    md_content = "# Leaderboard\n\n"
    md_content += "| Rank | Team | Score | Date |\n"
    md_content += "|:---:||:---|:---:|:---:|\n"
    
    for i, r in enumerate(rows, 1):
        md_content += f"| {i} | {r['team']} | {r['score']:.4f} | {r['date']} |\n"
        
    md_path.write_text(md_content, encoding='utf-8')
    print("✅ leaderboard.md updated successfully.")

if __name__ == "__main__":
    main()
