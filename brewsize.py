#!/usr/bin/env python

import sys
from os.path import basename
from os import getpid
import subprocess
import json
import requests
import sizeof_fmt
from osxplatform import get_local_platform
from functools import reduce

import logging
import argparse

module_name = 'brewsize'


def get_json_info(package):
    """retrieves json info as str for given homebrew package name


    Parameters
    ----------
    package : str
        homebrew package for which to retrieve info in json format as str

    Returns
    -------
    str
        json representation of homebrew package

    """
    proc = subprocess.Popen(
            ['brew', 'info', '--json=v1', package],
            stdout=subprocess.PIPE)
    (stdout, stderr) = proc.communicate()
    return json.loads(stdout)


def get_size(package, indent=0):
    """recursively calculates the size in bytes for a given homebrew package


    Parameters
    ----------
    package : str
        homebrew package for which to retrieve the size

    indent : int
        indentation for debug output

    Returns
    -------
    int
        package size in bytes if it hasn't been installed, 0 otherwise

    """
    logger = get_logger()

    try:
        get_size.packages_checked
        get_size.indent_space
    except AttributeError:
        get_size.packages_checked = set()
        get_size.indent_space = '    '

    ind = get_size.indent_space * indent
    logger.debug("{}package {}".format(ind, package))
    if package in get_size.packages_checked:
        logger.debug("{}{} checked, returning size 0".format(ind, package))
        return 0
    get_size.packages_checked.add(package)
    jd = get_json_info(package)
    url = jd[0]['bottle']['stable']['files'][get_local_platform()]['url']
    installed = len(jd[0]['installed']) > 0
    if installed:
        logger.debug("{}{} installed, returning size 0".format(ind, package))
        return 0
    else:
        dependencies = set(jd[0]['dependencies'])
        dependencies = dependencies.union(jd[0]['build_dependencies'])
        logger.debug("{}{} not installed, checking deps: {}".format(
            ind,
            package,
            ", ".join(map(str, dependencies))
            if len(dependencies) > 0 else "None."
        ))
        resp = requests.head(url, allow_redirects=True)
        size = int(resp.headers['Content-Length'])
        if len(dependencies) == 0:
            logger.debug(
                "{}{} size {} ({})".
                format(ind, package, size, sizeof_fmt.sizeof_fmt(size)))
        else:
            logger.debug(
                "{}{} alone size {} ({})".
                format(ind, package, size, sizeof_fmt.sizeof_fmt(size)))
            size += reduce(lambda x, y: x+y,
                           map(lambda x: get_size(x, indent+1), dependencies),
                           0)
            logger.debug("{}{} with deps size {} ({})".
                         format(
                             ind, package, size, sizeof_fmt.sizeof_fmt(size)))
        return int(size)  # in bytes


def usage(pgnam):
    """Displays usage and sys.exits."""
    print('''
       Usage: {} package
    ''').format(pgnam)
    sys.exit()


def get_logger():
    """retrieves logger ("singleton").


    Returns
    -------
    logging.Logger
        logger for this module

    """
    global module_name

    try:
        get_logger.logger
    except AttributeError:
        get_logger.logger = logging.getLogger(module_name)

    return get_logger.logger


def setup_logger(loglevel='INFO'):
    """sets up logger ("singleton").

    Parameters
    ----------
    loglevel : str
        log level

    """
    logger = get_logger()
    if loglevel is None:
        loglevel = "INFO"

    numeric_level = getattr(logging, loglevel.upper())

    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {}".format(loglevel))
    logger.setLevel(numeric_level)
    ch = logging.StreamHandler()
    formatter = logging.Formatter(fmt='%(name)s - %(message)s')
    ch.setFormatter(formatter)
    ch.setLevel(numeric_level)
    logger.addHandler(ch)


def make_args(pgnam):
    """builds the args object

    Parameters
    ----------
    pgnam : str
        program name (for usage message in case of failure)

    Returns
    -------
    args
        the object returned by argparse.ArgumentParser.parse_args()

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--loglevel",
                        help="set loglevel to one of ERROR, "
                             "CRITICAL, WARNING, DEBUG, INFO")
    parser.add_argument('package', type=str, help='homebrew package to check')
    args = parser.parse_args()

    setup_logger(args.loglevel)

    argc = len(args.package)
    if argc < 1:
        usage(pgnam)

    return args


def main():

    pgnam = basename(sys.argv[0])
    print("{}:{}".format(pgnam, getpid()))

    args = make_args(pgnam)

    brew_package = args.package

    packagesizeinbytes = get_size(brew_package)
    if packagesizeinbytes == 0:
        get_logger().info("{} already installed.".format(brew_package))
    else:
        get_logger().info(
                "{} package size including dependencies: {}".
                format(
                    brew_package,
                    sizeof_fmt.sizeof_fmt(packagesizeinbytes)))


# curl -I -L "$(brew info --json=v1 $@ | \
#       jq -r '.[0].bottle.stable.files.el_capitan.url')" \
#       2>&1 | egrep '^Content-Length: [^0]' | cut -d ' ' -f 2

if __name__ == "__main__":
    main()
