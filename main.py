"""Funniest Lost Sock Status Update — make.fun bounty entry.

Writes a single status update, in the voice of a lost sock, to
/output/entry.txt (or the path resolved from the environment).

Stdlib only. Deterministic bytes on every run: no trailing newline.
"""

import os

LINE = (
    "I'm a sock in a library book, page 247. Someone dog-eared me. "
    "Fourteen reads in and I still don't know whodunit."
)


def output_path():
    """Resolve where entry.txt goes, without depending on the cwd.

    Precedence: ENTRY_OUTPUT, then OUTPUT_DIR / MAKEFUN_OUTPUT_DIR
    joined with entry.txt, then /output/entry.txt when that directory
    exists, else next to this script.
    """
    direct = os.environ.get("ENTRY_OUTPUT")
    if direct:
        return direct
    for name in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        folder = os.environ.get(name)
        if folder:
            return os.path.join(folder, "entry.txt")
    if os.path.isdir("/output"):
        return "/output/entry.txt"
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.txt")


def main():
    if not 1 <= len(LINE) <= 120:
        raise SystemExit("entry fails the 1-120 character gate")
    if not LINE.strip():
        raise SystemExit("entry is blank")
    encoded = LINE.encode("utf-8")
    if encoded.decode("utf-8") != LINE:
        raise SystemExit("entry fails UTF-8 round-trip")
    if any(byte < 0x20 or byte == 0x7F for byte in encoded):
        raise SystemExit("entry contains a control character")
    path = output_path()
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    os.chmod(path, 0o644)
    with open(path, "rb") as handle:
        data = handle.read()
    if data != LINE.encode("utf-8"):
        raise SystemExit("read-back mismatch: bytes differ from entry")
    if b"\n" in data or b"\r" in data:
        raise SystemExit("read-back mismatch: entry must be one line")


if __name__ == "__main__":
    main()
