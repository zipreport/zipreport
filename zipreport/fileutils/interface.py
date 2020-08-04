import io


class FsError(Exception):
    pass


class FsInterface:

    def get(self, name: str) -> io.BytesIO:
        pass

    def add(self, name: str, content):
        pass

    def mkdir(self, name: str):
        pass

    def exists(self, path: str) -> bool:
        pass

    def is_dir(self, path: str) -> bool:
        pass

    def list(self, path: str) -> list:
        pass

    def list_files(self, path: str) -> list:
        pass

    def list_dirs(self, path: str) -> list:
        pass

    def get_backend(self) -> any:
        pass
