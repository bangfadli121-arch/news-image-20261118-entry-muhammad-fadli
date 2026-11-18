"""news-image-20261118 entry program (Python 3.13, standard library only).

The entry image is the entry.png held in this repository. The program copies
it to the output directory as entry.png, after validating that it is a whole
PNG of 1024 by 1024 pixels and at most 1 MiB, and prints its sha256.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Deterministic: no network, no clock, no randomness; the same input bytes
always produce the same output bytes.
"""

import hashlib
import os
import shutil
import struct
import sys
import zlib

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def fail(message):
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def validate_png(data):
    """Check the bytes are a whole PNG with the expected size and dimensions."""
    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if data[:8] != PNG_MAGIC:
        fail("entry.png does not start with the PNG magic bytes")
    if len(data) < 33:
        fail("entry.png is too short to hold a PNG header")

    # IHDR chunk: length (4), type (4), width (4), height (4), ...
    ihdr_length = struct.unpack(">I", data[8:12])[0]
    ihdr_type = data[12:16]
    if ihdr_type != b"IHDR" or ihdr_length != 13:
        fail("entry.png has no valid IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail("entry.png is %dx%d, expected 1024x1024" % (width, height))
    bit_depth, color_type = data[24], data[25]
    if bit_depth != 8 or color_type not in (2, 6):
        fail("entry.png has unexpected IHDR bit depth %d / color type %d"
             % (bit_depth, color_type))

    # Every chunk must carry a correct CRC, and the file must end with IEND.
    offset = 8
    seen_iend = False
    while offset < len(data):
        if offset + 8 > len(data):
            fail("entry.png ends in the middle of a chunk header")
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk_type = data[offset + 4:offset + 8]
        end = offset + 8 + length + 4
        if end > len(data):
            fail("entry.png ends in the middle of chunk %r" % chunk_type)
        stored_crc = struct.unpack(">I", data[offset + 8 + length:end])[0]
        actual_crc = zlib.crc32(data[offset + 4:offset + 8 + length]) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            fail("entry.png chunk %r has a bad CRC" % chunk_type)
        if chunk_type == b"IEND":
            seen_iend = True
            if end != len(data):
                fail("entry.png has trailing bytes after IEND")
            break
        offset = end
    if not seen_iend:
        fail("entry.png has no IEND chunk")

    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    output = os.path.join(output_dir, "entry.png")

    if not os.path.isfile(source):
        fail("entry.png not found beside main.py")

    with open(source, "rb") as handle:
        data = handle.read()
    width, height = validate_png(data)

    os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(source, output)

    with open(output, "rb") as handle:
        written = handle.read()
    if written != data:
        fail("output bytes differ from entry.png")

    digest = hashlib.sha256(written).hexdigest()
    print("entry.png: %dx%d, %d bytes, sha256 %s" % (width, height, len(written), digest))


if __name__ == "__main__":
    main()
