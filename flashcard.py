#!/usr/bin/env python3
"""CLI tool for managing study flashcards. Cards are stored in ~/.flashcards.json."""

import json
import random
import argparse
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

CARDS_FILE = Path.home() / ".flashcards.json"


def load_cards() -> list:
    if CARDS_FILE.exists():
        return json.loads(CARDS_FILE.read_text(encoding="utf-8"))
    return []


def save_cards(cards: list) -> None:
    CARDS_FILE.write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")


def next_id(cards: list) -> int:
    return max((c["id"] for c in cards), default=0) + 1


def add_card(question: str, answer: str, tag: str = "general") -> None:
    cards = load_cards()
    card = {
        "id": next_id(cards),
        "question": question,
        "answer": answer,
        "tag": tag,
        "created": datetime.now().isoformat(),
        "correct": 0,
        "reviews": 0,
    }
    cards.append(card)
    save_cards(cards)
    print(f"[+] Card #{card['id']} ({tag}): {question[:60]}")


def list_cards(tag: str = None) -> None:
    cards = load_cards()
    if tag:
        cards = [c for c in cards if c.get("tag") == tag]
    if not cards:
        print("No cards found.")
        return
    print(f"{'ID':<4} {'Tag':<12} {'Score':<8} Question")
    print("-" * 60)
    for c in cards:
        score = f"{c['correct']}/{c['reviews']}" if c["reviews"] else "new"
        print(f"{c['id']:<4} {c['tag']:<12} {score:<8} {c['question'][:40]}")


def quiz(tag: str = None, count: int = 5) -> None:
    cards = load_cards()
    pool = [c for c in cards if c.get("tag") == tag] if tag else cards
    if not pool:
        print("No cards to quiz.")
        return

    # Prioritize cards with lower correct rate
    pool.sort(key=lambda c: (c["correct"] / c["reviews"]) if c["reviews"] else -1)
    session = pool[: min(count, len(pool))]
    random.shuffle(session)

    correct_count = 0
    for i, card in enumerate(session, 1):
        print(f"\n[{i}/{len(session)}] Q: {card['question']}")
        input("  → Press Enter to reveal answer...")
        print(f"  A: {card['answer']}")
        result = input("  Correct? (y/n): ").strip().lower()
        if result == "y":
            correct_count += 1
            card["correct"] += 1
        card["reviews"] += 1

    # Write updated scores back
    id_map = {c["id"]: c for c in session}
    all_cards = load_cards()
    for ac in all_cards:
        if ac["id"] in id_map:
            ac["correct"] = id_map[ac["id"]]["correct"]
            ac["reviews"] = id_map[ac["id"]]["reviews"]
    save_cards(all_cards)

    pct = int(correct_count / len(session) * 100)
    print(f"\nResult: {correct_count}/{len(session)} correct ({pct}%)")


def delete_card(card_id: int) -> None:
    cards = load_cards()
    before = len(cards)
    cards = [c for c in cards if c["id"] != card_id]
    if len(cards) == before:
        print(f"Card #{card_id} not found.")
    else:
        save_cards(cards)
        print(f"Deleted card #{card_id}.")


def stats() -> None:
    cards = load_cards()
    if not cards:
        print("No cards yet.")
        return
    total = len(cards)
    reviewed = [c for c in cards if c["reviews"] > 0]
    new = total - len(reviewed)
    avg = sum(c["correct"] / c["reviews"] for c in reviewed) / len(reviewed) if reviewed else 0
    tags = {}
    for c in cards:
        tags[c.get("tag", "general")] = tags.get(c.get("tag", "general"), 0) + 1
    print(f"Total cards : {total}")
    print(f"New (unseen): {new}")
    print(f"Avg accuracy: {avg:.0%}")
    print("By tag:")
    for tag, n in sorted(tags.items()):
        print(f"  {tag}: {n}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Flashcard CLI for learning")
    sub = parser.add_subparsers(dest="cmd", metavar="command")

    p_add = sub.add_parser("add", help="Add a new flashcard")
    p_add.add_argument("question")
    p_add.add_argument("answer")
    p_add.add_argument("--tag", default="general", help="Topic tag (default: general)")

    p_list = sub.add_parser("list", help="List flashcards")
    p_list.add_argument("--tag", help="Filter by tag")

    p_quiz = sub.add_parser("quiz", help="Start a quiz session")
    p_quiz.add_argument("--tag", help="Limit to a tag")
    p_quiz.add_argument("--count", type=int, default=5, help="Number of cards (default: 5)")

    p_del = sub.add_parser("delete", help="Delete a card by ID")
    p_del.add_argument("id", type=int)

    sub.add_parser("stats", help="Show statistics")

    args = parser.parse_args()

    if args.cmd == "add":
        add_card(args.question, args.answer, args.tag)
    elif args.cmd == "list":
        list_cards(args.tag)
    elif args.cmd == "quiz":
        quiz(args.tag, args.count)
    elif args.cmd == "delete":
        delete_card(args.id)
    elif args.cmd == "stats":
        stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
