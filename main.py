#!/usr/bin/env python3
"""news-image-20261118 — reproduce the competition entry image.

Reads entry.png next to this script, validates it (PNG magic, IHDR
1024x1024, per-chunk CRC, IEND present, size <= 1 MiB), checks its
SHA-256 against the expected value recorded below, then copies it
byte-for-byte to /output/entry.png and re-reads the output to confirm
the SHA-256 is identical.

Python 3.13, standard library only — no PIL, no third-party packages.

Usage:
    python3 main.py [output_path]

    output_path defaults to /output/entry.png when omitted. When given,
    the validated entry image is written to that path instead; its
    parent directory is created if needed (and must be writable).
"""

import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "69da07cdd67723144390dcbc2d81593b8c67a4c92bcb0028eb065145d68d9f7c"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_SIZE_BYTES = 1 * 1024 * 1024  # 1 MiB
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.png")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_png(data: bytes) -> None:
    """Validate PNG structure: magic, IHDR 1024x1024, chunk CRCs, IEND."""
    if len(data) > MAX_SIZE_BYTES:
        raise ValueError(
            f"entry.png too large: {len(data)} bytes (limit {MAX_SIZE_BYTES})"
        )
    if len(data) < 8 or data[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file: bad magic bytes")

    offset = 8
    seen_ihdr = False
    seen_iend = False

    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError("truncated PNG chunk header")
        (length,) = struct.unpack(">I", data[offset : offset + 4])
        chunk_type = data[offset + 4 : offset + 8]
        chunk_start = offset + 8
        chunk_end = chunk_start + length
        if chunk_end + 4 > len(data):
            raise ValueError(f"truncated PNG chunk: {chunk_type!r}")
        chunk_data = data[chunk_start:chunk_end]
        (stored_crc,) = struct.unpack(">I", data[chunk_end : chunk_end + 4])
        actual_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if actual_crc != stored_crc:
            raise ValueError(
                f"CRC mismatch in chunk {chunk_type!r}: "
                f"stored {stored_crc:#010x}, computed {actual_crc:#010x}"
            )

        if chunk_type == b"IHDR":
            if seen_ihdr:
                raise ValueError("duplicate IHDR chunk")
            if length != 13:
                raise ValueError(f"IHDR has wrong length: {length}")
            width, height = struct.unpack(">II", chunk_data[:8])
            if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
                raise ValueError(
                    f"IHDR dimensions {width}x{height}, "
                    f"expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
                )
            seen_ihdr = True
        elif chunk_type == b"IEND":
            if length != 0:
                raise ValueError(f"IEND has wrong length: {length}")
            seen_iend = True
            offset = chunk_end + 4
            break

        offset = chunk_end + 4

    if not seen_ihdr:
        raise ValueError("missing IHDR chunk")
    if not seen_iend:
        raise ValueError("missing IEND chunk")
    if offset != len(data):
        raise ValueError(f"trailing bytes after IEND: {len(data) - offset}")


def resolve_output_path(argv) -> str:
    """Resolve the output path from argv.

    ``argv`` holds the command-line arguments after the script name.
    At most one argument is accepted: an explicit output file path.
    With no argument the default /output/entry.png is used.
    """
    if len(argv) > 1:
        raise ValueError(
            "too many arguments: usage: python3 main.py [output_path]"
        )
    if len(argv) == 1:
        output_path = argv[0]
        if not output_path:
            raise ValueError("output_path must not be empty")
        return output_path
    return OUTPUT_PATH


def ensure_output_dir_writable(output_path: str) -> str:
    """Create the output file's parent directory and check it is writable.

    Returns the directory path. Raises ValueError with a clear message
    when the directory cannot be created or is not writable, so the
    failure is reported before any bytes are written.
    """
    out_dir = os.path.dirname(os.path.abspath(output_path)) or "."
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        raise ValueError(
            f"cannot create output directory {out_dir!r}: {exc}"
        ) from exc
    if not os.path.isdir(out_dir):
        raise ValueError(
            f"output directory {out_dir!r} does not exist "
            f"and could not be created"
        )
    if not os.access(out_dir, os.W_OK):
        raise ValueError(
            f"output directory {out_dir!r} is not writable"
        )
    return out_dir


def main(argv=None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    output_path = resolve_output_path(argv)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    entry_path = os.path.join(script_dir, "entry.png")

    with open(entry_path, "rb") as f:
        data = f.read()

    validate_png(data)

    digest = sha256_hex(data)
    if digest != EXPECTED_SHA256:
        raise ValueError(
            f"SHA-256 mismatch for entry.png:\n"
            f"  got      {digest}\n"
            f"  expected {EXPECTED_SHA256}"
        )

    ensure_output_dir_writable(output_path)
    try:
        with open(output_path, "wb") as f:
            f.write(data)
    except OSError as exc:
        raise ValueError(
            f"cannot write output file {output_path!r}: {exc}"
        ) from exc

    with open(output_path, "rb") as f:
        out_data = f.read()
    out_digest = sha256_hex(out_data)
    if out_digest != digest:
        raise ValueError(
            f"output SHA-256 mismatch: {out_digest} != {digest}"
        )

    print(f"entry.png: {len(data)} bytes")
    print(f"sha256: {digest}")
    print(f"output: {output_path} ({len(out_data)} bytes, sha256 {out_digest})")
    print("OK: output is byte-identical to entry.png")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
