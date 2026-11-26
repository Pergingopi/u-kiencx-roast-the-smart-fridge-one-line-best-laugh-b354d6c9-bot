#!/usr/bin/env python3
"""One-line roast of the smart fridge that shares my house.

The program writes a single roast line to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default ``/output/entry.txt``) and
nothing else. The line is checked twice -- once before it is written
and once after it is read back from disk -- so an invalid entry can
never slip through: it must be one line, 1-160 characters, not
whitespace-only, and free of characters a reader cannot see.

Publishing is atomic. The text is staged in a temporary file inside
the output directory (never in /tmp, where a bind-mounted output
directory would make the rename fail), flushed to disk, and only then
moved into place with ``os.replace``. The finished file is left with
mode 0644.
"""

import os
import sys
import unicodedata

# The roast: the fridge rats me out with a push notification every
# time I open it at 2 a.m. -- a snitch with a light inside, and no
# loyalty whatsoever.
ENTRY = (
    "My smart fridge sends me a push notification every time I open it "
    "at 2 a.m., like a snitch with a light inside and no loyalty."
)

MAX_CHARS = 160
OUTPUT_NAME = "entry.txt"
STAGING_NAME = ".entry.txt.tmp"


def _is_hidden_character(ch):
    """True for a character that counts for the scorer but not the eye.

    C1 controls (U+0080-U+009F), the byte-order mark, the Unicode line
    and paragraph separators, surrogates, and any other control,
    format, or non-spacing mark are all invisible to a reader, so any
    one of them disqualifies the line. An ordinary space is the only
    separator allowed through.
    """
    code = ord(ch)
    if 0x0080 <= code <= 0x009F:
        return True
    if ch in ("\ufeff", "\u2028", "\u2029"):
        return True
    category = unicodedata.category(ch)
    if category in ("Cc", "Cf", "Cs", "Zl", "Zp"):
        return True
    if category == "Zs" and ch != " ":
        return True
    return False


def _check_shape(text):
    """Reject a line that fails the gate on size or structure."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text or not text.strip():
        raise ValueError("entry is empty or whitespace-only")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def _check_characters(text):
    """Reject a line carrying any character a reader cannot see."""
    for ch in text:
        if _is_hidden_character(ch):
            raise ValueError(
                "entry contains invisible character U+%04X" % ord(ch)
            )


def validate(text):
    """Raise ValueError unless *text* is a single valid roast line."""
    _check_shape(text)
    _check_characters(text)
    return text


def _sweep_output_dir(path):
    """Delete stale files inside *path*; the directory itself remains."""
    for name in os.listdir(path):
        full = os.path.join(path, name)
        if os.path.isfile(full) or os.path.islink(full):
            os.unlink(full)


def _publish_atomically(out_dir, text):
    """Stage, fsync, and atomically move *text* into ``entry.txt``."""
    payload = text.encode("utf-8")
    target = os.path.join(out_dir, OUTPUT_NAME)
    staging = os.path.join(out_dir, STAGING_NAME)
    with open(staging, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(staging, 0o644)
    os.replace(staging, target)
    os.chmod(target, 0o644)
    return target


def _read_back_and_verify(target, expected):
    """Re-read *target* from disk and confirm it matches *expected*."""
    with open(target, "rb") as handle:
        landed = handle.read().decode("utf-8")
    validate(landed)
    if landed != expected:
        raise ValueError("read-back mismatch after publish")
    return landed


def _resolve_output_dir():
    """Return the output directory, creating it if it is missing.

    The harness sets MAKEFUN_OUTPUT_DIR; running the program by hand
    falls back to /output. The directory itself is never removed --
    only its stale contents are swept -- because the harness may have
    bind-mounted it.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def main():
    out_dir = _resolve_output_dir()
    _sweep_output_dir(out_dir)

    text = validate(ENTRY)
    target = _publish_atomically(out_dir, text)
    _read_back_and_verify(target, text)

    print("wrote %s (%d characters)" % (target, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
