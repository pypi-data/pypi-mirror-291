import argparse

from fbc.fbc import fast_blockcheck
from fbc.targets import get_urls

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--timeout", type=int, default=5, help="request timeout in seconds (5 by default)")
parser.add_argument("-s", "--shuffle", action='store_true', help="shuffle domains each time")
parser.add_argument("-r", "--repeat", type=int, default=0, help="repeat each N minutes")

args = parser.parse_args()


def main():
    urls = get_urls()

    try:
        fast_blockcheck(urls, args.timeout, args.shuffle, args.repeat)
    except KeyboardInterrupt:
        exit(0)
