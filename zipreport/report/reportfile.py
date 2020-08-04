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
        if name in self._manifest.keys():
            return self._manifest[name]
        return default

    def get_fs(self) -> ZipFs:
        return self._fs

    def exists(self, path) -> bool:
        return self._fs.exists(path)

    def get(self, name: str) -> io.BytesIO:
        return self._fs.get(name)

    def add(self, name:str, content):
        return self._fs.add(name, content)

    def save(self) -> io.BytesIO:
        return self._fs.get_backend().save_stream()