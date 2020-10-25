.. _install:

Installation
============

Required dependencies for ZipReport |version|:

* jinja2_ >=2.11
* requests_ >= 2.22.0
* WeasyPrint_ >= 51 (optional, see below)

Step 1: install ZipReport library
_________________________________

To install ZipReport library, just run:

.. code-block:: sh

    $ python3 -m pip install zipreport-lib

Or if WeasyPrint backend is required, install:

.. code-block:: sh

    $ python3 -m pip install zipreport-lib[weasyprint]

Step 2: choose and install a rendering backend
______________________________________________

Available backends:

* ZipReport-Server_ (API server, can be run on Docker, see zipreport-docker_)
* ZipReport-Cli_ (Command-line report generation)
* WeasyPrint_ (WeasyPrint backend, experimental)
* MIME (Mime Processor bundled, has no external dependencies)

Installing from source
______________________

ZipReport resides on GitHub_, you can clone the repository:

.. code-block:: sh

    $ git clone git@github.com:zipreport/zipreport.git

You can now install the package from the cloned repository:

.. code-block:: sh

    $ cd zipreport
    $ python3 setup.py install


.. _jinja2: https://palletsprojects.com/p/jinja/
.. _requests:  https://requests.readthedocs.io/en/master/
.. _WeasyPrint:  https://weasyprint.readthedocs.io/
.. _zipreport-docker: https://github.com/zipreport/zipreport-docker
.. _ZipReport-Server: https://github.com/zipreport/zipreport-server
.. _ZipReport-Cli: https://github.com/zipreport/zipreport-cli
.. _GitHub: https://github.com/zipreport/zipreport