import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="palisade", description="Palisade productivity app"
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Dev mode: no real system changes; use /tmp paths and log instead of acting",
    )

    from palisade.gui.app import run

    return run()


if __name__ == "__main__":
    sys.exit(main())
