import io
from abc import ABC, abstractmethod


class FsError(Exception):
    pass


class FsInterface(ABC):
    @abstractmethod
    def get(self, name: str) -> io.BytesIO:
        """
        Read file
        :param name:
        :return:
        """
        pass

    @abstractmethod
    def add(self, name: str, content, overwrite: bool = False):
        """
        Create file
        :param name:
        :param content:
        :param overwrite: if True, allow overwriting existing files
        :return:
        """
        pass

    @abstractmethod
    def mkdir(self, name: str):
        """
        Make directory
        :param name:
        :return:
        """
        pass

    @abstractmethod
    def exists(self, path: str) -> bool:
        """
        Check if path (file or dir) exists
        :param path:
        :return:
        """
        pass

    @abstractmethod
    def is_dir(self, path: str) -> bool:
        """
        Check if path is a dir
        :param path:
        :return:
        """
        pass

    @abstractmethod
    def list(self, path: str) -> list:
        """
        List contents of the given path
        :param path:
        :return:
        """
        pass

    @abstractmethod
    def list_files(self, path: str) -> list:
        """
        List files on the given path
        :param path:
        :return:
        """
        pass

    @abstractmethod
    def list_dirs(self, path: str) -> list:
        """
        List dirs on the given path
        :param path:
        :return:
        """
        pass

    @abstractmethod
    def get_backend(self):
        """
        Get internal backend object
        :return:
        """
        pass
