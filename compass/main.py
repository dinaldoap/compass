import argparse
import sys


def run(argv):
    parser = argparse.ArgumentParser(
        description='Compass: Helping investors to stick with theirs plans.')
    args = parser.parse_args(argv)


def main():
    run(sys.argv[1:])


if __name__ == '__main__':
    main()
