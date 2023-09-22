from pathlib import Path


class PathCache:
    """
    ZipFs content cache
    """

    def __init__(self, trailing="/"):
        self._sep = trailing
        self._cache = {}

    def add(self, item: str):
        """
        Add a file to the path cache
        :param item:
        :return:
        """
        item = Path(item)
        root = self._cache
        parts = list(item.parts)
        file = parts.pop()
        for p in parts:
            if p not in root.keys():
                root[p] = {}
            root = root[p]
        root[file] = None

    def path_exists(self, path: str) -> bool:
        """
        Check if a dir path exists
        :param path:
        :return:
        """
        path = Path(path)
        root = self._cache
        for p in path.parts:
            if p not in root.keys():
                return False
            root = root[p]

        return type(root) is dict

    def file_exists(self, path: str) -> bool:
        """
        Check if a file path exists
        :param path:
        :return:
        """
        path = Path(path)
        root = self._cache
        for p in path.parts:
            if p not in root.keys():
                return False
            root = root[p]
        return root is None

    def list_files(self, path: str) -> list:
        """
        List files on a given path
        :param path:
        :return:
        """
        result = []
        root = self._cache
        path = Path(path)
        for p in path.parts:
            if p in root.keys():
                root = root[p]
            else:
                # invalid path
                return result
        if root is None:
            # its a file, not a dir
            return result
        result.extend(k for k in root.keys() if root[k] is None)
        return result

    def list_dirs(self, path: str) -> list:
        """
        List dirs on a given path
        :param path:
        :return:
        """
        result = []
        root = self._cache
        path = Path(path)
        for p in path.parts:
            if p in root.keys():
                root = root[p]
            else:
                # invalid path
                return result
        if root is None:
            # its a file, not a dir
            return result
        result.extend(k + self._sep for k in root.keys() if root[k] is not None)
        return result

    def list(self, path) -> list:
        """
        List all starting from a given path, recursively
        :param path:
        :return:
        """
        result = []
        root = self._cache
        path = Path(path)
        for p in path.parts:
            if p in root.keys():
                root = root[p]
            else:
                # invalid path
                return result
        return result if root is None else self._path_transversal(root, Path(""))

    def _path_transversal(self, root: dict, path: Path) -> list:
        """
        Internal path transversal routine
        :param root:
        :param path:
        :return:
        """
        result = []

        for k in root:
            if root[k] is None:
                result.append(str(path / k))
            else:
                dir = path / k
                result.append(str(dir) + self._sep)
                result.extend(self._path_transversal(root[k], dir))
        return result

    def clear(self):
        """
        Clear path cache
        :return:
        """
        self._cache = {}
