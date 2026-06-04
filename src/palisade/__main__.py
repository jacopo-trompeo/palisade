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
        "--daemon",
        action="store_true",
        help="Run the background enforcement daemon",
    )
    parser.add_argument(
        "--install-daemon",
        action="store_true",
        dest="install_daemon",
        help="Install the systemd daemon service (requires root)",
    )
    parser.add_argument(
        "--uninstall-daemon",
        action="store_true",
        dest="uninstall_daemon",
        help="Uninstall the systemd daemon service (requires root)",
    )
    parser.add_argument(
        "--version", action="version", version=f"palisade {__version__}"
    )
    args = parser.parse_args()

    if args.install_daemon:
        from palisade.installer import install

        return install()
    if args.uninstall_daemon:
        from palisade.installer import uninstall

        return uninstall()
    if args.daemon:
        from palisade import config

        config.configure(args.dev)
        config.setup_logging(args.dev)

        from palisade.daemon.daemon import run as run_daemon

        return run_daemon()

    from palisade.gui.app import run

    return run(dev=args.dev)


if __name__ == "__main__":
    sys.exit(main())
