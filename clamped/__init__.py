from six.moves import urllib
from java.io import Serializable
from java.util.concurrent import Callable

from clamp import clamp_base


BarBase = clamp_base("bar")


class BarClamp(BarBase, Callable, Serializable):

    def __init__(self):
        print "Being init-ed", self

    def call(self):
        print "Hello, world!"
        return 42


