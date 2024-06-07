import os
import tempfile
from pathlib import Path
from shutil import rmtree

from tests.utils import RPT_SIMPLE_PATH, CUSTOM_ENV_PATH
from zipreport.report import ReportFileBuilder, ReportFileLoader


class BaseTest:
    temp_dir = "/tmp"

    def setup_method(self, method):
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self, method):
        if os.path.exists(self.temp_dir) and self.temp_dir != "/tmp":
            rmtree(self.temp_dir)
            self.temp_dir = "/tmp"

    def build_zpt(self):
        zptfile = Path(self.temp_dir) / "test.zpt"

        result = ReportFileBuilder.build_file(RPT_SIMPLE_PATH, zptfile)
        assert result.success() is True
        zpt = ReportFileLoader.load_file(zptfile)
        assert zpt is not None
        return zpt

    def build_customenv_zpt(self):
        zptfile = Path(self.temp_dir) / "customenv.zpt"

        result = ReportFileBuilder.build_file(CUSTOM_ENV_PATH, zptfile)
        assert result.success() is True
        zpt = ReportFileLoader.load_file(zptfile)
        assert zpt is not None
        return zpt
