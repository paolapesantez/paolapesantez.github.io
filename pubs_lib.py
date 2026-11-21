"""
Shared helpers for turning references.bib into rendered publication entries.
Imported by publications.qmd (catalog-card view) and cv.qmd (numbered list view).
Runs with cwd == project root during `quarto render`, so relative paths work as-is.
"""

import re
import unicodedata

import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

YOUR_NAME = "Pesantez-Cabrera, Paola"  # bolded wherever it appears in an author list

# pub_type() -> (stamp label, css class)
STAMP_LABELS = {
    "journal": ("JOURNAL", "rust"),
    "conference": ("CONFERENCE", ""),
    "chapter": ("BOOK CHAPTER", ""),
    "preprint": ("PREPRINT", ""),
}

JOURNAL_TYPES = {"article"}
CONFERENCE_TYPES = {"inproceedings", "conference", "proceedings"}
CHAPTER_TYPES = {"incollection", "inbook"}
PREPRINT_TYPES = {"misc", "unpublished", "online", "preprint"}

# Words a `type = {...}` field may use to override the entry type.
TYPE_ALIASES = {
    "journal": "journal", "article": "journal",
    "conference": "conference", "inproceedings": "conference", "proceedings": "conference",
    "chapter": "chapter", "incollection": "chapter", "inbook": "chapter", "book chapter": "chapter",
    "preprint": "preprint", "misc": "preprint",
}

_META_KEYS = {"ENTRYTYPE", "ID"}


# ----------------------------------------------------------------------------- utils
def _clean(text):
    """Strip BibTeX braces/backslashes and turn --/--- into proper dashes."""
    text = (text or "").replace("{", "").replace("}", "").replace("\\", "")
    text = text.replace("---", "—").replace("--", "–")
    return re.sub(r"\s+", " ", text).strip()


def _fold(text):
    """Lower-case and drop accents, so 'Pesántez' matches 'Pesantez'."""
    text = unicodedata.normalize("NFKD", _clean(text))
    return "".join(c for c in text if not unicodedata.combining(c)).lower()


def _year(entry):
    m = re.search(r"\d{4}", entry.get("year", ""))
    return int(m.group()) if m else 0


# ----------------------------------------------------------------------------- loading
def load_entries(bib_path="references.bib"):
    """Return bib entries sorted newest-first."""
    with open(bib_path, encoding="utf-8") as f:
        bib = bibtexparser.load(f)
    return sorted(bib.entries, key=_year, reverse=True)


# ----------------------------------------------------------------------------- classification
def pub_type(entry):
    """Return 'journal', 'conference', 'chapter', 'preprint' or 'other'.

    1. An explicit `type = {conference}` (or journal/chapter/preprint) field wins.
    2. Otherwise the BibTeX entry type decides.
    3. Safety net: an @article whose "journal" is really conference proceedings
       (e.g. "Proceedings of the AAAI Conference ...") is treated as a conference
       paper, and an @article in arXiv/bioRxiv etc. (or with no journal) as a preprint.
    """
    custom = _fold(entry.get("type", ""))
    if custom in TYPE_ALIASES:
        return TYPE_ALIASES[custom]

    etype = entry.get("ENTRYTYPE", "").lower()
    if etype in JOURNAL_TYPES:
        venue = _fold(entry.get("journal", ""))
        if not venue:  # @article with no journal is not a published article
            return "preprint"
        if re.search(r"\b(arxiv|biorxiv|medrxiv|ssrn|preprint)\b", venue):
            return "preprint"
        if re.search(r"\bproceedings\b", venue) and re.search(r"\b(conference|symposium|workshop)\b", venue):
            return "conference"
        return "journal"
    if etype in CONFERENCE_TYPES:
        return "conference"
    if etype in CHAPTER_TYPES:
        return "chapter"
    return "preprint" if etype in PREPRINT_TYPES else "other"  # book, thesis, report...


def stamp_for(entry):
    return STAMP_LABELS.get(pub_type(entry), ("PUBLICATION", ""))


# ----------------------------------------------------------------------------- authors
def format_authors(raw, bold_name=YOUR_NAME, style="full"):
    """style='full' -> 'Last, First, Last, First, & Last, First' (as stored in the .bib)
    style='initials' -> 'Last, F., Last, F., & Last, F.' (compact CV style)

    Your name is bolded even if the .bib spells it with accents or a middle initial
    (e.g. 'Pesántez-Cabrera, Paola G.')."""
    b_last, _, b_first = _fold(bold_name).partition(",")
    b_last, b_first = b_last.strip(), b_first.strip()

    people = [_clean(p) for p in raw.split(" and ") if p.strip()]
    out = []
    for p in people:
        label = p
        if "," in p:
            last, first = [x.strip() for x in p.split(",", 1)]
        else:  # "First Last" form
            parts = p.rsplit(" ", 1)
            first, last = (parts[0], parts[1]) if len(parts) == 2 else ("", p)
        if style == "initials":
            initials = "".join(f"{part[0]}." for part in re.split(r"[\s-]+", first) if part)
            label = f"{last}, {initials}" if initials else last
        f_last, f_first = _fold(last), _fold(first)
        bold = f_last == b_last and (not b_first or f_first.startswith(b_first))
        out.append(f"**{label}**" if bold else label)
    if len(out) > 1:
        return ", ".join(out[:-1]) + ", & " + out[-1]
    return out[0] if out else ""


# ----------------------------------------------------------------------------- venue line
def meta_line(entry):
    kind = pub_type(entry)
    year = entry.get("year", "")
    vol, num = entry.get("volume"), entry.get("number")
    pages = _clean(entry.get("pages"))
    publisher = _clean(entry.get("publisher"))

    if kind == "journal":
        parts = [f"*{_clean(entry.get('journal'))}*"]
        if vol:
            parts.append(vol + (f"({num})" if num else ""))
        if pages:
            parts.append(pages)
        return ", ".join(parts) + f" ({year})."

    if kind == "conference":
        venue = _clean(entry.get("booktitle") or entry.get("journal"))
        parts = [f"In *{venue}*"]
        if vol:  # e.g. AAAI proceedings volume/issue, or a CCIS series volume
            parts.append(f"vol. {vol}" + (f"({num})" if num else ""))
        if pages:
            parts.append(f"pp. {pages}")
        if publisher:
            parts.append(publisher)
        return ", ".join(parts) + f" ({year})."

    if kind == "chapter":
        parts = [f"In *{_clean(entry.get('booktitle'))}*"]
        editors = _clean(entry.get("editor"))
        if editors:
            parts.append(f"ed. {editors.replace(' and ', ', ')}")
        if pages:
            parts.append(f"pp. {pages}")
        if publisher:
            parts.append(publisher)
        return ", ".join(parts) + f" ({year})."

    # preprint / other
    venue = _clean(entry.get("howpublished") or entry.get("journal") or entry.get("publisher"))
    if entry.get("eprint") and not venue:
        venue = f"{entry.get('archiveprefix', 'arXiv')} preprint {entry['eprint']}"
    return f"*{venue}* ({year})." if venue else f"Preprint ({year})."


# ----------------------------------------------------------------------------- links / export
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