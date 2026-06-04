# Palisade

**A Linux desktop app that blocks distracting websites and apps on a schedule**

Define *filters*, a set of blocked websites and applications plus a schedule for when
they apply (always, or specific days and time ranges), and Palisade enforces them so you
can stay focused when you want to be productive

## Features

- **Filters** with a name, a schedule, blocked websites, and blocked apps
- **Flexible schedules**: Always, weekday/weekend presets, or a custom set of days with
  one or more time ranges
- **App discovery**: browse installed applications (parsed from XDG `.desktop` entries)
  instead of typing process names by hand
- **Light & dark themes**, switchable at runtime
- **Dev mode** (`--dev`) that touches only `/tmp` and never modifies real system files,
  safe to run while developing.

## Install & run

Palisade uses [uv](https://docs.astral.sh/uv/) and targets **Python 3.14+**.

```bash
uv sync                 # create the environment and install dependencies
uv run palisade --dev   # run in dev mode (no real system changes; /tmp paths)
uv run palisade         # run normally
uv run palisade --help  # see options (--dev, --version)
```

## Development

```bash
uv run pytest                       # tests (Qt tests run headless via QT_QPA_PLATFORM=offscreen)
uv run ruff check .                 # lint
uv run ruff format .                # format
uv run pyright                      # type check
```

## Tech stack

- Python 3.14 
- [PySide6](https://doc.qt.io/qtforpython/) (Qt 6) 
- SQLite 
- [qtawesome](https://github.com/spyder-ide/qtawesome) 
- [uv](https://docs.astral.sh/uv/) 
- ruff 
- pyright 
- pytest
