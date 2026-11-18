#!/usr/bin/env python3
"""news-image-20261118 — reproduce the competition entry image (v6-hdmap).

Reads ``entry.png`` sitting next to this script, validates the PNG
structure (magic bytes, IHDR 1024x1024 8-bit RGB, every chunk CRC,
IEND present, no trailing bytes, total size at most 1 MiB), checks its
SHA-256 against the value recorded below, copies it byte-for-byte to
``/output/entry.png`` (or to the path given on the command line),
re-reads the written file and confirms the SHA-256 matches.

Python 3.13, standard library only — no PIL, no third-party packages.

Usage:
    python3 main.py [output_path]
    python3 main.py --check-only

    With no argument the image is written to /output/entry.png.
    With one argument it is written to that path instead; the parent
    directory is created when missing. With --check-only the image is
    validated and its SHA-256 reported, but no output file is written.
"""

import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "5a2114aa2751984f303452f9ae879b2e9aed551c9383a910f434d5fe20bd28f4"
EXPECTED_SIZE = 406087
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
EXPECTED_BIT_DEPTH = 8
EXPECTED_COLOR_TYPE = 2  # truecolour (RGB)
MAX_SIZE_BYTES = 1024 * 1024  # 1 MiB
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
DEFAULT_OUTPUT = "/output/entry.png"


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_chunk(data: bytes, offset: int):
    """Return (type, payload, next_offset) for the chunk at offset."""
    if offset + 8 > len(data):
        raise ValueError("truncated PNG chunk header at offset %d" % offset)
    (length,) = struct.unpack(">I", data[offset:offset + 4])
    chunk_type = data[offset + 4:offset + 8]
    body_start = offset + 8
    body_end = body_start + length
    if body_end + 4 > len(data):
        raise ValueError("truncated PNG chunk %r" % chunk_type)
    body = data[body_start:body_end]
    (stored_crc,) = struct.unpack(">I", data[body_end:body_end + 4])
    actual_crc = zlib.crc32(chunk_type + body) & 0xFFFFFFFF
    if actual_crc != stored_crc:
        raise ValueError(
            "CRC mismatch in chunk %r: stored %#010x, computed %#010x"
            % (chunk_type, stored_crc, actual_crc)
        )
    return chunk_type, body, body_end + 4


def validate_png(data: bytes) -> int:
    """Validate the PNG; return the number of chunks seen.

    Raises ValueError on any structural problem.
    """
    if len(data) > MAX_SIZE_BYTES:
        raise ValueError(
            "entry.png too large: %d bytes (limit %d)"
            % (len(data), MAX_SIZE_BYTES)
        )
    if len(data) < 8 or data[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file: bad magic bytes")

    offset = 8
    chunks = 0
    seen_ihdr = False
    seen_iend = False
    while offset < len(data):
        chunk_type, body, offset = _read_chunk(data, offset)
        chunks += 1
        if chunk_type == b"IHDR":
            if seen_ihdr:
                raise ValueError("duplicate IHDR chunk")
            if len(body) != 13:
                raise ValueError("IHDR has wrong length: %d" % len(body))
            width, height, bit_depth, color_type = struct.unpack(
                ">IIBB", body[:10]
            )
            if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
                raise ValueError(
                    "IHDR dimensions %dx%d, expected %dx%d"
                    % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT)
                )
            if bit_depth != EXPECTED_BIT_DEPTH:
                raise ValueError(
                    "IHDR bit depth %d, expected %d"
                    % (bit_depth, EXPECTED_BIT_DEPTH)
                )
            if color_type != EXPECTED_COLOR_TYPE:
                raise ValueError(
                    "IHDR colour type %d, expected %d (RGB)"
                    % (color_type, EXPECTED_COLOR_TYPE)
                )
            seen_ihdr = True
        elif chunk_type == b"IEND":
            if len(body) != 0:
                raise ValueError("IEND has wrong length: %d" % len(body))
            seen_iend = True
            break

    if not seen_ihdr:
        raise ValueError("missing IHDR chunk")
    if not seen_iend:
        raise ValueError("missing IEND chunk")
    if offset != len(data):
        raise ValueError(
            "trailing bytes after IEND: %d" % (len(data) - offset)
        )
    return chunks


def resolve_output_path(argv) -> tuple:
    """Parse argv into (output_path, check_only).

    Accepts at most one positional output path and the optional
    ``--check-only`` flag (in either order). With no positional path
    the default /output/entry.png is used; in check-only mode the
    returned path is None because nothing is written.
    """
    check_only = False
    positional = []
    for arg in argv:
        if arg == "--check-only":
            check_only = True
        elif arg.startswith("--"):
            raise ValueError("unknown option %r" % arg)
        else:
            positional.append(arg)
    if len(positional) > 1:
        raise ValueError(
            "too many arguments: usage: python3 main.py [--check-only] "
            "[output_path]"
        )
    if check_only:
        return None, True
    if positional:
        if not positional[0]:
            raise ValueError("output_path must not be empty")
        return positional[0], False
    return DEFAULT_OUTPUT, False


def prepare_output_dir(output_path: str) -> str:
    """Create the output parent directory and check it is writable."""
    out_dir = os.path.dirname(os.path.abspath(output_path)) or "."
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        raise ValueError(
            "cannot create output directory %r: %s" % (out_dir, exc)
        ) from exc
    if not os.path.isdir(out_dir):
        raise ValueError(
            "output directory %r does not exist and could not be created"
            % out_dir
        )
    if not os.access(out_dir, os.W_OK):
        raise ValueError("output directory %r is not writable" % out_dir)
    return out_dir


def main(argv=None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    output_path, check_only = resolve_output_path(argv)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    entry_path = os.path.join(script_dir, "entry.png")

    with open(entry_path, "rb") as handle:
        data = handle.read()

    if len(data) != EXPECTED_SIZE:
        raise ValueError(
            "entry.png size %d bytes, expected %d"
            % (len(data), EXPECTED_SIZE)
        )

    chunk_count = validate_png(data)

    digest = sha256_hex(data)
    if digest != EXPECTED_SHA256:
        raise ValueError(
            "SHA-256 mismatch for entry.png:\n"
            "  got      %s\n"
            "  expected %s" % (digest, EXPECTED_SHA256)
        )

    print("entry.png: %d bytes, %d chunks validated" % (len(data), chunk_count))
    print("sha256: %s" % digest)

    if check_only:
        print("OK: entry.png is valid (check-only, nothing written)")
        return 0

    prepare_output_dir(output_path)
    try:
        with open(output_path, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        raise ValueError(
            "cannot write output file %r: %s" % (output_path, exc)
        ) from exc

    with open(output_path, "rb") as handle:
        out_data = handle.read()
    out_digest = sha256_hex(out_data)
    if out_digest != digest:
        raise ValueError(
            "output SHA-256 mismatch: %s != %s" % (out_digest, digest)
        )

    print(
        "output: %s (%d bytes, sha256 %s)"
        % (output_path, len(out_data), out_digest)
    )
    print("OK: output is byte-identical to entry.png")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        sys.exit(1)
