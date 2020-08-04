import os
from pathlib import Path

from zipreport.fileutils import FsInterface, DiskFs, ZipFs

TREE_LEVEL = 4


class BaseFsTest:
    tree_filename = "document_{}_{}.txt"
    tree_dirname = "directory_{}_{}"
    tree_content = "The quick brown fox jumped over the lazy dog {}-{}"
    tree_dir_count = 10
    tree_file_count = 10
    tree_level = TREE_LEVEL

    def build_tree(self, fs: FsInterface, path='/', level=tree_level):
        """
        Create a FS tree of x tree_level
        each dir will have 10 files and 10 dirs
        :param fs:
        :param path:
        :param level:
        :return:
        """
        desc_level = self.tree_level - level
        if level == 0:
            return

        # create files
        for i in range(self.tree_file_count):
            name = self.tree_filename.format(desc_level, i)
            fs.add(os.path.join(path, name), bytes(self.tree_content.format(desc_level, i), encoding='utf8'))

        # create dirs
        # last level are just empty dirs, so we skip it
        if level-1 > 0:
            for i in range(self.tree_dir_count):
                name = self.tree_dirname.format(desc_level, i)
                dirname = os.path.join(path, name)
                if isinstance(fs, DiskFs):
                    fs.mkdir(dirname)
                self.build_tree(fs, dirname, level - 1)

    def verify_tree(self, fs: FsInterface, path='/', level=TREE_LEVEL):
        """
        Verify FS tree contents
        :param fs:
        :param path:
        :param level:
        :return:
        """
        desc_level = self.tree_level - level
        if level == 0:
            return

        # verify listings
        list_dirs = fs.list_dirs(path)
        list_files = fs.list_files(path)
        list_all = fs.list(path)
        if level -1 > 0:
            assert len(list_dirs) == self.tree_dir_count
        assert len(list_files) == self.tree_file_count

        # verify list_all
        expected_files, expected_dirs = self.gen_fnames_dirnames('/', level)
        list_all_expected = expected_dirs + expected_files
        assert len(list_all) == len(list_all_expected)
        for item in list_all:
            assert item in list_all_expected

        # verify files
        for i in range(self.tree_file_count):
            name = self.tree_filename.format(desc_level, i)
            assert name in list_files
            expected = bytes(self.tree_content.format(desc_level, i), encoding='utf8')
            contents = fs.get(os.path.join(path, name))
            assert contents.getbuffer() == expected
            assert fs.exists(os.path.join(path, name)) is True

        # verify dirs
        # last level are just empty dirs, so we skip it
        if level-1 > 0:
            for i in range(self.tree_dir_count):
                name = self.tree_dirname.format(desc_level, i)
                dirname = os.path.join(path, name)
                assert fs.is_dir(dirname) is True
                assert fs.exists(dirname) is True
                # all dirnames end with "/"
                assert name + '/' in list_dirs

                # recurse
                self.verify_tree(fs, dirname, level - 1)

    def gen_fnames_dirnames(self, path='/', level=TREE_LEVEL):
        """
        Generate a list of all filenames and dirnames from the specified path
        :param path:
        :param level:
        :return:
        """
        path = path.lstrip('/')
        desc_level = self.tree_level - level
        fnames = []
        dirnames = []
        if level == 0:
            return fnames, dirnames
        for i in range(self.tree_file_count):
            name = self.tree_filename.format(desc_level, i)
            fnames.append(os.path.join(path, name))

        if level -1 > 0:
            for i in range(self.tree_dir_count):
                # all dirs have trailing slash
                # all paths don't have root slash
                name = self.tree_dirname.format(desc_level, i) + '/'
                dirname = os.path.join(path, name)
                dirnames.append(dirname)
                a, b = self.gen_fnames_dirnames(dirname, level - 1)
                dirnames.extend(b)
                fnames.extend(a)

        return fnames, dirnames

    def path_walk(self, path):
        """
        Retrieve recursive list of dirs and files
        :param path:
        :return:
        """
        items = []
        rootdirs = []
        rootfiles = []
        first_dir = False
        first_files = False
        for dirname, dirs, files in os.walk(path):
            for d in dirs:
                name = Path(dirname) / d
                rel = str(name.relative_to(path)) + os.sep
                items.append(rel)
                # we collect dirs only on root path
                if not first_dir:
                    rootdirs.append(rel)
            for f in files:
                name = Path(dirname) / f
                rel = str(name.relative_to(path))
                items.append(rel)
                # we collect files only on root path
                if not first_files:
                    rootfiles.append(rel)
            first_dir = True
            first_files = True

        return rootdirs, rootfiles, items