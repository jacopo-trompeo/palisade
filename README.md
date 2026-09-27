# Palisade

A Linux desktop productivity tool that blocks distracting websites and
applications on a schedule. Define filters with a set of blocked domains and
process names and a schedule, then a background daemon enforces them by
rewriting `/etc/hosts` and terminating matching processes.

## Architecture

Palisade runs as two separate processes that communicate over a Unix domain
socket using newline-delimited JSON messages.

```
GUI Process (PySide6)          Unix Socket          Daemon Process (systemd)
┌──────────────────────┐                            ┌─────────────────────┐
│  Window              │  ── JSON-RPC messages ──►  │  IPC Handler        │
│  ├─ HomeView         │  ◄── JSON-RPC replies ──   │  Schedule Loop      │
│  ├─ FilterEditor     │                            │  ├─ compute active  │
│  ├─ SettingsView     │                            │  │  filters         │
│  └─ AboutView        │                            │  └─ write /etc/hosts│
│                      │                            │  Process Monitor    │
│  DBI (db interface)  │                            │  ├─ poll psutil     │
│  ├─ dev: direct SQL  │                            │  └─ SIGTERM matches │
│  └─ prod: via socket │                            │  SQLite Database    │
└──────────────────────┘                            └─────────────────────┘
```

**The daemon** runs as a systemd service and owns the SQLite database. It runs
two concurrent asyncio loops: one recomputes which filters are active and
rewrites `/etc/hosts` on every schedule transition, and the other polls running
processes every 5 seconds and terminates any whose name matches a blocked app.

**The GUI** is a PySide6 desktop application. In production, it talks to the
daemon over the Unix socket for all database operations and status queries. In
dev mode (`--dev`), it accesses the SQLite database directly and spawns a child
daemon process, never touching real system files.

**IPC** is synchronous on the client side and asynchronous on the server side.
The GUI sends a JSON line and blocks for a reply (with a 3-second timeout). The
daemon's asyncio server reads messages, dispatches them to a handler, and sends
back a JSON reply.

## Features

- **Filters**: Named rulesets that group blocked websites and apps under a
  schedule. Filters can be enabled or disabled with a toggle.
- **Schedules**: Three presets (Always, Weekdays, Weekends) or custom
  configurations with specific days of the week and multiple time ranges.
- **Website blocking**: Adds entries to `/etc/hosts` that resolve blocked
  domains to `127.0.0.1`. Only domains managed by Palisade are touched. The
  block section is delimited by marker comments so the rest of the file
  remains intact.
- **Application blocking**: Monitors running processes with `psutil` and
  terminates any whose process name matches a blocked app. Sends `SIGTERM`
  first, then `SIGKILL` after 2 seconds if the process is still alive.
- **App discovery**: Browse installed applications by parsing XDG `.desktop`
  entries. This lets you pick apps by name and icon instead of typing process
  names manually.
- **Edit lock**: A configurable delay (5 to 300 seconds) before you can edit a
  filter after opening it. The editor shows a countdown and disables all inputs
  until the lock expires. Meant to discourage impulsive unblocking.
- **Desktop notifications**: Shows a notification when an application is killed,
  naming the app and the filter that blocked it.
- **Themes**: Light and dark themes (QSS stylesheets), switchable
  at runtime from the Settings view. The choice is persisted in the database.
- **Dev mode**: The `--dev` flag places all files under `/tmp` and prevents any
  modification to real system paths. Safe to run while developing.

## Tech Stack

| Technology          | Role                 | Notes                                                               |
| ------------------- | -------------------- | ------------------------------------------------------------------- |
| Python 3.14         | Language             |                                                                     |
| PySide6             | GUI framework        | Qt 6 bindings for Python. Native look, no web runtime needed        |
| SQLite              | Database             | Embedded database via stdlib `sqlite3`. Filter and settings storage |
| psutil              | Process management   | Cross-platform process discovery and termination                    |
| QtAwesome           | Icons                | Font Awesome 6 icon library for Qt                                  |
| asyncio             | Daemon concurrency   | Concurrent schedule and process monitoring loops                    |
| systemd             | Service management   | Production daemon lifecycle and auto-restart                        |
| Unix domain sockets | IPC                  | JSON-over-socket communication between GUI and daemon               |
| uv                  | Package management   |                                                                     |
| ruff                | Linting & formatting |                                                                     |
| pyright             | Type checking        |                                                                     |
| pytest              | Testing              | Unit tests with headless Qt via `QT_QPA_PLATFORM=offscreen`         |
| GitHub Actions      | CI/CD                | Lint, format check, type check, and tests on every push and PR      |

