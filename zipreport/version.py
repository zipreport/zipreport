ZIPREPORT_VERSION = ["1", "1", "0"]


def get_version():
    return ".".join(ZIPREPORT_VERSION)


__version__ = get_version()
