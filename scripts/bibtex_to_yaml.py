import bibtexparser
import yaml
from pathlib import Path

bib_path = Path("assets/publications.bib")
yaml_path = Path("data/publications.yaml")

with bib_path.open(encoding="utf-8") as f:
    bib_database = bibtexparser.load(f)

publications = []

for entry in bib_database.entries:

    entry_type = entry.get("ENTRYTYPE", "").lower()

    if entry_type == "article":
        pub_type = "Journal Articles"
    elif entry_type in ["inproceedings", "conference"]:
        pub_type = "Conference Papers"
    elif entry_type in ["book", "inbook", "incollection"]:
        pub_type = "Books / Book Chapters"
    else:
        pub_type = "arXiv Preprints"
    
    if pub_type == "Journal Articles":
        venue_label = "Journal"
    elif pub_type == "Conference Papers":
        venue_label = "Conference"
    elif pub_type == "Books / Book Chapters":
        venue_label = "Book"
    else:
        venue_label = "arXiv"

    title = entry.get("title", "").replace("{", "").replace("}", "")
    authors = entry.get("author", "")
    journal = entry.get("journal", entry.get("booktitle", ""))
    year = int(entry.get("year", 0)) if entry.get("year", "").isdigit() else entry.get("year", "")
    doi = entry.get("doi", "")
    url = entry.get("url", "")

    if doi and not doi.startswith("http"):
        doi = "https://doi.org/" + doi

    publications.append({
        "title": title,
        "authors": authors,
        "journal": journal,
        "year": year,
        "doi": doi or url,
        "type": pub_type,
        "venue_label": venue_label
    })

publications = sorted(publications, key=lambda x: x.get("year", 0), reverse=True)

with yaml_path.open("w", encoding="utf-8") as f:
    yaml.dump(publications, f, allow_unicode=True, sort_keys=False)

print(f"Converted {len(publications)} publications to {yaml_path}")