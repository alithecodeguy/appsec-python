"""Maintain GitHub reading navigation and check local Markdown links (stdlib only)."""

import argparse
import html
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "manuscript/chapters"
LINK = re.compile(r"\[([^\]\n]+)\]\((<[^>]+>|(?:[^\s()]|\([^()]*\))+)(?:\s+\"[^\"]*\")?\)")


def prose(text):
    """Yield numbered non-fenced lines; retain blank lines for source locations."""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            continue
        if marker:
            fence = marker[1]
            continue
        yield number, line
    if fence:
        raise ValueError("unclosed code fence")


def slug(title):
    title = LINK.sub(r"\1", title)
    title = html.unescape(re.sub(r"<[^>]+>", "", title)).lower()
    return "".join(c for c in title if c in "-_ " or unicodedata.category(c)[0] in "LNM").replace(" ", "-")


def headings(text):
    used = set()
    result = []
    for _, line in prose(text):
        match = re.match(r"^ {0,3}(#{1,6})\s+(.+?)(?:\s+#+)?\s*$", line)
        if match:
            base = slug(match[2])
            anchor, suffix = base, 0
            while anchor in used:
                suffix += 1
                anchor = f"{base}-{suffix}"
            used.add(anchor)
            result.append((len(match[1]), match[2], anchor))
    return result


def block(name, body):
    return f"<!-- book:{name}:start -->\n{body}\n<!-- book:{name}:end -->"


def strip_navigation(text):
    return re.sub(r"\n*<!-- book:(header|footer):start -->.*?<!-- book:\1:end -->\n*", "\n\n", text, flags=re.S).strip() + "\n"


def chapter_navigation(path, text):
    clean = strip_navigation(text)
    number = int(path.stem)
    sections = headings(clean)
    title = sections[0][1]
    previous = f"[← Chapter {number - 1:02}]({number - 1:02}.md)" if number > 1 else "[← Preface](../README.md#preface)"
    following = f"[Chapter {number + 1:02} →]({number + 1:02}.md)" if number < 44 else "[Appendices →](../appendices.md)"
    nav = f"{previous} · [Contents](../README.md#contents) · [Repository](../../README.md) · {following}"
    companion = ROOT / f"examples/ch{number:02}/README.md"
    companion_link = f"\n\n[Runnable companion](../../examples/ch{number:02}/README.md)" if companion.is_file() else ""
    toc = "\n".join(f"- [{label}](#{anchor})" for level, label, anchor in sections if level == 2)
    header = block("header", nav + companion_link + "\n\n<details>\n<summary>In this chapter</summary>\n\n" + toc + "\n\n</details>")
    first, body = clean.split("\n", 1)
    footer = block("footer", "---\n\n" + nav + f"\n\n[Back to top](#{slug(title)})")
    return first + "\n\n" + header + "\n" + body.rstrip() + "\n\n" + footer + "\n"


def documents():
    process = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", "*.md"],
        cwd=ROOT, check=True, capture_output=True,
    )
    return sorted({ROOT / name.decode() for name in process.stdout.split(b"\0") if name})


def reference_key(label):
    return " ".join(label.split()).casefold()


def links(text):
    lines = [(number, re.sub(r"(`+).*?\1", "code", line)) for number, line in prose(text)]
    definitions = {}
    for _, line in lines:
        match = re.match(r"^ {0,3}\[([^]]+)\]:\s*(<[^>]+>|\S+)", line)
        if match:
            definitions[reference_key(match[1])] = match[2].strip("<>")
    for number, line in lines:
        if re.match(r"^ {0,3}\[[^]]+\]:", line):
            continue
        for match in LINK.finditer(line):
            yield number, match[2].strip("<>")
        remainder = LINK.sub("", line)
        for match in re.finditer(r"\[([^]\n]+)\]\[([^]\n]*)\]", remainder):
            key = reference_key(match[2] or match[1])
            if key not in definitions:
                raise ValueError(f"line {number}: undefined reference [{key}]")
            yield number, definitions[key]
        remainder = re.sub(r"\[[^]\n]+\]\[[^]\n]*\]", "", remainder)
        for match in re.finditer(r"\[([^]\n]+)\](?!\(|:)", remainder):
            key = reference_key(match[1])
            if key in definitions:
                yield number, definitions[key]


def check_links(paths):
    errors, count, cache = [], 0, {}
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
            for number, destination in links(text):
                parsed = urlsplit(destination)
                if parsed.scheme or parsed.netloc:
                    continue
                count += 1
                target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve()
                where = f"{path.relative_to(ROOT)}:{number}: {destination}"
                if not target.is_relative_to(ROOT):
                    errors.append(where + " (outside repository)")
                elif not target.exists():
                    errors.append(where + " (missing file)")
                elif parsed.fragment and target.suffix == ".md":
                    if target not in cache:
                        cache[target] = {anchor for _, _, anchor in headings(target.read_text(encoding="utf-8"))}
                    if unquote(parsed.fragment) not in cache[target]:
                        errors.append(where + " (missing heading)")
        except (ValueError, OSError) as error:
            errors.append(f"{path.relative_to(ROOT)}: {error}")
    return count, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="refresh generated chapter navigation before checking")
    args = parser.parse_args()
    errors = []
    expected = {f"{number:02}.md" for number in range(1, 45)}
    actual = {path.name for path in CHAPTERS.glob("*.md")}
    if actual != expected:
        errors.append(f"Expected chapters 01–44; missing={sorted(expected - actual)}, extra={sorted(actual - expected)}")
    for name in sorted(actual & expected):
        path = CHAPTERS / name
        text = path.read_text(encoding="utf-8")
        try:
            generated = chapter_navigation(path, text)
        except (ValueError, IndexError) as error:
            errors.append(f"{path.relative_to(ROOT)}: {error}")
            continue
        if text != generated:
            if args.write:
                path.write_text(generated, encoding="utf-8")
            else:
                errors.append(f"{path.relative_to(ROOT)}: stale navigation; run python3 scripts/check_book.py --write")
    paths = documents()
    count, link_errors = check_links(paths)
    errors.extend(link_errors)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS: 44 chapters, generated navigation, {len(paths)} Markdown files, {count} local links/anchors.")
    print("External URLs, Mermaid rendering and executable examples require separate checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
