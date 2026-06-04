import asyncio
import contextlib
import json
import logging
import os
import socket
from collections.abc import Awaitable, Callable

from palisade import config

logger = logging.getLogger(__name__)

Handler = Callable[[dict], Awaitable[dict | None]]


def notify(message: dict, timeout: float = 1.0) -> dict | None:
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect(str(config.socket_path()))
    except (TimeoutError, FileNotFoundError, ConnectionRefusedError, OSError):
        return None
    try:
        s.sendall((json.dumps(message) + "\n").encode())
        data = b""
        while b"\n" not in data:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
        if not data:
            return None
        return json.loads(data.split(b"\n", 1)[0].decode())
    except (TimeoutError, OSError, json.JSONDecodeError):
        return None
    finally:
        s.close()


def ping() -> bool:
    reply = notify({"type": "ping"})
    return bool(reply and reply.get("type") == "pong")


async def serve(handler: Handler) -> asyncio.AbstractServer:
    sock_path = config.socket_path()
    if sock_path.exists():
        sock_path.unlink()
    sock_path.parent.mkdir(parents=True, exist_ok=True)

    async def on_client(
        reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        try:
            line = await reader.readline()
            if not line:
                return
            try:
                msg = json.loads(line.decode())
            except json.JSONDecodeError:
                return
            reply = await handler(msg)
            if reply is not None:
                writer.write((json.dumps(reply) + "\n").encode())
                await writer.drain()
        finally:
            writer.close()
            with contextlib.suppress(Exception):
                await writer.wait_closed()

    server = await asyncio.start_unix_server(on_client, path=str(sock_path))
    with contextlib.suppress(OSError):
        os.chmod(sock_path, 0o666)
    return server
