import io
import os
from pathlib import Path

from .interface import FsError, FsInterface


class DiskFs(FsInterface):
    """
    Disk-based file operations
    Note: due to the way path separators are handled, one should assume compatibility with unix-os only
    """

    def __init__(self, path):
        """
        Constructor
        :param path: filesystem path to use as root
        """
        self._basepath = str(path) if isinstance(path, Path) else path

    def get(self, name: str) -> io.BytesIO:
        """
        Retrieve contents of a file
        :param name: filename with full path
        :return: io.BytesIO
        """
        path = self._build_path(name)
        if not os.path.exists(path):
            raise FsError(f"Path '{path}' does not exist")

        if not os.path.isfile(path):
            raise FsError(f"Path '{path}' is not a file")
        with open(path, "rb", buffering=0) as f:
            return io.BytesIO(f.read())

    def add(self, name: str, content):
        """
        Add a new file
        :param name: filename with full path
        :param content: file contents
        :return:
        """
        name = self._build_path(name)
        if not self._can_create(os.path.dirname(name), name):
            raise FsError(
                f"Cannot add file '{name}'; Invalid path or already existing file"
            )
        with open(name, "wb", buffering=0) as f:
            f.write(content)

    def mkdir(self, name: str):
        """
        Creates a directory
        :param name: full directory path
        :return:
        """
        name = self._build_path(name)
        if not self._can_create(os.path.dirname(name), name):
            raise FsError(
                f"Cannot add file '{name}'; Invalid path or already existing dir"
            )
        os.mkdir(name)

    def exists(self, path: str) -> bool:
        """
        Check if a given path (file or dir) exists
        :param path:
        :return:
        """
        return os.path.exists(self._build_path(path))

    def is_dir(self, path: str) -> bool:
        """
        Check if path is a valid directory
        :param path: path to check
        :return: bool
        """
        path = self._build_path(path)
        return os.path.exists(path) and os.path.isdir(path)

    def list_files(self, path: str) -> list:
        """
        List existing files on the given path
        :param path: path
        :return: list
        """
        path = self._build_path(path)
        if not os.path.exists(path) or not os.path.isdir(path):
            raise FsError(f"Cannot stat '{path}'; Invalid path")
        for _, _, filenames in os.walk(path):
            return filenames

    def list(self, path: str) -> list:
        """
        List all contents (files and dirs) on the specified path and subpaths
        directories are listed with trailing slash (/)
        :param path: root path to start listing
        :return: list
        """
        path = Path(self._build_path(path))
        result = []
        for dirname, dirs, files in os.walk(path):
            dirname = Path(dirname)
            for f in dirs:
                f = dirname / Path(f)
                # directories always have trailing slash
                result.append(str(f.relative_to(path)) + os.sep)
            for f in files:
                f = dirname / Path(f)
                result.append(str(f.relative_to(path)))
        return result

    def list_dirs(self, path: str) -> list:
        """
        List all directories in the specified path
        :param path: path to check
        :return: list
        """
        path = self._build_path(path)
        if not os.path.exists(path) or not os.path.isdir(path):
            raise FsError(f"Cannot stat '{path}'; Invalid path")
        result = []
        for _, dirnames, _ in os.walk(path):
            result.extend(dir + os.sep for dir in dirnames)
            return result

    def get_backend(self) -> any:
        """
        Retrieve fs backend
        For disk-based is None
        :return: None
        """
        return None

    def _can_create(self, path, name: str) -> bool:
        """
        Verify if a file/dir can be created on a given path
        :param path: path to check
        :param name: name to check
        :return: bool
        """
        return os.path.exists(path) and os.path.isdir(path) and not os.path.exists(name)

    def _build_path(self, path):
        """
        Cleans and build absolute path for internal use
        :param path: relative path
        :return: absolute path
        """
        return os.path.join(self._basepath, path.lstrip(os.sep))
