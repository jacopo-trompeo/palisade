import asyncio
import contextlib
import logging
import os
import signal
import subprocess
from collections.abc import Iterable
from dataclasses import dataclass

import psutil

from palisade import config
from palisade.db.models import Filter

logger = logging.getLogger(__name__)


@dataclass
class EnforcementSnapshot:
    domains: set[str]
    apps: set[str]
    filter_name_by_domain: dict[str, str]
    filter_name_by_app: dict[str, str]


def build_snapshot(active: Iterable[Filter]) -> EnforcementSnapshot:
    domains: set[str] = set()
    apps: set[str] = set()
    fname_by_domain: dict[str, str] = {}
    fname_by_app: dict[str, str] = {}

    for f in active:
        for d in f.blocked_websites:
            d = d.strip().lower()
            if d and d not in domains:
                domains.add(d)
                fname_by_domain[d] = f.name
        for a in f.blocked_apps:
            a = a.strip()
            if a and a not in apps:
                apps.add(a)
                fname_by_app[a] = f.name

    return EnforcementSnapshot(domains, apps, fname_by_domain, fname_by_app)


def _build_hosts_block(domains: Iterable[str]) -> str:
    lines = [config.HOSTS_MARKER_START]

    for d in sorted(domains):
        lines.append(f"127.0.0.1 {d}")
        if not d.startswith("www."):
            lines.append(f"127.0.0.1 www.{d}")
    lines.append(config.HOSTS_MARKER_END)

    return "\n".join(lines) + "\n"


def _read_hosts() -> str:
    path = config.hosts_path()

    if not path.exists():
        return ""

    return path.read_text()


def _strip_managed_block(content: str) -> str:
    if config.HOSTS_MARKER_START not in content:
        return content
    pre, _, rest = content.partition(config.HOSTS_MARKER_START)
    _, _, post = rest.partition(config.HOSTS_MARKER_END)

    return pre.rstrip("\n") + ("\n" + post.lstrip("\n") if post.strip() else "\n")


def _flush_dns_cache() -> None:
    for cmd in (["resolvectl", "flush-caches"], ["systemd-resolve", "--flush-caches"]):
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=5, check=False)
            if result.returncode == 0:
                return
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue


def write_hosts(domains: set[str]) -> None:
    hosts_path = config.hosts_path()
    existing = _read_hosts()
    stripped = _strip_managed_block(existing)

    if domains:
        new_content = stripped.rstrip("\n") + "\n\n" + _build_hosts_block(domains)
    else:
        new_content = stripped if stripped else ""

    hosts_path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = hosts_path.with_suffix(".tmp")
    try:
        temp_path.write_text(new_content)
        temp_path.replace(hosts_path)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise

    if config.is_dev():
        logger.debug(
            "would write %d domains to %s (dev preview)",
            len(domains),
            hosts_path,
        )
    else:
        _flush_dns_cache()
        logger.info("wrote %d domains to %s", len(domains), hosts_path)


def _process_matches(proc_name: str, blocked_app: str) -> bool:
    n = proc_name.lower()
    b = blocked_app.lower()

    return n == b or n == os.path.basename(b)


def find_blocked_processes(apps: set[str]) -> list[tuple[int, str, str]]:
    if not apps:
        return []

    hits: list[tuple[int, str, str]] = []

    for proc in psutil.process_iter(["pid", "name"]):
        try:
            name = proc.info.get("name") or ""
            if not name:
                continue
            for app in apps:
                if _process_matches(name, app):
                    hits.append((proc.info["pid"], name, app))
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return hits


async def enforce_processes(
    apps: set[str], filter_name_by_app: dict[str, str]
) -> list[tuple[int, str, str]]:
    matches = find_blocked_processes(apps)

    for pid, name, app in matches:
        filter_name = filter_name_by_app.get(app, "Palisade")
        if config.is_dev():
            logger.debug(
                "would kill PID %d (%s) - blocked by filter '%s'",
                pid,
                name,
                filter_name,
            )
        else:
            await _kill_process(pid, name)

    return matches


async def _kill_process(pid: int, name: str) -> None:
    try:
        os.kill(pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        return

    await asyncio.sleep(2)

    try:
        os.kill(pid, 0)
        os.kill(pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        return


def notify_user(title: str, body: str) -> None:
    logger.debug("%s - %s", title, body)

    with contextlib.suppress(FileNotFoundError):
        subprocess.Popen(
            ["notify-send", "-a", "Palisade", title, body],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
