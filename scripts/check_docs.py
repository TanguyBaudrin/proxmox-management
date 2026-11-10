#!/usr/bin/env python3
"""Structure and prose checks for the documentation.

The script is the source of truth for the rules that a machine can judge.
Vale and markdownlint cover the rest.

Exit code 1 when at least one error is reported.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"
TERMINOLOGY = ROOT / "scripts" / "terminology.json"

ALLOWED_TYPES = {
    "index",
    "glossary",
    "adr",
    "how-to",
    "reference",
    "explanation",
    "tutorial",
}
ADR_STATUS = {"proposed", "accepted", "rejected", "superseded", "deprecated"}
PROCEDURE_TYPES = {"how-to", "tutorial", "reference"}
LIMITS = {"how-to": 20, "tutorial": 20, "reference": 20}
DEFAULT_LIMIT = 25

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
FENCE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
ACRONYM = re.compile(r"\b[A-Z][A-Z0-9]{1,7}\b")
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’._/-]*")
CONTRACTION = re.compile(
    r"\b(?:\w+['’](?:t|re|ve|ll|d|m)|(?:it|that|there|here|what|who|this|let|one)['’]s)\b",
    re.IGNORECASE,
)

errors: list[str] = []
warnings: list[str] = []


def report(path: Path, line: int, rule: str, message: str) -> None:
    rel = path.relative_to(ROOT)
    errors.append(f"{rel}:{line}: [{rule}] {message}")


def warn(path: Path, line: int, rule: str, message: str) -> None:
    rel = path.relative_to(ROOT)
    warnings.append(f"{rel}:{line}: [{rule}] {message}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_front_matter(text: str) -> tuple[dict[str, str], str, int]:
    match = FRONT_MATTER.match(text)
    if not match:
        return {}, text, 0
    meta: dict[str, str] = {}
    for raw in match.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        key, _, value = raw.partition(":")
        meta[key.strip()] = value.strip().strip('"').strip("'")
    body = text[match.end():]
    return meta, body, match.group(0).count("\n")


def blank_sub(pattern: re.Pattern[str], text: str) -> str:
    """Replace a match with spaces, and keep the line structure."""
    def keep_lines(m: re.Match[str]) -> str:
        return "".join("\n" if c == "\n" else " " for c in m.group(0))

    return pattern.sub(keep_lines, text)


def prose(body: str) -> str:
    return blank_sub(INLINE_CODE, blank_sub(FENCE, body))


LIST_MARKER = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+")
EMPHASIS = re.compile(r"\*\*|__")


def blocks(body: str) -> list[tuple[int, str]]:
    """Group wrapped lines into logical blocks, with the starting line."""
    out: list[tuple[int, str]] = []
    current: list[str] = []
    start = 0
    for index, raw in enumerate(body.splitlines(), start=1):
        stripped = EMPHASIS.sub("", raw.strip())
        starts_block = stripped.startswith(("|", "#", "<", ">")) or bool(
            LIST_MARKER.match(stripped)
        )
        if not stripped:
            if current:
                out.append((start, " ".join(current)))
                current = []
            continue
        if starts_block and current:
            out.append((start, " ".join(current)))
            current = []
        if not current:
            start = index
        current.append(LIST_MARKER.sub("", stripped))
    if current:
        out.append((start, " ".join(current)))
    text = [(line, re.sub(r"\s{2,}", " ", block)) for line, block in out]
    return text


def sentences(block: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'`])", block)
    return [part.strip() for part in parts if part.strip()]


def word_count(sentence: str) -> int:
    clean = LINK.sub(r"\1", sentence)
    return len(WORD.findall(clean))


def check_nav(files: list[Path]) -> set[str]:
    config = read(MKDOCS)
    listed = set(re.findall(r"([A-Za-z0-9_./-]+\.md)\b", config))
    for entry in sorted(listed):
        if not (DOCS / entry).exists():
            report(MKDOCS, 0, "nav-target", f"navigation lists a missing page: {entry}")
    for path in files:
        rel = str(path.relative_to(DOCS))
        if rel not in listed:
            report(path, 1, "nav", "page is missing from mkdocs.yml nav")
    return listed


def check_front_matter(path: Path, meta: dict[str, str]) -> str:
    doc_type = meta.get("type", "")
    if not doc_type:
        report(path, 1, "front-matter", "missing type")
    elif doc_type not in ALLOWED_TYPES:
        report(path, 1, "type", f"unknown type '{doc_type}'")
    if not meta.get("title"):
        report(path, 1, "front-matter", "missing title")
    return doc_type


def check_adr(path: Path, meta: dict[str, str], index_text: str) -> None:
    status = meta.get("status", "")
    if status not in ADR_STATUS:
        report(path, 1, "adr-status", f"invalid status '{status}'")
    if not meta.get("date"):
        report(path, 1, "adr-date", "missing date")
    if path.name not in index_text:
        report(path, 1, "adr-index", "the ADR index does not link this file")


def check_sentences(path: Path, doc_type: str, body: str) -> None:
    limit = LIMITS.get(doc_type, DEFAULT_LIMIT)
    strict = doc_type in PROCEDURE_TYPES
    for line, block in blocks(prose(body)):
        if block.startswith(("|", "#", "<")):
            continue
        for sentence in sentences(block):
            count = word_count(sentence)
            if count <= limit:
                continue
            message = f"{count} words, limit {limit}: {sentence[:90]}"
            if strict:
                report(path, line, "sentence", message)
            else:
                warn(path, line, "sentence", message)


def check_line_rules(path: Path, doc_type: str, body: str) -> None:
    strict = doc_type in PROCEDURE_TYPES
    text = prose(body)
    for number, line in enumerate(text.splitlines(), start=1):
        if ";" in line:
            message = "semicolon in a procedure"
            if strict:
                report(path, number, "semicolon", message)
            else:
                warn(path, number, "semicolon", message)
        if CONTRACTION.search(line):
            report(path, number, "contraction", "contraction found")


def check_phrases(path: Path, body: str, phrases: list[str]) -> None:
    if path.name == "style-ste100.md":
        # The style page quotes the forbidden forms on purpose.
        return
    text = prose(body).lower()
    for phrase in phrases:
        for match in re.finditer(rf"\b{re.escape(phrase)}\b", text):
            line = text.count("\n", 0, match.start()) + 1
            report(path, line, "phrase", f"banned phrase '{phrase}'")


def check_synonyms(path: Path, body: str, synonyms: dict[str, list[str]]) -> None:
    if path.name == "glossary.md":
        return
    text = prose(body)
    for canonical, variants in synonyms.items():
        for variant in variants:
            pattern = rf"\b{re.escape(variant)}\b"
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                line = text.count("\n", 0, match.start()) + 1
                report(path, line, "synonym", f"'{variant}' is a variant of '{canonical}'")


def check_acronyms(path: Path, body: str, allowed: set[str]) -> None:
    if path.name == "glossary.md":
        # The glossary is where the acronyms and the banned variants live.
        return
    text = prose(body)
    for match in ACRONYM.finditer(text):
        token = match.group(0)
        if token in allowed:
            continue
        line = text.count("\n", 0, match.start()) + 1
        report(path, line, "acronym", f"'{token}' is not in the glossary")


def glossary_tables(text: str) -> tuple[list[str], set[str]]:
    terms: list[str] = []
    acronyms: set[str] = set()
    section = ""
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip().lower()
            continue
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or set(cells[0]) <= set("-: "):
            continue
        if section == "terms" and len(cells) >= 2:
            terms.append(cells[0])
        elif section == "acronyms" and len(cells) >= 2:
            acronyms.add(cells[0])
    return terms, acronyms


def main() -> int:
    files = sorted(DOCS.rglob("*.md"))
    if not files:
        print("no documentation found", file=sys.stderr)
        return 1

    terminology = json.loads(read(TERMINOLOGY))
    glossary = read(DOCS / "glossary.md")
    terms, acronyms = glossary_tables(glossary)
    adr_index = read(DOCS / "adr" / "index.md")

    check_nav(files)

    for path in files:
        text = read(path)
        meta, body, _ = split_front_matter(text)
        doc_type = check_front_matter(path, meta)
        if doc_type == "adr":
            check_adr(path, meta, adr_index)
        check_sentences(path, doc_type, body)
        check_line_rules(path, doc_type, body)
        check_phrases(path, body, terminology["phrases"])
        check_synonyms(path, body, terminology["synonyms"])
        check_acronyms(path, body, acronyms)

    corpus = "\n".join(
        read(path) for path in files
        if path.name not in {"glossary.md"}
    ).lower()
    for term in terms:
        if term.lower() not in corpus:
            report(DOCS / "glossary.md", 0, "glossary-unused", f"term '{term}' appears in no page")

    for message in warnings:
        print(f"warning: {message}")
    for message in errors:
        print(message)
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
