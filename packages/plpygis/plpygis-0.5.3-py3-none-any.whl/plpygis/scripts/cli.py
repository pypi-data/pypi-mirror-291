from argparse import ArgumentParser
from plpygis import __version__

def cli():
    parser = ArgumentParser(
        description="Convert geometries",
        epilog="epilog"
    )
    parser.add_argument()
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    cli()
