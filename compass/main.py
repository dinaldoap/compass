import argparse
import sys


def run(argv):
    parser = argparse.ArgumentParser(
        description='Compass: Helping investors to stick with theirs plans.')
    namespace = parser.parse_args(argv)
    args = dict(vars(namespace))


def main():
    run(sys.argv[1:])


if __name__ == '__main__':
    main()
