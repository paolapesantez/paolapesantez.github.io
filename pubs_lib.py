"""
Shared helpers for turning references.bib into rendered publication entries.
Imported by publications.qmd (catalog-card view) and cv.qmd (numbered list view).
Runs with cwd == project root during `quarto render`, so relative paths work as-is.
"""

import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

YOUR_NAME = "Pesantez-Cabrera, Paola"  # bolded wherever it appears in an author list

STAMP_LABELS = {
    "journal": ("JOURNAL", "rust"),
    "article": ("JOURNAL", "rust"),
    "preprint": ("PREPRINT", ""),
    "conference": ("CONFERENCE", ""),
    "inproceedings": ("CONFERENCE", ""),
}

_META_KEYS = {"ENTRYTYPE", "ID"}


def load_entries(bib_path="references.bib"):
    """Return bib entries sorted newest-first."""
    with open(bib_path) as f:
        bib = bibtexparser.load(f)
    return sorted(bib.entries, key=lambda e: int(e.get("year", 0)), reverse=True)


def format_authors(raw, bold_name=YOUR_NAME, style="full"):
    """style='full' -> 'First Last, First Last, & First Last'
    style='initials' -> 'Last, F., Last, F., & Last, F.' (compact CV style)"""
    people = [p.strip() for p in raw.split(" and ")]
    out = []
    for p in people:
        label = p
        if style == "initials" and "," in p:
            last, first = [x.strip() for x in p.split(",", 1)]
            initials = "".join(f"{part[0]}." for part in first.split() if part)
            label = f"{last}, {initials}"
        bold = (p == bold_name)
        out.append(f"**{label}**" if bold else label)
    if len(out) > 1:
        return ", ".join(out[:-1]) + ", & " + out[-1]
    return out[0]


def meta_line(entry):
    etype = entry.get("ENTRYTYPE", "").lower()
    if etype == "article":
        parts = [f"*{entry.get('journal', '')}*"]
        vol, num, pages = entry.get("volume"), entry.get("number"), entry.get("pages")
        if vol:
            parts.append(vol + (f"({num})" if num else ""))
        if pages:
            parts.append(pages)
        return ", ".join(parts) + f" ({entry.get('year', '')})."
    if etype == "inproceedings":
        return f"*{entry.get('booktitle', '')}* ({entry.get('year', '')})."
    return ""

def links_line(entry, include_cite=True):
    link_fields = [
        ("pdf", "PDF"), ("doi", "DOI"), ("code", "Code"),
        ("data", "Data"), ("slides", "Slides"),
    ]
    links = []
    for field, label in link_fields:
        if field in entry:
            href = entry[field]
            if field == "doi":
                href = f"https://doi.org/{href}"
            links.append(f'<a href="{href}">{label}</a>')
    return links


def stamp_for(entry):
    etype = entry.get("ENTRYTYPE", "").lower()
    custom_type = entry.get("type", etype).lower()
    return STAMP_LABELS.get(custom_type, ("PUBLICATION", ""))


def to_bibtex_string(entry):
    """Reconstruct a clean, standalone .bib entry for a single reference,
    for the 'Cite' / BibTeX-export links on the publications page."""
    clean = {k: v for k, v in entry.items() if k not in _META_KEYS}
    clean["ENTRYTYPE"] = entry["ENTRYTYPE"]
    clean["ID"] = entry["ID"]
    db = BibDatabase()
    db.entries = [clean]
    writer = BibTexWriter()
    writer.indent = "  "
    writer.order_entries_by = None
    return writer.write(db).strip()
