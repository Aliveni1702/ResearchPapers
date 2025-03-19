import argparse
import json
from researchpaper.fetcher import fetch_and_filter_papers
from researchpaper.serializers import papers_to_csv

def save_csv(file_name, csv_data):
    """Saves CSV data to a file."""
    with open(file_name, "w", encoding="utf-8", newline="") as f:
        f.write(csv_data)
    print(f"✅ CSV saved successfully: {file_name}")

def main():
    parser = argparse.ArgumentParser(description="Fetch and export PubMed papers.")

    parser.add_argument("--query", type=str, required=True, help="Search query for PubMed")
    parser.add_argument("--export", type=str, help="Export papers to CSV file (optional)")

    args = parser.parse_args()

    print(f"🔍 Searching for papers with query: {args.query}")
    
    papers = fetch_and_filter_papers(args.query)

    if not papers:
        print("❌ No papers found.")
        return

    if args.export:
        csv_data = papers_to_csv(papers)
        save_csv(args.export, csv_data)
    else:
        print(json.dumps({"papers": papers}, indent=4))

if __name__ == "__main__":
    main()
