import java
from java.io import Serializable
from java.util.concurrent import Callable

from clamp import ClampProxyMaker


class BarClamp(Callable, Serializable):

    __proxymaker__ = ClampProxyMaker(
        "bar",
        constants={ "fortytwo": (java.lang.Integer(42), java.lang.Integer.TYPE),
                    "str": ("A string", java.lang.String),
                    "serialVersionUID" : (java.lang.Long(99), java.lang.Long.TYPE),
                   })

    def __init__(self):
        print "Being init-ed", self

    def call(self):
        print "foo"
        return 42


