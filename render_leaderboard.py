import csv
from pathlib import Path
from datetime import datetime

# Path setup: Points to the main folder
ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "leaderboard.csv"
MD_PATH = ROOT / "leaderboard.md"

def read_rows():
    if not CSV_PATH.exists():
        print(f"CSV not found at {CSV_PATH}")
        return []
    with CSV_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [r for r in reader if (r.get("team") or "").strip()]

def main():
    rows = read_rows()
    
    # Sorting logic
    def score_key(r):
        try: return float(r.get("score", "-inf"))
        except: return float("-inf")
    
    def ts_key(r):
        try: return r.get("date", "") # Using 'date' based on your previous csv snippet
        except: return ""

    rows.sort(key=lambda r: (score_key(r), ts_key(r)), reverse=True)

    lines = [
        "# Leaderboard\n",
        "This leaderboard is **auto-updated** via GitHub Actions.\n\n",
        "| Rank | Team | Model | Score | Date |\n",
        "|---:|---|---|---:|---|\n"
    ]

    for i, r in enumerate(rows, start=1):
        team = r.get("team", "Unknown").strip()
        model = r.get("model_type", "N/A").strip()
        score = r.get("score", "0").strip()
        date = r.get("date", "").strip()
        lines.append(f"| {i} | {team} | `{model}` | {score} | {date} |\n")

    MD_PATH.write_text("".join(lines), encoding="utf-8")
    print(f"Successfully updated {MD_PATH}")

if __name__ == "__main__":
    main()
