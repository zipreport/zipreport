import io


class FsError(Exception):
    pass


class FsInterface:

    def get(self, name: str) -> io.BytesIO:
        """
        Read file
        :param name:
        :return:
        """
        pass

    def add(self, name: str, content):
        """
        Create file
        :param name:
        :param content:
        :return:
        """
        pass

    def mkdir(self, name: str):
        """
        Make directory
        :param name:
        :return:
        """
        pass

    def exists(self, path: str) -> bool:
        """
        Check if path (file or dir) exists
        :param path:
        :return:
        """
        pass

    def is_dir(self, path: str) -> bool:
        """
        Check if path is a dir
        :param path:
        :return:
        """
        pass

    def list(self, path: str) -> list:
        """
        List contents of the given path
        :param path:
        :return:
        """
        pass

    def list_files(self, path: str) -> list:
        """
        List files on the given path
        :param path:
        :return:
        """
        pass

    def list_dirs(self, path: str) -> list:
        """
        List dirs on the given path
        :param path:
        :return:
        """
        pass

    def get_backend(self) -> any:
        """
        Get internal backend object
        :return:
        """
        pass
