import io
from io import StringIO
from pathlib import Path

from zipreport.fileutils import ZipFs
from zipreport.report.builder import ReportFileBuilder


class ReportFileError(Exception):
    pass


class ReportFile:

    def __init__(self, source: ZipFs, manifest: dict):
        if not isinstance(manifest, dict):
            raise ReportFileError("Invalid manifest format")
        if not isinstance(source, ZipFs):
            raise ReportFileError("Invalid source type")
        self._manifest = manifest
        self._fs = source

    def get_param(self, name: str, default=None):
        """
        Retrieve a parameter from the manifest file
        :param name: parameter name
        :param default: default value if parameter doesn't exist
        :return: parameter value
        """
        if name in self._manifest.keys():
            return self._manifest[name]
        return default

    def get_fs(self) -> ZipFs:
        """
        Retrieve internal ZipFs object
        :return: ZipFs
        """
        return self._fs

    def exists(self, path) -> bool:
        """
        Check if a file exists in the report
        :param path: path to check
        :return: true if file exists, false otherwise
        """
        return self._fs.exists(path)

    def get(self, name: str) -> io.BytesIO:
        """
        Read a file from the report into a buffer
        :param name: path to file
        :return: io.BytesIO
        """
        return self._fs.get(name)

    def add(self, name: str, content):
        """
        Add a file to the report
        :param name: file path
        :param content: contents of file
        :return:
        """
        return self._fs.add(name, content)

    def save(self) -> io.BytesIO:
        """
        Saves current report to a buffer
        :return: io.BytesIO
        """
        return self._fs.get_backend().save_stream()
