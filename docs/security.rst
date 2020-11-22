.. _security:

Security considerations
=======================

While your reports can reference external resources such as JavaScript files, images, CSS and fonts just like any
regular HTML page, keep in mind this may expose your system to security threats. To mimimize this possibility, you should
not reference external resources you don't know or trust, and - if using zipreport-cli, **never** disable sandboxing mode.

There is a `zipreport-server docker image <https://github.com/zipreport/zipreport-docker>`__ available with sandboxing
enabled.



