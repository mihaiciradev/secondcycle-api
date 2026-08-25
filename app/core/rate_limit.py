"""Shared slowapi limiter, keyed by client IP.

Behind Fly.io the real client address arrives in ``Fly-Client-IP`` (or the
first hop of ``X-Forwarded-For``); fall back to the socket peer otherwise.
"""

from __future__ import annotations

from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request


def client_ip(request: Request) -> str:
    fly_ip = request.headers.get("Fly-Client-IP")
    if fly_ip:
        return fly_ip
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return get_remote_address(request)


limiter = Limiter(key_func=client_ip)
