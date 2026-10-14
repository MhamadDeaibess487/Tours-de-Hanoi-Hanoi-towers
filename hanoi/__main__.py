import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Tours de Hanoï")
    parser.add_argument("--cli", action="store_true", help="Jouer dans le terminal")
    args = parser.parse_args()
    try:
        if args.cli:
            from .cli import run

            run()
        else:
            from .ui import run

            run()
    except (KeyboardInterrupt, EOFError):
        print("\nAu revoir !")
    except ImportError as error:
        print(f"Tkinter indisponible : {error}. Installez python3-tk ou utilisez --cli.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
