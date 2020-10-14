import json
import os
import tempfile
from pathlib import Path
from shutil import rmtree

from tests.utils import SAMPLE1_PATH
from zipreport.report.builder import ReportFileBuilder
from zipreport.report.const import ZIPREPORT_FILE_EXTENSION


class TestReportFileBuilder:
    temp_dir = '/tmp'
    temp_methods = ['test_builder_success', 'test_builder_fail', 'test_builder_required_files']

    manifest = {
        "author": "some_author",
        "title": "Sample report 1",
        "description": "Sample report",
        "version": "1.0",
        "params": [],
        "config": {}
    }

    def setup_method(self, method):
        if method.__name__ in self.temp_methods:
            self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self, method):
        if method.__name__ in self.temp_methods:
            if os.path.exists(self.temp_dir) and self.temp_dir != '/tmp':
                rmtree(self.temp_dir)
                self.temp_dir = '/tmp'

    def test_builder_success(self):
        destfile = Path(self.temp_dir) / 'test'

        result = ReportFileBuilder.build_file(SAMPLE1_PATH, destfile)
        assert result.success() is True
        # this should fail because we automatically added an extension
        assert destfile.exists() is False

        # test actual created file
        destfile = destfile.parent / (destfile.name + ZIPREPORT_FILE_EXTENSION)
        assert destfile.exists() is True

    def test_builder_fail(self):
        destfile = Path(self.temp_dir) / 'test.zpt'

        # invalid path
        result = ReportFileBuilder.build_file(os.path.dirname(__file__), destfile)
        assert result.success() is False
        assert len(result.get_errors()) == 1

        # dest file exists and overwrite is False
        with open(destfile, 'wb') as f:
            f.write(b"abc")
        result = ReportFileBuilder.build_file(SAMPLE1_PATH, destfile)
        assert result.success() is False
        assert len(result.get_errors()) == 1
        # try again with overwrite
        result = ReportFileBuilder.build_file(SAMPLE1_PATH, destfile, overwrite=True)
        assert result.success() is True

    def test_builder_required_files(self):
        path = Path(self.temp_dir)
        destfile = Path(self.temp_dir) / 'test.zpt'

        # failure by lack of manifest
        result = ReportFileBuilder.build_file(path, destfile)
        assert result.success() is False
        assert len(result.get_errors()) == 1

        # failure by invalid manifest
        manifest = path / 'manifest.json'
        self._touch(manifest, b'abc')
        result = ReportFileBuilder.build_file(path, destfile)
        assert result.success() is False

        # valid manifest, now fail by lack of index.html
        manifest.unlink()
        self._touch(manifest, bytes(json.dumps(self.manifest), encoding='utf8'))
        result = ReportFileBuilder.build_file(path, destfile)
        assert result.success() is False

        # add an index.html and should work
        index = path / 'index.html'
        self._touch(index, b'<html>')
        result = ReportFileBuilder.build_file(path, destfile)
        assert result.success() is True

    def _touch(self, file, contents):
        with open(file, 'wb') as f:
            f.write(contents)
