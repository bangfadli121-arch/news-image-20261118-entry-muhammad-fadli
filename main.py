#!/usr/bin/env python3
"""Emit the 18 November 2026 world-news front page.

``entry.png`` in this repository is the whole entry: a single 1024x1024
photographic newspaper front page summing up one day of world news.
This script does not draw anything. It proves the shipped file is the
real entry -- a well-formed PNG of the right size and the exact bytes
we submitted -- and then places an identical copy at the output path
the grader reads.

Behaviour, by design:

* only the Python standard library is imported (no network, no clock,
  no randomness, no third-party packages), so the program runs in the
  bare harness sandbox;
* the output directory comes from ``MAKEFUN_OUTPUT_DIR`` and falls back
  to ``/output``;
* every run prints one line with the size and sha256 of the emitted
  file, and two runs into different directories produce byte-identical
  files.

Usage::

    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import struct
import sys
import zlib

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
EXPECTED_W = 1024
EXPECTED_H = 1024
EXPECTED_SHA256 = (
    "02ef0be82e86b96b98e526e33877d75a6a32a394d6ab431806daa8e8fdd57de0"
)


def die(message):
    """Report a failed check on stderr and stop with a nonzero exit."""
    print("error: %s" % message, file=sys.stderr)
    sys.exit(1)


class PngReader:
    """Walk a PNG byte string chunk by chunk, checking its framing."""

    def __init__(self, data):
        self.data = data
        self.offset = len(PNG_MAGIC)
        self.chunk_kinds = []
        self.header = None

    def next_chunk(self):
        """Return the next (kind, payload) pair, or None past IEND."""
        data = self.data
        pos = self.offset
        if pos + 8 > len(data):
            die("PNG ends inside a chunk header at byte %d" % pos)
        (payload_len,) = struct.unpack_from(">I", data, pos)
        kind = data[pos + 4:pos + 8]
        end = pos + 8 + payload_len + 4
        if end > len(data):
            die("chunk %s overruns the file" % kind.decode("latin-1"))
        (stored,) = struct.unpack_from(">I", data, pos + 8 + payload_len)
        actual = zlib.crc32(data[pos + 4:pos + 8 + payload_len]) & 0xFFFFFFFF
        if actual != stored:
            die("chunk %s has a bad CRC" % kind.decode("latin-1"))
        self.chunk_kinds.append(kind)
        self.offset = end
        return kind, data[pos + 8:pos + 8 + payload_len]

    def walk(self):
        """Consume every chunk; return the IHDR payload."""
        if self.data[:8] != PNG_MAGIC:
            die("file does not start with the PNG magic bytes")
        while True:
            kind, payload = self.next_chunk()
            if kind == b"IHDR":
                if self.header is not None:
                    die("PNG has two IHDR chunks")
                if len(payload) != 13:
                    die("IHDR payload is %d bytes, want 13" % len(payload))
                self.header = payload
            if kind == b"IEND":
                if self.offset != len(self.data):
                    die("trailing bytes after the IEND chunk")
                break
        return self.header


def check_image(data):
    """Validate the candidate entry bytes; return (width, height)."""
    if len(data) > MAX_BYTES:
        die("entry image is %d bytes, over the 1 MiB limit" % len(data))
    if len(data) < 8 + 25 + 12:
        die("entry image is too short to be a PNG")
    reader = PngReader(data)
    header = reader.walk()
    kinds = reader.chunk_kinds
    if not kinds or kinds[0] != b"IHDR":
        die("first chunk is not IHDR")
    if kinds[-1] != b"IEND":
        die("last chunk is not IEND")
    width, height = struct.unpack_from(">II", header, 0)
    if (width, height) != (EXPECTED_W, EXPECTED_H):
        die("image is %dx%d, want 1024x1024" % (width, height))
    depth, colour = header[8], header[9]
    if depth != 8 or colour not in (2, 6):
        die("image is not 8-bit RGB/RGBA (depth %d, colour %d)"
            % (depth, colour))
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dst = os.path.join(out_dir, "entry.png")

    try:
        with open(src, "rb") as handle:
            raw = handle.read()
    except OSError:
        die("cannot read entry.png from the repository")

    width, height = check_image(raw)

    fingerprint = hashlib.sha256(raw).hexdigest()
    if fingerprint != EXPECTED_SHA256:
        die("sha256 %s is not the submitted entry" % fingerprint)

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)

    with open(dst, "rb") as handle:
        emitted = handle.read()
    if emitted != raw:
        die("output file differs from entry.png")

    print("entry.png: %dx%d, %d bytes, sha256 %s"
          % (width, height, len(emitted), fingerprint))


if __name__ == "__main__":
    main()
