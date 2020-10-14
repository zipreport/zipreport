import os
import tempfile
from pathlib import Path
from shutil import rmtree

import pytest

from tests.utils import SAMPLE1_PATH
from .basefs import BaseFsTest
from zipreport.fileutils import DiskFs, FsError


class TestDiskFs(BaseFsTest):
    dname = 'this_test_dir'
    fname = 'this_test_file.txt'
    fcontents = b"The quick brown fox jumped over the lazy dog"

    temp_dir = '/tmp'
    temp_methods = ['test_diskfs_tree', 'test_diskfs_files']

    def setup_method(self, method):
        if method.__name__ in self.temp_methods:
            self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self, method):
        if method.__name__ in self.temp_methods:
            if os.path.exists(self.temp_dir) and self.temp_dir != '/tmp':
                rmtree(self.temp_dir)
                self.temp_dir = '/tmp'

    def test_diskfs_list(self):
        """
        Simple diskfs operations on examples/sample1
        :return:
        """
        path = Path(SAMPLE1_PATH)
        dfs = DiskFs(path)
        assert dfs.get_backend() is None

        rootdirs, rootfiles, items = self.path_walk(path)

        assert len(items) > 0
        assert len(rootdirs) > 0
        assert len(rootfiles) > 0
        assert len(dfs.list('')) == len(items)
        assert len(dfs.list_dirs('/')) == len(rootdirs)
        assert len(dfs.list_files('/')) == len(rootfiles)

        for dir in dfs.list_dirs('/'):
            assert dir in rootdirs
            assert dfs.is_dir(dir) is True
        for file in dfs.list_files('/'):
            assert file in rootfiles
            assert dfs.is_dir(file) is False

    def test_diskfs_files(self):
        """
        Simple add/get tests
        :return:
        """
        path = Path(self.temp_dir)
        dfs = DiskFs(path)

        assert dfs.exists(self.fname) is False
        # == add file to root
        dfs.add(self.fname, self.fcontents)

        # can we read the file?
        assert dfs.exists(self.fname) is True
        assert dfs.get(self.fname).getbuffer() == self.fcontents

        # check if file was created
        fpath = path / self.fname
        with open(fpath, 'rb') as f:
            assert f.read() == self.fcontents
        os.unlink(fpath)

        # == add file to new dir
        assert dfs.exists(self.dname) is False
        dfs.mkdir(self.dname)
        assert dfs.exists(self.dname) is True
        dfs.add(os.path.join(self.dname, self.fname), self.fcontents)

        # can we read the file?
        assert dfs.get(os.path.join(self.dname, self.fname)).getbuffer() == self.fcontents

        # check if file was created inside dname
        fpath = path / self.dname / self.fname
        with open(fpath, 'rb') as f:
            assert f.read() == self.fcontents
        os.unlink(fpath)
        os.rmdir(path / self.dname)

    def test_diskfs_tree(self):
        """
        Test a full directory tree
        :return:
        """
        dfs = DiskFs(self.temp_dir)
        self.build_tree(dfs)

        # test that we can't overwrite files
        with pytest.raises(FsError):
            self.build_tree(dfs)

        # test that we can't create dirs on top of existing stuff
        for i in range(1, 10):
            with pytest.raises(FsError):
                dfs.mkdir(self.tree_filename.format(0, i))
            with pytest.raises(FsError):
                dfs.mkdir(self.tree_dirname.format(0, i))

        # verify tree
        self.verify_tree(dfs)
