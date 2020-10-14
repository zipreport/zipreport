import os
from pathlib import Path

from tests.utils import SAMPLE1_PATH
from zipreport.fileutils import ZipFs
from zipreport.fileutils.backend.zip import InMemoryZip


class BaseZipTest:

    def create_sample1_zip(self, path=SAMPLE1_PATH) -> list:
        # create a zip file from examples/sample1
        assert os.path.exists(path) is True

        zipitems = 0
        zfs = ZipFs(InMemoryZip(None))
        for dirname, dirs, files in os.walk(path):
            dirname = Path(dirname)
            for fname in files:
                fname = dirname / Path(fname)
                with open(fname, 'rb') as fh:
                    zfs.add(str(fname.relative_to(path)), fh.read())
                    zipitems += 1
        return [path, zipitems, zfs]
