clamped
=======

The idea of clamp is very simple; it's to support functionality like
the following in Java code:

````java
import bar.clamped.BarClamp;  // yes, you can now just import Python classes!

public class UseClamped {

    public static void main(String[] args) {
        BarClamp barclamp = new BarClamp();
	try {
	    System.out.println("BarClamp: " + barclamp.call());
	} catch (Exception ex) {
	    System.err.println("Exception: " + ex);
	}
    }

}
````

Such clamping is even more useful for projects like Storm where in
using Python classes, you would need similar support at the
`ClassLoader` level.

To write a clampable Python class, here's what it looks like. Note
that such classes need to extend a Java class and/or Java
interfaces. This Python class extends two Java interfaces,
`Serializable` and `Callable`. By doing so, Java code knows how to
work with your Python classes. Note this part is no different than
writing a Python callback for Java. However, the key extra step is the
use of `ClampProxyMaker`, which also indicates that the package for
this class should be `bar`, or fully qualified,
`bar.clamped.BarClamp`.

````python
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
````

Next, a key piece of clamp is that it supports setuptools and soon
the PyPI ecosystem. This is all that is required to clamp a module,
you simply need to specify it with the `clamp` keyword and require the
`clamp` package:

````python
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages


setup(
    name = "clamped",
    version = "0.1",
    packages = find_packages(),
    install_requires = ["clamp>=0.1"],
    clamp = ["clamped"],
)
````

To use this example project, you need to install install both clamp
and a fork of Jython that supports SSL:

1. `hg clone https://bitbucket.org/jimbaker/jython-ssl`. For this presentation, use `~jythondev/jython-ssl` as the place you put this.
2. run `ant` in `~jythondev/jython-ssl` directory and do something like `alias jython-ssl=~/jythondev/jython-ssl/dist/bin/jython`
3. `git clone https://github.com/rackerlabs/clamp.git`
4. `jython-ssl setup.py install`

Both requirements will go away as soon as clamp is in PyPI and
jython-ssl is merged against trunk (with some more work on SSL
support, of course).

To then install this example package, which uses clamp:

````bash
jython-ssl setup.py install
jython-ssl setup.py buildjar
````

The `buildjar` step constructs a jarfile, with the default name of
`clamped-0.1.jar` (`{projectname}-{version}.jar`) in this directory
(probably should go in the build directory). You need this as a separate jar because this is the part that Java needs to go against to figure out to interface with Jython.

Next step, you need to construct a reasonable `CLASSPATH`. I have
included a simple script for constructing this path, `alljars`;
assuming you are in the clamped directory:

````bash
export PATH=$(pwd)/bin:$PATH
export CLASSPATH=$(alljars ~/jythondev/jython-ssl/dist/javalib/*.jar):$(alljars ~/jythondev/jython-ssl/dist/jython-dev.jar):$(pwd)/clamped-0.1.jar:.
cd testjava
javac UseClamped.java  # ignore warnings about missing annotations
java UseClamped
````

and then you should expect to see output like the following, mostly
debugging so we know it's still working :)

````
ClampProxyMaker: bar None array(java.lang.Class, [<type 'java.util.concurrent.Callable'>, <type 'java.io.Serializable'>]) BarClamp clamped org.python.proxies.clamped$BarClamp$1 {'__init__': <function __init__ at 0x2>, '__module__': 'clamped', 'call': <function call at 0x3>, '__proxymaker__': <clamp.ClampProxyMaker object at 0x4>}
superclass=None, interfaces=array(java.lang.Class, [<type 'java.util.concurrent.Callable'>, <type 'java.io.Serializable'>]), className=BarClamp, pythonModuleName=clamped, fullProxyName=bar.clamped.BarClamp, mapping={'__init__': <function __init__ at 0x2>, '__module__': 'clamped', 'call': <function call at 0x3>, '__proxymaker__': <clamp.ClampProxyMaker object at 0x4>}, package=bar, kwargs={}
Entering makeClass org.python.proxies.clamp$SerializableProxyMaker$0@76ef1d4c
Looked up proxy bar.clamped.BarClamp
Being init-ed bar.clamped.BarClamp@5e476e34
BarClamp bar.clamped.BarClamp@23944847
BarClamp: 42
````

You can decompile the proxy class to see exactly what's going on with
these steps. First, download the Procyon decompiler from https://bitbucket.org/mstrobel/procyon/downloads. I'm using 0.5.21, but the most recent when you look should be just fine.

Then unpack the jar and decompile with Procyon. You should do this in some
unpacking directory, since jar unpacking will explode nicely at
toplevel.

```bash
mkdir unpacked && cd unpacked
jar xf ../clamped-0.1.jar
java -jar /path/to/procyon-decompiler-0.5.21.jar bar/clamped/BarClamp.class
````

This will result in output like the following:

````java
package bar.clamped;

import java.util.concurrent.*;
import java.io.*;
import org.python.core.*;
import org.python.compiler.*;

@APIVersion(33)
@MTime(-1L)
public class BarClamp implements PyProxy, Callable, Serializable, ClassDictInit
{
    protected PyObject __proxy;
    protected transient PySystemState __systemState;
    public static final long serialVersionUID;

    public void _setPyInstance(final PyObject _proxy) {
        this.__proxy = _proxy;
    }

    public PyObject _getPyInstance() {
        return this.__proxy;
    }

    public void _setPySystemState(final PySystemState _systemState) {
        this.__systemState = _systemState;
    }

    public PySystemState _getPySystemState() {
        return this.__systemState;
    }

    public void __initProxy__(final Object[] array) {
        Py.initProxy((PyProxy)this, "clamped", "BarClamp", array);
    }

    public BarClamp() {
        super();
        this.__initProxy__(Py.EmptyObjects);
    }

    public void finalize() {
        super.finalize();
    }

    public Object clone() {
        return super.clone();
    }

    public Object call() throws Exception {
        final PyObject findPython = ProxyMaker.findPython((PyProxy)this, "call");
        if (findPython != null) {
            final PyObject pyObject = findPython;
            try {
                return Py.tojava(pyObject._jcallexc((Object[])Py.EmptyObjects), (Class)Class.forName("java.lang.Object"));
            }
            catch (Exception ex) {
                throw ex;
            }
            catch (Throwable t) {
                pyObject._jthrow(t);
                return null;
            }
        }
        return null;
    }

    static {
        serialVersionUID = 1L;
    }

    public static void classDictInit(final PyObject pyObject) {
        pyObject.__setitem__("__supernames__", Py.java2py((Object)new String[] { "clone", "finalize" }));
    }
}
````

Credits
=======

Clamp is a project that has been discussed for a long time in the
Jython community as a way to replace the functionality of
`jythonc`. [Darjus Loktevic](http://darjus.blogspot.com/2013/01/customizing-jython-proxymaker.html)
did much of the latest work to get this working, and I have added a
few critical bits, including setuptools integration.