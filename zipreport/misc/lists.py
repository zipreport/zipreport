import collections


class RoOptionalList:
    def __init__(self, contents: list = None):
        if contents is None:
            contents = []
        self._list = contents

    def __len__(self):
        return len(self._list)

    def get(self, index, default=None):
        try:
            return self._list[index]
        except IndexError:
            return default