## Install & Run

Palisade requires Python 3.14 or later and [uv](https://docs.astral.sh/uv/)
(or [mise](https://mise.jdx.dev) with the included `mise.toml`).

Clone the repository and install:

```bash
git clone https://github.com/jacopo-trompeo/palisade.git
cd palisade
uv sync
```

**Dev mode** runs everything under `/tmp` and never touches `/etc/hosts` or
kills real processes:

```bash
uv run palisade --dev
```

**Production mode** runs the GUI that communicates with the systemd daemon.
Install the daemon first (requires root):

```bash
sudo -E uv run palisade --install-daemon
uv run palisade
```

The `-E` flag preserves your environment so `uv` is available inside `sudo`.
To remove the daemon:

```bash
sudo -E uv run palisade --uninstall-daemon
```

Other options:

```
uv run palisade --help
uv run palisade --version
```

## Development

Set up the development environment:

```bash
uv sync            # installs dependencies including dev tools
```

Run checks:

```bash
uv run ruff check .                  # lint
uv run ruff format --check .         # format check
uv run pyright                       # type check
uv run pytest                        # run tests
```

Tests use `QT_QPA_PLATFORM=offscreen` (set automatically in `conftest.py`) so
no display server is needed. CI runs the same commands on every push to `main`
or `develop` and on all pull requests.

## Project Structure

```
palisade/
  src/palisade/
    __main__.py             entry point and CLI argument parsing
    config.py               centralized path and logging configuration
    dbi.py                  database interface, dispatches to direct SQL or IPC
    ipc.py                  Unix socket client/server for GUI-daemon communication
    installer.py            systemd unit generation, install, and uninstall
    db/                     SQLite schema, models (Filter, Schedule, TimeRange), CRUD
    daemon/                 asyncio scheduler, hosts/proc enforcer, schedule engine
    gui/                    PySide6 desktop application, views, and reusable widgets
    assets/themes/          dark and light QSS stylesheets
  tests/                    unit tests with headless Qt via conftest fixtures
  pyproject.toml            dependencies, build config, lint/typecheck/test tooling
  mise.toml                 mise runtime configuration (uv)
```

## Design Decisions

**Two-process architecture with a systemd daemon.**
The GUI and the enforcement engine are separate processes. This means filters
stay active even when the GUI is closed and the daemon restarts automatically
if it crashes or after a reboot.

**`/etc/hosts` for website blocking.**
Simple, requires no browser extension or proxy configuration, and works across
all applications. The downside is that it only affects DNS resolution: users
with DNS-over-HTTPS or custom DNS servers will bypass it, and blocked HTTPS
sites show certificate errors rather than a clean block page.

**Process name matching for app blocking.**
Matching by process name (the executable basename) is simple and covers most
cases. It can be bypassed by renaming the executable or by apps that spawn
child processes under different names.

**Dev mode with `/tmp` paths.**
A global `--dev` flag switches all file paths to `/tmp/palisade_dev.*`. This is
simpler than mocking or dependency injection for the filesystem but relies on a
mutable module-level global in `config.py`, which makes tests somewhat fragile.

**Qt/PySide6 over Electron or GTK.**
Qt was chosen because it provides a mature, native-feeling desktop toolkit with
Python bindings that are well-maintained. The alternative of a web-based UI
(Electron) was avoided to keep the application lightweight and avoid shipping a
browser runtime.

## Limitations & Future Work

- **Overnight time ranges are not supported.** The `TimeRange` model rejects
  `start >= end`, so ranges like 22:00-06:00 cannot be expressed. The schedule
  engine has some logic for overnight handling but the model layer blocks it.
- **Website blocking is DNS-only.** Users with DNS-over-HTTPS, custom DNS
  servers, or cached DNS entries will not be blocked reliably. Browser
  extensions or a local proxy would be more robust.
- **App blocking is name-based.** A renamed or copied executable will not be
  caught. Hashing or path-based matching could improve this.
- **No packaging beyond source.** No Flatpak, AppImage, or PyPI distribution.
  Installation currently requires cloning the repository and building with uv.
- **Single-user assumption.** The daemon runs as root via systemd and applies
  the same rules to all users on the machine. There is no per-user
  configuration or multi-user isolation.
- **Fixed window geometry.** The window size is set to 960x640 on launch and
  user preferences are not saved or restored.

## License

MIT. Copyright 2026 Jacopo Trompeo.
