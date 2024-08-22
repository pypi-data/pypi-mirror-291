v3.0.4
======

Bugfixes
--------

- Moved more_itertools into the dependencies. (#5)


v3.0.3
======

Refreshed package metadata.

#3: Fixed issue in tests where the connection to the test server
would fail on hosts where localhost resolved to ::1. Now the
test server binds to IPv6 when available and appropriate.

v3.0.2
======

Rely on PEP 420 for namespace packages.

v3.0.1
======

Refresh package metadata.

v3.0.0
======

Require Python 3.6 or later.

Adopt black for code style and other updates from jaraco/skeleton.

2.0
===

Switch to `pkgutil namespace technique
<https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages>`_
for the ``jaraco`` namespace.

1.2
===

Added ``jaraco.stream.Tee`` from jaraco.util 11.

1.1.2
=====

Refresh packaging.

1.1.1
=====

#2: Fixed issue where ``gzip.load_streams`` would get into
an infinite loop at the end of every stream.

1.1
===

Declared compatibility with Python 2.7 and gzip module now
is also Python 2.7 compatible.

1.0
===

Initial release with gzip and buffer module.
