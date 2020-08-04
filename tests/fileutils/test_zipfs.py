import pytest

from zipreport.fileutils import ZipFs, FsError
from zipreport.fileutils.backend.zip import InMemoryZip
from .basefs import BaseFsTest
from .basezip import BaseZipTest


class TestZipFs(BaseFsTest, BaseZipTest):
    dname = 'this_test_dir'
    fname = 'this_test_file.txt'
    fcontents = b"The quick brown fox jumped over the lazy dog"

    def test_zipfs(self):
        # note: some of zipfs operations are tested in test_zip.py
        path, zipitems, zfs = self.create_sample1_zip()

        rootdirs, rootfiles, items = self.path_walk(path)
        zipdirs = zfs.list_dirs('/')

        # check dir validations
        for dir in rootdirs:
            assert dir in zipdirs
            assert zfs.is_dir(dir) is True
            assert zfs.is_dir(dir.rstrip('/')) is True

        zfs.add(self.fname, self.fcontents)
        assert zfs.get(self.fname).getbuffer() == self.fcontents

    def test_zipfs_tree(self):
        """
        Test a full directory tree
        :return:
        """
        zfs = ZipFs(InMemoryZip())
        self.build_tree(zfs)

        # test that we can't overwrite files
        with pytest.raises(FsError):
            self.build_tree(zfs)

        # test that we can't create dirs on top of existing stuff
        for i in range(1, 10):
            with pytest.raises(FsError):
                zfs.mkdir(self.tree_filename.format(0, i))
            with pytest.raises(FsError):
                zfs.mkdir(self.tree_dirname.format(0, i))

        # verify tree
        self.verify_tree(zfs)
