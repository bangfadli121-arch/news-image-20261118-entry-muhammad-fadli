#!/usr/bin/env python3
"""Copy the news-image-20261118 entry image to the output directory.

The image lives in this repository as entry.png. The program checks it is
really the entry image -- a complete PNG, 1024x1024, 8-bit true colour,
no more than 1 MiB, with the expected sha256 -- and then copies it to
``<output>/entry.png``. The output is re-read and compared with the input,
so the printed digest proves the run produced exactly the shipped bytes.

Run locally with an output directory of your choice:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

With no MAKEFUN_OUTPUT_DIR set, the program writes to /output, the path
the grader uses. Only the Python standard library is used: there is no
network access, no clock and no randomness, so every run is identical.
"""

import hashlib
import os
import shutil
import struct
import sys
import zlib

SIGNATURE = b"\x89PNG\r\n\x1a\n"
SIZE_LIMIT = 1_048_576
SIZE = (1024, 1024)
DIGEST = "e781f22b8623980e557d65a1ee2780f9161f8d30f28b2f525eb72ac93224de70"


def abort(reason):
    """Print a validation failure and stop with a non-zero status."""
    print("error: " + reason, file=sys.stderr)
    raise SystemExit(1)


def chunks(blob):
    """Yield (kind, payload) for each chunk of a PNG byte string.

    Raises through abort() when the chunk framing is broken or a stored
    CRC does not match the bytes it covers.
    """
    pos = 8
    while pos < len(blob):
        if pos + 8 > len(blob):
            abort("truncated chunk header at offset %d" % pos)
        (size,) = struct.unpack(">I", blob[pos:pos + 4])
        kind = blob[pos + 4:pos + 8]
        stop = pos + 8 + size + 4
        if stop > len(blob):
            abort("chunk %r runs past the end of the file" % kind)
        (stored_crc,) = struct.unpack(">I", blob[pos + 8 + size:stop])
        crc = zlib.crc32(blob[pos + 4:pos + 8 + size]) & 0xFFFFFFFF
        if crc != stored_crc:
            abort("chunk %r fails its CRC check" % kind)
        yield kind, blob[pos + 8:pos + 8 + size]
        if kind == b"IEND":
            if stop != len(blob):
                abort("bytes follow the IEND chunk")
            return
        pos = stop
    abort("no IEND chunk found")


def inspect(blob):
    """Return (width, height) after checking the whole PNG is sound."""
    if len(blob) > SIZE_LIMIT:
        abort("entry.png is %d bytes, above the 1 MiB cap" % len(blob))
    if len(blob) < 33 or blob[:8] != SIGNATURE:
        abort("entry.png lacks the PNG signature")

    seen = list(chunks(blob))
    kinds = [kind for kind, _ in seen]
    if not kinds or kinds[0] != b"IHDR":
        abort("entry.png does not open with an IHDR chunk")
    if kinds[-1] != b"IEND":
        abort("entry.png does not close with an IEND chunk")
    if kinds.count(b"IHDR") != 1:
        abort("entry.png carries more than one IHDR chunk")

    header = seen[0][1]
    if len(header) != 13:
        abort("IHDR chunk is %d bytes, expected 13" % len(header))
    width, height = struct.unpack(">II", header[0:8])
    if (width, height) != SIZE:
        abort("entry.png is %dx%d, expected 1024x1024" % (width, height))
    if header[8] != 8 or header[9] not in (2, 6):
        abort("entry.png is not 8-bit true colour (depth %d, type %d)"
              % (header[8], header[9]))
    return width, height


def run():
    base = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(base, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dest = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(source):
        abort("entry.png is missing from the repository")

    with open(source, "rb") as handle:
        blob = handle.read()
    width, height = inspect(blob)

    digest = hashlib.sha256(blob).hexdigest()
    if digest != DIGEST:
        abort("entry.png digest %s does not match the entry" % digest)

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, dest)

    with open(dest, "rb") as handle:
        copied = handle.read()
    if copied != blob:
        abort("the copied file differs from entry.png")

    print("entry.png: %dx%d, %d bytes, sha256 %s"
          % (width, height, len(copied), digest))


if __name__ == "__main__":
    run()
