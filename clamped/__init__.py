import java
from java.io import Serializable
from java.util.concurrent import Callable

from clamp import ClampProxyMaker


class BarClamp(Callable, Serializable):

    __proxymaker__ = ClampProxyMaker("bar")

    def __init__(self):
        print "Being init-ed", self

    def call(self):
        print "foo"
        return 42


