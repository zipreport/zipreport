import io
import os
import tempfile
from pathlib import Path
from shutil import rmtree

import pytest

from zipreport.fileutils.backend.zip import InMemoryZip, InMemoryZipError
from zipreport.fileutils import ZipFs
from .basezip import BaseZipTest


class TestZip(BaseZipTest):

    def test_create_zip(self):

        path, zipitems, zfs = self.create_sample1_zip()
        # now we close the file, retrieve buffer
        zipfile = zfs.get_backend().save_stream()
        assert isinstance(zipfile, io.BytesIO) is True

        # open file again from buffer
        zfs = ZipFs(InMemoryZip(zipfile))
        zlist = self.remove_dirs(zfs.list('/'))
        assert len(zlist) > 0
        assert len(zlist) == zipitems

        # check that every file is there
        for dirname, dirs, files in os.walk(path):
            dirname = Path(dirname)
            for fname in files:
                fname = dirname / Path(fname)
                assert str(fname.relative_to(path)) in zlist

    def test_load_zip(self):
        _, zipitems, zfs = self.create_sample1_zip()

        tmp = tempfile.mkdtemp()
        path = os.path.join(tmp, 'sample1.zip')
        zfs.get_backend().save(path)

        zfs = ZipFs(InMemoryZip(path))
        assert len(self.remove_dirs(zfs.list(''))) == zipitems
        # cleanup
        rmtree(tmp, ignore_errors=True)

    def test_buffer_zip(self):
        _, _, zfs = self.create_sample1_zip()
        buf = zfs.get_backend().get_buffer()
        assert isinstance(buf, io.BytesIO) is True

        with pytest.raises(InMemoryZipError) as e:
            buf = zfs.get_backend().save_stream()
            assert isinstance(buf, io.BytesIO) is True
            # must fail, file closed
            zfs.get_backend().get_buffer()

        with pytest.raises(InMemoryZipError):
            # must fail, file closed
            list = zfs.list('')

    def test_append_zip(self):
        fname = 'some_stupid_file.file'
        fcontents = b"the quick brown fox jumped over the lazy dog"
        _, _, zfs = self.create_sample1_zip()
        zfs.add(fname, fcontents)
        buf = zfs.get_backend().get_buffer()
        assert isinstance(buf, io.BytesIO) is True

        # new ZipFs instance from the previous buffer
        zfs = ZipFs(InMemoryZip(buf))
        data = zfs.get(fname)
        assert bytes(data.getbuffer()) == fcontents

    def remove_dirs(self, dirlist: list):
        result = []
        for i in dirlist:
            if not i.endswith('/'):
                result.append(i)
        return result
