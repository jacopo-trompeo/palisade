import argparse
import sys

from palisade import __version__


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="palisade", description="Palisade productivity app"
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help=(
            "Dev mode: no real system changes; use /tmp paths and log instead of acting"
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"palisade {__version__}"
    )
    args = parser.parse_args()

    from palisade.gui.app import run

    return run(dev=args.dev)


if __name__ == "__main__":
    sys.exit(main())
