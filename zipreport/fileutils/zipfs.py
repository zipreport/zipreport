import io
from pathlib import Path
from zipfile import ZIP_DEFLATED

from zipreport.fileutils.backend.zip import InMemoryZip
from .interface import FsError, FsInterface
from .pathcache import PathCache


class ZipFs(FsInterface):
    """
    Implement FsInterface operations on zipfiles
    Note: the list_*() operations and is_dir() can be quite slow, due to implementation restrictions
    """

    def __init__(self, zip: InMemoryZip):
        """
        Constructor
        :param zip: Zip Backend
        """
        self._sep = '/'
        self._zip = zip
        self._cache = PathCache(self._sep)
        self._build_cache()

    def get(self, name: str) -> io.BytesIO:
        """
        Read a file
        :param name: file path
        :return: file stream or None
        """
        zipfile = self._zip.zip()
        try:
            info = zipfile.getinfo(self._clean_path(name))
            with zipfile.open(info) as zf:
                return io.BytesIO(zf.read())
        except ValueError:
            raise FsError("Error reading file '{}'. Maybe it doesn't exist?".format(name))

    def add(self, name: str, content):
        """
        Add a file
        :param name: filename to create
        :param content: file contents
        :return:
        """
        zfile = self._zip.zip()
        name = self._clean_path(name)
        # convert BytesIO to bytes
        if isinstance(content, io.BytesIO):
            content.seek(0)
            content = content.read()
        try:
            zfile.getinfo(name)
            raise FsError("File'{}' already exists".format(name))
        except KeyError:
            pass
        try:
            zfile.writestr(name, content, compress_type=ZIP_DEFLATED)
            self._cache.add(name)
        except Exception as e:
            raise FsError("Error adding '{}' to  Zip: {}".format(name, e))

    def mkdir(self, name: str):
        raise FsError("ZipFs does not support creation of explicit directories")

    def exists(self, path: str) -> bool:
        """
        Check if a given path (file or dir) exists
        :param path:
        :return:
        """
        self._zip.zip()
        path = self._clean_path(path)
        # check if file exists first, then dir
        if not self._cache.file_exists(path):
            return self._cache.path_exists(path)
        return True

    def is_dir(self, path: str) -> bool:
        # check if file is still opened
        self._zip.zip()
        path = self._clean_path(path)
        return self._cache.path_exists(path)

    def list_dirs(self, path: str) -> list:
        """
        List dirs on a given path
        :param path:
        :return:
        """
        # check if file is still opened
        self._zip.zip()
        return self._cache.list_dirs(self._clean_path(path))

    def list_files(self, path: str) -> list:
        # check if file is still opened
        self._zip.zip()
        return self._cache.list_files(self._clean_path(path))

    def list(self, path: str) -> list:
        """
        List all contents (files and dirs) on the specified path and subpaths
        directories are listed with trailing slash (/)
        :param path: root path to start listing
        :return: list
        """
        # check if file is still opened
        self._zip.zip()
        return self._cache.list(self._clean_path(path))

    def get_backend(self) -> any:
        return self._zip

    def _build_cache(self):
        """
        Build path cache
        :return:
        """
        zipfile = self._zip.zip()
        for item in zipfile.namelist():
            self._cache.add(item)

    def _clean_path(self, path):
        """
        Remove self._sep from starting of path, if exists
        :param path:
        :return:
        """
        return str(path).lstrip(self._sep)
