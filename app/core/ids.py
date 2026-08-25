"""UUIDv7 generation.

UUIDv7 (RFC 9562) embeds a millisecond Unix timestamp in the high bits, so
primary keys are time-ordered. That keeps B-tree index inserts local and
avoids the write amplification of random UUIDv4 keys. The stdlib does not
ship a v7 generator on Python 3.12, so we implement the layout directly.
"""

from __future__ import annotations

import os
import time
from uuid import UUID


def uuid7() -> UUID:
    """Return a new time-ordered UUIDv7."""
    unix_ts_ms = int(time.time() * 1000)

    # 48 bits: unix timestamp in milliseconds.
    ts = unix_ts_ms & 0xFFFFFFFFFFFF

    rand = os.urandom(10)
    rand_a = int.from_bytes(rand[:2], "big") & 0x0FFF  # 12 bits
    rand_b = int.from_bytes(rand[2:], "big") & 0x3FFFFFFFFFFFFFFF  # 62 bits

    value = ts << 80
    value |= 0x7 << 76  # version 7
    value |= rand_a << 64
    value |= 0b10 << 62  # variant (RFC 4122)
    value |= rand_b

    return UUID(int=value)
