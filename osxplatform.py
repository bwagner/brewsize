#!/usr/bin/env python
import sys
from os.path import basename
from os import getpid
import platform


def get_platform(version):
    try:
        get_platform.names
    except AttributeError:
        # list taken from https://en.wikipedia.org/wiki/OS_X
        # https://en.wikipedia.org/wiki/MacOS_version_history
        names = [
             "Cheetah", "Puma", "Jaguar", "Panther", "Tiger",
             "Leopard", "Snow Leopard", "Lion", "Mountain Lion",
             "Mavericks", "Yosemite", "El Capitan", "Sierra",
             "High Sierra", "Mojave",
        ]

        i = 0
        get_platform.names = dict()
        for name in names:
            get_platform.names["10.{}".format(i)] = name
            i = i+1

    return get_platform.names[version].lower().replace(" ", "_")


def get_local_platform():
    ver = platform.mac_ver()[0]
    ver = ver[:ver.rfind('.')]
    return get_platform(ver)


def main():

    pgnam = basename(sys.argv[0])
    print("{}:{}".format(pgnam, getpid()))

    if len(sys.argv) < 2:
        print(get_local_platform())
    else:
        print(get_platform(sys.argv[1]))


if __name__ == "__main__":
    main()
