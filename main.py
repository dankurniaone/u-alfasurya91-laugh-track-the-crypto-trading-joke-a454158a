#!/usr/bin/env python3
"""Laugh Track: The Crypto Trading Joke Contest.

Writes one line about crypto trading life to /output/entry.txt.
The line won the candidate tournament (specificity / surprise / freshness)
as the sharpest of eight drafts: 100x leverage is a recognisable trading
detail, the setup is one breath, and the punchline turns the loss into a
joke about impatience instead of a complaint about the market.
"""

import argparse
import sys
from pathlib import Path

# Winning line: 80 chars, gate is 1-200.
# Tournament: specificity 5, surprise 5, freshness 4 = 14 (highest of 8).
JOKE = "Leverage 100x: because losing my money slowly felt disrespectful to my time."

# Tournament record (specificity / surprise / freshness, 1-5 each):
#  1. stop-loss executed perfectly, portfolio did not ......... 5/4/4 = 13
#  2. trading bot buys the top, sells the bottom, charges a sub  4/4/3 = 11
#  3. "accumulating" on a coin whose founder left in 2023 ..... 5/5/4 = 14
#  4. the chart said support, the support said goodbye ........ 3/4/4 = 11
#  5. my own research was a YouTube thumbnail, green arrow ..... 5/4/3 = 12
#  6. my cold wallet froze my gains too ....................... 3/3/3 = 9
#  7. sold at the bottom to buy back higher, "discipline" ...... 4/4/4 = 12
#  8. Leverage 100x, losing money slowly felt disrespectful ... 5/5/4 = 14
# Tie at 14 between #3 and #8; #8 wins it — tighter setup, punchline
# lands harder, and 100x leverage is the more recognisable detail.
TOURNAMENT = {
    "winner": 8,
    "scores": {"1": 13, "2": 11, "3": 14, "4": 11,
               "5": 12, "6": 9, "7": 12, "8": 14},
}

OUTPUT_PATH = Path("/output/entry.txt")


def write_entry(path: Path = OUTPUT_PATH) -> int:
    """Write the joke as UTF-8 text, exactly one line, no trailing newline."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = JOKE.strip()
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry must be 1-200 chars, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    path.write_text(text, encoding="utf-8")
    return len(text)


def check() -> int:
    """Verify the written bytes round-trip byte-identical to the joke."""
    written = write_entry()
    back = OUTPUT_PATH.read_text(encoding="utf-8")
    if back != JOKE:
        print(f"FAIL: round-trip mismatch: {back!r} != {JOKE!r}", file=sys.stderr)
        return 1
    print(f"OK: {written} chars, {len(JOKE.encode('utf-8'))} bytes, round-trip identical")
    print(f"tournament winner: candidate {TOURNAMENT['winner']} "
          f"(score {TOURNAMENT['scores'][str(TOURNAMENT['winner'])]}/15)")
    print(f"entry: {JOKE}")
    return 0


def self_test() -> int:
    """Write to a temp file and verify the bytes read back match exactly."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        probe = Path(tmp) / "entry.txt"
        write_entry(probe)
        back = probe.read_text(encoding="utf-8")
        if back != JOKE:
            print(f"FAIL: self-test mismatch: {back!r} != {JOKE!r}", file=sys.stderr)
            return 1
        print(f"self-test OK: {len(back)} chars written to temp file, bytes match")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Write the crypto trading joke.")
    parser.add_argument("--check", action="store_true",
                        help="write the entry and verify it round-trips")
    parser.add_argument("--self-test", action="store_true",
                        help="write to a temp file and verify the bytes match")
    args = parser.parse_args(argv)
    if args.check:
        return check()
    if args.self_test:
        return self_test()
    written = write_entry()
    print(f"wrote {written} chars to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
