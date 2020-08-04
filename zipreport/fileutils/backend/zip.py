import io
import os
import zipfile
from typing import Union


class InMemoryZipError(Exception):
    pass


class InMemoryZip:

    def __init__(self, source: Union[str, io.BytesIO] = None):
        self._zip = None
        self._buffer = None
        if isinstance(source, io.BytesIO) or source is None:
            # create new zip or from buffer
            self.new(source)
        else:
            # source may be str or Path
            self.load(source)

    def new(self, buffer: io.BytesIO = None):
        flags = 'w'
        if isinstance(buffer, io.BytesIO):
            self._buffer = buffer
            flags = 'a'
        else:
            self._buffer = io.BytesIO()
        self._zip = zipfile.ZipFile(self._buffer, flags, zipfile.ZIP_DEFLATED)

    def load(self, disk_file: str):
        if not os.path.exists(disk_file) or not os.path.isfile(disk_file):
            raise InMemoryZipError("Zip file '{}' does not exist or is not a valid file")

        try:
            with open(disk_file, 'rb', buffering=0) as f:
                self._buffer = io.BytesIO(f.read())
                self._zip = zipfile.ZipFile(self._buffer, mode='a')
        except Exception as e:
            raise InMemoryZipError("Error reading Zip file: {}".format(e))

    def get_buffer(self) -> io.BytesIO:
        if not self.is_open():
            raise InMemoryZipError("Cannot get_buffer(); Zip is already closed.")
        # flush file, clone stream, reopen file
        self._zip.close()
        self._buffer.seek(0)
        result = io.BytesIO(self._buffer.read())
        self.new(self._buffer)
        return result

    def save_stream(self) -> io.BytesIO:
        if not self.is_open():
            raise InMemoryZipError("Cannot get_buffer(); Zip is already closed.")
        self._zip.close()
        self._buffer.seek(0)
        result = io.BytesIO(self._buffer.read())
        self._buffer = None
        self._zip = None
        return result

    def save(self, dest_file: str):
        if not self.is_open():
            raise InMemoryZipError("Cannot save(); Zip is already closed.")
        try:
            self._zip.close()
            self._buffer.seek(0)
            with open(dest_file, 'wb', buffering=0) as f:
                f.write(self._buffer.read())
            self._buffer = None
            self._zip = None
        except Exception as e:
            raise InMemoryZipError("Error saving Zip file: {}".format(e))

    def zip(self) -> zipfile.ZipFile:
        if not self.is_open():
            raise InMemoryZipError("Cannot zip(); Zip is already closed.")
        return self._zip

    def is_open(self):
        return self._zip is not None
