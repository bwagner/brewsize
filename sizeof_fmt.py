#!/usr/bin/env python

import sys
from os.path import basename
from os import getpid


# from https://stackoverflow.com/a/1094933
def sizeof_fmt(num, suffix='B'):
    num = int(num)
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "{:3.1f}{}{}".format(num, unit, suffix)
        num /= 1024.0
    return "{:.1f}{}{}".format(num, 'Yi', suffix)


def main():

    pgnam = basename(sys.argv[0])
    print("{}:{}".format(pgnam, getpid()))

    nbytes = sys.argv[1]
    print("{} is {}".format(nbytes, sizeof_fmt(nbytes)))


if __name__ == "__main__":
    main()
