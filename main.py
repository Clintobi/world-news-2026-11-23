#!/usr/bin/env python3
"""
make.fun bounty "news-image-20261123" entry.

Sums up the world's news of Monday 23 November 2026 in one image.
The image (entry_image.png, held in this repository) was composed from
the day's wire reporting (AP, BBC, Reuters, Al Jazeera, ESA, Dawn/IQAir)
as a magazine cover: the Strait of Hormuz tanker attacks as the lead,
pictured panels on the Russian warship down at Benghazi, BepiColombo
reaching Mercury and Lahore's record smog, and a breadth line covering
COP31's collapse, the boy pulled alive near Kyiv, the Democrats' House
majority and the AI rout in Asian markets.

This program writes that image to /output/entry.png, byte for byte,
using only the Python standard library. It is deterministic: every run
writes identical bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry_image.png")
OUTPUT = "/output/entry.png"


MAX_BYTES = 1_048_576  # the bounty caps the image at 1 MiB


def check_source() -> None:
    """Fail loudly rather than write an entry the gate would reject."""
    with open(SOURCE, "rb") as fh:
        head = fh.read(8)
    size = os.path.getsize(SOURCE)
    is_png = head.startswith(b"\x89PNG\r\n\x1a\n")
    is_jpeg = head.startswith(b"\xff\xd8\xff")
    if not (is_png or is_jpeg):
        raise ValueError("entry_image.png is neither PNG nor JPEG content")
    if size > MAX_BYTES:
        raise ValueError(f"entry_image.png is {size} bytes, over the 1 MiB cap")


def main() -> None:
    check_source()
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    with open(SOURCE, "rb") as a, open(OUTPUT, "rb") as b:
        if a.read() != b.read():
            raise IOError("written entry.png does not match the source image")


if __name__ == "__main__":
    main()
