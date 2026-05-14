#!/usr/bin/env python3
"""CLI tool for managing code snippets. Snippets stored in ~/.snippets.json."""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SNIPPETS_FILE = Path.home() / ".snippets.json"


def load_snippets() -> list:
    if SNIPPETS_FILE.exists():
        return json.loads(SNIPPETS_FILE.read_text(encoding="utf-8"))
    return []


def save_snippets(snippets: list) -> None:
    SNIPPETS_FILE.write_text(
        json.dumps(snippets, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def next_id(snippets: list) -> int:
    return max((s["id"] for s in snippets), default=0) + 1


def add_snippet(title: str, code: str, lang: str = "python", tags: list = None, note: str = "") -> None:
    snippets = load_snippets()
    snippet = {
        "id": next_id(snippets),
        "title": title,
        "code": code,
        "lang": lang,
        "tags": tags or [],
        "note": note,
        "created": datetime.now().isoformat(),
        "used": 0,
    }
    snippets.append(snippet)
    save_snippets(snippets)
    print(f"[+] Snippet #{snippet['id']} ({lang}): {title}")


def list_snippets(lang: str = None, tag: str = None) -> None:
    snippets = load_snippets()
    if lang:
        snippets = [s for s in snippets if s.get("lang") == lang]
    if tag:
        snippets = [s for s in snippets if tag in s.get("tags", [])]
    if not snippets:
        print("No snippets found.")
        return
    print(f"{'ID':<4} {'Lang':<10} {'Tags':<20} Title")
    print("-" * 65)
    for s in snippets:
        tags_str = ", ".join(s.get("tags", []))[:18]
        print(f"{s['id']:<4} {s['lang']:<10} {tags_str:<20} {s['title'][:30]}")


def show_snippet(snippet_id: int) -> None:
    snippets = load_snippets()
    match = next((s for s in snippets if s["id"] == snippet_id), None)
    if not match:
        print(f"Snippet #{snippet_id} not found.")
        return
    # Increment usage counter
    for s in snippets:
        if s["id"] == snippet_id:
            s["used"] += 1
    save_snippets(snippets)

    print(f"\n{'='*50}")
    print(f"#{match['id']} — {match['title']}")
    print(f"Lang: {match['lang']}  |  Tags: {', '.join(match.get('tags', []))}")
    if match.get("note"):
        print(f"Note: {match['note']}")
    print(f"{'='*50}")
    print(f"\n```{match['lang']}")
    print(match["code"])
    print("```\n")


def search_snippets(keyword: str) -> None:
    keyword = keyword.lower()
    snippets = load_snippets()
    results = [
        s for s in snippets
        if keyword in s["title"].lower()
        or keyword in s.get("note", "").lower()
        or keyword in s["code"].lower()
        or keyword in " ".join(s.get("tags", [])).lower()
        or keyword == s.get("lang", "").lower()
    ]
    if not results:
        print(f"No snippets found for '{keyword}'.")
        return
    print(f"Found {len(results)} snippet(s):\n")
    for s in results:
        print(f"  #{s['id']} [{s['lang']}] {s['title']}")
        if s.get("note"):
            print(f"       → {s['note']}")


def delete_snippet(snippet_id: int) -> None:
    snippets = load_snippets()
    before = len(snippets)
    snippets = [s for s in snippets if s["id"] != snippet_id]
    if len(snippets) == before:
        print(f"Snippet #{snippet_id} not found.")
    else:
        save_snippets(snippets)
        print(f"Deleted snippet #{snippet_id}.")


def export_snippets(output_file: str = "snippets_export.md", lang: str = None) -> None:
    snippets = load_snippets()
    if lang:
        snippets = [s for s in snippets if s.get("lang") == lang]
    if not snippets:
        print("Nothing to export.")
        return

    lines = [f"# Code Snippets Export\n\n_Generated: {datetime.now().strftime('%Y-%m-%d')}_\n"]
    for s in snippets:
        lines.append(f"\n## #{s['id']} — {s['title']}\n")
        lines.append(f"**Lang:** `{s['lang']}` | **Tags:** {', '.join(s.get('tags', []))}\n")
        if s.get("note"):
            lines.append(f"> {s['note']}\n")
        lines.append(f"\n```{s['lang']}\n{s['code']}\n```\n")

    Path(output_file).write_text("\n".join(lines), encoding="utf-8")
    print(f"Exported {len(snippets)} snippet(s) to {output_file}")


def stats() -> None:
    snippets = load_snippets()
    if not snippets:
        print("No snippets yet.")
        return
    total = len(snippets)
    langs: dict = {}
    tags: dict = {}
    for s in snippets:
        langs[s.get("lang", "?")] = langs.get(s.get("lang", "?"), 0) + 1
        for t in s.get("tags", []):
            tags[t] = tags.get(t, 0) + 1
    top = sorted(snippets, key=lambda s: s.get("used", 0), reverse=True)[:3]

    print(f"Total snippets : {total}")
    print("\nBy language:")
    for lang, n in sorted(langs.items(), key=lambda x: -x[1]):
        print(f"  {lang}: {n}")
    if tags:
        print("\nTop tags:")
        for tag, n in sorted(tags.items(), key=lambda x: -x[1])[:5]:
            print(f"  #{tag}: {n}")
    if top:
        print("\nMost used:")
        for s in top:
            print(f"  #{s['id']} ({s.get('used', 0)}x) {s['title']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Code Snippet Manager CLI")
    sub = parser.add_subparsers(dest="cmd", metavar="command")

    p_add = sub.add_parser("add", help="Save a new code snippet")
    p_add.add_argument("title", help="Short descriptive title")
    p_add.add_argument("code", help="The code snippet")
    p_add.add_argument("--lang", default="python", help="Programming language (default: python)")
    p_add.add_argument("--tags", nargs="*", default=[], help="Space-separated tags")
    p_add.add_argument("--note", default="", help="Optional explanation/context")

    p_list = sub.add_parser("list", help="List saved snippets")
    p_list.add_argument("--lang", help="Filter by language")
    p_list.add_argument("--tag", help="Filter by tag")

    p_show = sub.add_parser("show", help="Display a snippet by ID")
    p_show.add_argument("id", type=int)

    p_search = sub.add_parser("search", help="Search snippets by keyword")
    p_search.add_argument("keyword")

    p_del = sub.add_parser("delete", help="Delete a snippet by ID")
    p_del.add_argument("id", type=int)

    p_export = sub.add_parser("export", help="Export snippets to Markdown")
    p_export.add_argument("--output", default="snippets_export.md")
    p_export.add_argument("--lang", help="Export only this language")

    sub.add_parser("stats", help="Show usage statistics")

    args = parser.parse_args()

    if args.cmd == "add":
        add_snippet(args.title, args.code, args.lang, args.tags, args.note)
    elif args.cmd == "list":
        list_snippets(args.lang, args.tag)
    elif args.cmd == "show":
        show_snippet(args.id)
    elif args.cmd == "search":
        search_snippets(args.keyword)
    elif args.cmd == "delete":
        delete_snippet(args.id)
    elif args.cmd == "export":
        export_snippets(args.output, args.lang)
    elif args.cmd == "stats":
        stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
