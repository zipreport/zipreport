import os
import tempfile
from pathlib import Path
from shutil import rmtree

from tests.utils import SAMPLE1_PATH
from zipreport.report.builder import ReportFileBuilder
from zipreport.report.const import MANIFEST_AUTHOR
from zipreport.report.loader import ReportFileLoader
from zipreport.report.reportfile import ReportFile


class TestLoader:
    temp_dir = '/tmp'
    temp_methods = ['test_loader_pass', ]

    def setup_method(self, method):
        if method.__name__ in self.temp_methods:
            self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self, method):
        if method.__name__ in self.temp_methods:
            if os.path.exists(self.temp_dir) and self.temp_dir != '/tmp':
                rmtree(self.temp_dir)
                self.temp_dir = '/tmp'

    def test_loader_pass(self):
        # load from file
        destfile = Path(self.temp_dir) / 'test.zpt'

        # build zpt file
        result = ReportFileBuilder.build_file(SAMPLE1_PATH, destfile)
        assert result.success() is True
        assert destfile.exists() is True

        bundle = ReportFileLoader.load(destfile)
        assert bundle is not None
        assert isinstance(bundle, ReportFile) is True
        assert bundle.get_param(MANIFEST_AUTHOR) is not None

        # load from dir
        path = SAMPLE1_PATH
        bundle = ReportFileLoader.load(path)
        assert bundle is not None
        assert isinstance(bundle, ReportFile) is True
        assert bundle.get_param(MANIFEST_AUTHOR) is not None
