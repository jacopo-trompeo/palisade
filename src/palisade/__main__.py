from __future__ import annotations

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="palisade", description="Palisade productivity app"
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Dev mode: no real system changes; use /tmp paths and log instead of acting",
    )
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    sys.exit(main())
