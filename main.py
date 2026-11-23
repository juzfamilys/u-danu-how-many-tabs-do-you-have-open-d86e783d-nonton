"""How Many Tabs Do You Have Open? — make.fun entry.

Writes a single honest tab count — the digits ``137`` and nothing else —
to ``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default ``/output``).

Why 137: it is the real count of a chronic tab hoarder. Three browser
windows: one full of half-read docs and Stack Overflow answers, one of
shopping carts and flight tabs never booked, one of articles saved
"for later" since last year. It is high enough to surprise, odd and
specific enough to read as a number somebody actually counted (nobody
invents 137 as a round guess), and small enough to stay believable —
a life lived in browser tabs, not a number picked to shock.

Gate: the entry file must be UTF-8 text of 1 to 5 characters, not only
white space. ``137`` is 3 bytes, digits only, no trailing newline.

Pure Python standard library. Deterministic: the same bytes on every run.
"""

import os
import sys

# The honest count of open browser tabs at the moment of the build.
COUNT = 137

# The entry text: digits only, no words, no punctuation, no newline.
ENTRY = str(COUNT)


def validate_entry(text: str) -> None:
    """Enforce the competition gate before anything is written."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not 1 <= len(text) <= 5:
        raise ValueError(
            "entry must be 1 to 5 characters, got %d" % len(text)
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if not text.isascii() or not text.isdigit():
        raise ValueError("entry must be digits only, got %r" % text)
    # Guard the count itself: a real tab count is positive, and a number
    # with a leading zero ("0137") would not read as an honest count.
    if text != str(int(text)):
        raise ValueError("entry must be a plain integer, got %r" % text)
    if not 1 <= int(text) <= 99999:
        raise ValueError("tab count out of believable range: %r" % text)


def main() -> int:
    validate_entry(ENTRY)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    entry_path = os.path.join(output_dir, "entry.txt")

    with open(entry_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)

    # Read back what landed on disk and re-validate the exact bytes.
    with open(entry_path, "rb") as handle:
        landed = handle.read()
    if landed != ENTRY.encode("utf-8"):
        raise ValueError(
            "entry on disk %r does not match expected %r"
            % (landed, ENTRY.encode("utf-8"))
        )
    validate_entry(landed.decode("utf-8"))

    print("Wrote %d tabs to %s (%d bytes)" % (COUNT, entry_path, len(landed)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
