# Security considerations

While your reports can reference external resources such as JavaScript files, images, CSS and fonts just like any
regular HTML page, keep in mind this may expose your system to security threats. To mimimize this possibility, you should
not reference external resources you don't own or trust.

The zipreport-server daemon also creates temporary HTTP servers on each rendering request; these servers may expose
sensitive information, so appropriate protection measures (such as running zipreport-server in a Docker container) are
recommended.



