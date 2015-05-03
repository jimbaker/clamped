Clamped: Demonstrating the Clamp package
========================================

The [Clamp package][clamp] supports functionality like the following in Java
code:

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

In addition, Clamp also integrates with setuptools, in order to build
jars in `site-packages`, and then to package up Jython, other
dependent jars, the Python standard library, and installed packages
into a single jar suitable for running on containers.

There are alternatives to Clamp, such as [object factories][] (or more
generally dependency injection). However, the object factories
approach requires that the Java code must support factories, vs simple
constructors. For projects like Apache Storm, you would have to write
this object factory boilerplate code to use Python classes. In part to
address such needs as [Storm integration with Python][romper], Clamp
was created.


Release notes
=============

Building jars with Clamp on Windows is not yet supported, but it will
be once we have some development time to spare. (We are currently
focused on getting Jython 2.7.0 out.) However, you can run such jars
on Windows. (There's a small problem in using `\` instead of `/` -
easy to fix, however.)


Writing a Python class to use clamp
===================================

To write a clampable Python class, here's what it looks like. Note
that such classes need to extend a Java class and/or Java
interfaces. This Python class extends two Java interfaces,
`Serializable` and `Callable`. By extending an interface or
implementing class, you make it possible for Java code to know how to
work with your Python classes. Note this part is no different than
writing a Python callback for Java. However, the key extra step is the
use of `clamp_base`, which also indicates that the root package for
this class should be `bar`, or fully qualified,
`bar.clamped.BarClamp`.

````python
from java.io import Serializable
from java.util.concurrent import Callable
from clamp import clamp_base

BarBase = clamp_base("bar")  # metaclass to map to Java packages

class BarClamp(BarBase, Callable, Serializable):

    def __init__(self):
        print "Being init-ed", self

    def call(self):
        print "Hello, world!"
        return 42
````

Next, a key piece of Clamp is that it supports setuptools and soon
the PyPI ecosystem. This is all that is required to clamp a module,
you simply need to specify it with the `clamp` keyword and require the
`clamp` package:

````python
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
from clamp.commands import clamp_command

setup(
    name = "clamped",
    version = "0.1",
    packages = find_packages(),
    install_requires = ["clamp"],
    clamp = {
        "modules": ["clamped"]
    },
    cmdclass = { "install": clamp_command }
)
````

Follow the [Clamp installation][installation] steps.

Then install this example package. We will assume that you have
`jython27` mapped to the Jython launcher, `$JYTHON_HOME/bin/jython`:

````bash
$ git clone https://github.com/jimbaker/clamped.git
$ cd clamped
$ jython27 setup.py clamp
````

The `clamp` command constructs a jar in
`$JYTHON_HOME/Lib/site-packages/jars/clamped-0.1.jar`. It also ensures
that this jar is automatically added to `sys.path` through the use of
`site-packages/jar.pth`.

To make this more convenient, we can use a `cmdclass` with setuptools
such that `install` uses Clamp's version, which does the `clamp` as
part of its work:

````python
    cmdclass = { "install": clamp_command }
````

You can use now this newly built jar for Java integration, but more
likely you will need to build a single jar of your project, including
all other clamped jars. To combine with the previous step:

````bash
$ jython27 setup.py install singlejar
````

which will construct a single jar, in our case
`clamped-0.1-single.jar`. You can make this runnable if your toplevel
directory specifies a `__run__.py` file:

````python
from clamped import BarClamp

x = BarClamp()
x.call()
````

To run, simply do the following:

````bash
$ java -jar clamped-0.1-single.jar
````

which will result in output like the following:

````
Being init-ed bar.clamped.BarClamp@2798073c
Hello, world!
````

There you have it: Python code using a Java class to call Python, all
packaged up in a single Java jar. Boggles the mind! Of course, it's up
to you to write something more interesting than outputting `Hello,
world!`. For another example, check out [HelloWSGI][].

With this single jar, you are now ready to directly integrate with
Java. Let's say you have this class:

````bash
export CLASSPATH=`pwd`/clamped-0.1-single.jar:.
cd testjava
javac UseClamped.java
java UseClamped
````

and then you should expect to see output like the following, mostly
debugging so we know it's still working :)

````
Being init-ed bar.clamped.BarClamp@129e4e49
Hello, world!
BarClamp: 42
````

You can decompile the proxy class to see exactly what's going on with
these steps. First, download the [Procyon decompiler][Procyon]. I used
0.5.21 when I did this step, but the most recent version when you try
this out should be just fine.

Then unpack the jar and decompile with Procyon. You should do this in some
unpacking directory, since jar unpacking will explode a lot of files at
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

@APIVersion(36)
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
        throw (Throwable)Py.NotImplementedError("");
    }

    static {
        serialVersionUID = 1L;
    }

    public static void classDictInit(final PyObject pyObject) {
        pyObject.__setitem__("__supernames__", Py.java2py((Object)new String[] { "clone", "finalize" }));
    }
}
````

Note that the Python code still lives in another class - this is the
just the proxy wrapper.


Known issues
============

Clamp is still subject to refactoring at this point; see the TODO list at
the [project page][clamp].

Also, it's not feasible to use `__new__` in your Python classes that
are clamped. Why not? Java expects that constructing an object for a
given class returns an object of that class! The solution is simple:
call a factory function, in Python or Java, to return arbitrary
objects. This is just a simple, if fundamental, mismatch between
Python and Java in its object model.


Credits
=======

Clamp is a project that has been discussed for a long time in the
Jython community as a way to replace the functionality of `jythonc`,
which is no longer supported. [Darjus Loktevic][customizing proxymaker]
did much of the latest work to get this working, and I
have added a few critical bits, including setuptools integration.


<!-- References -->
  [clamp]: https://github.com/jythontools/clamp
  [HelloWSGI]: https://github.com/jimbaker/hellowsgi
  [installation]: https://github.com/jythontools/clamp#installation
  [object factories]: http://www.jython.org/jythonbook/en/1.0/JythonAndJavaIntegration.html#object-factories
  [customizing proxymaker]: http://darjus.blogspot.com/2013/01/customizing-jython-proxymaker.html
  [Procyon]: https://bitbucket.org/mstrobel/procyon/downloads
  [romper]: https://github.com/rackerlabs/romper
