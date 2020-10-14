import os
import tempfile
from pathlib import Path
from shutil import rmtree

from zipreport.report import ReportFileBuilder, ReportFileLoader


class BaseTest:
    temp_dir = '/tmp'

    def setup_method(self, method):
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self, method):
        if os.path.exists(self.temp_dir) and self.temp_dir != '/tmp':
            rmtree(self.temp_dir)
            self.temp_dir = '/tmp'

    def build_zpt(self, report:str):
        zptfile = Path(self.temp_dir) / 'test.zpt'

        result = ReportFileBuilder.build_file(report, zptfile)
        assert result.success() is True
        zpt = ReportFileLoader.load_file(zptfile)
        assert zpt is not None
        return zpt
