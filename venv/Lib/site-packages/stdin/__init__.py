__all__ = ["size", "isatty", "read"]


import os
import sys


def size():
    """return size in bytes of a stdin"""
    return os.fstat(sys.stdin.fileno()).st_size


def isatty():
    """return True if stdin is open and connected to a tty(-like) device, else False"""
    return sys.stdin.isatty()


def read():
    """return a string with stdin data"""
    if size() > 0:
        return sys.stdin.read()
    return ""
