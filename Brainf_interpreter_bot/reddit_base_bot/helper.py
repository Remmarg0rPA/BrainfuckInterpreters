#!/usr/bin/python3
import sys, logging

class PicnicException(Exception):
    """This exception is expected. It's something the user can deal with."""
    pass

def is_number(s):
    """ Returns True if string is a number. """
    return s.replace('.', '', 1).isdigit()

def s2b(s, default):
    if not s: return default
    if s == "True": return True
    if s == "False": return False
    raise ValueError("string must be empty, True or False.")

class MyLog(object):
    def __init__(self, *args, **kwargs): logging.basicConfig(*args, **kwargs)

    def __call__(self, *args, **kwargs): self.i(*args, **kwargs)

    def c(self, *args, **kwargs): logging.critical(*args, **kwargs)

    def e(self, *args, **kwargs): logging.error(*args, **kwargs)

    def w(self, *args, **kwargs): logging.warning(*args, **kwargs)

    def i(self, *args, **kwargs): logging.info(*args, **kwargs)

    def d(self, *args, **kwargs): logging.debug(*args, **kwargs)
