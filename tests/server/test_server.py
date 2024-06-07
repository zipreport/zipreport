import io
import os
import tempfile
from pathlib import Path
from PIL import Image
import pytest

from tests.utils import SAMPLE1_PATH, RPT_PAGEDJS_PATH
from zipreport import ZipReport
from zipreport.processors.weasyprint import WeasyPrintProcessor
from zipreport.report import ReportFileBuilder, ZIPREPORT_FILE_EXTENSION, ReportFileLoader, ReportJob
from shutil import rmtree

from zipreport.template import JinjaRender


@pytest.fixture
def api_host():
    return "127.0.0.1"


@pytest.fixture
def api_key():
    return os.getenv("ZIPREPORT_API_KEY", "somePassword")


@pytest.fixture
def api_port():
    return os.getenv("ZIPREPORT_API_PORT", 6543)


def png_rectangle(data) -> io.BytesIO:
    # generate a rectangle with the specified color
    img = Image.new('RGB', (256, 256))
    # save generated image to a memory buffer
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    # rewind to the beginning of the buffer
    buffer.seek(0)
    return buffer


class TestReportRenderServer:
    temp_dir = tempfile.gettempdir()

    def setup_method(self, method):
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self, method):
        if os.path.exists(self.temp_dir) and self.temp_dir != "/tmp":
            rmtree(self.temp_dir)
            self.temp_dir = "/tmp"

    def test_render_sample1(self, api_host, api_port, api_key):
        destfile = Path(self.temp_dir) / "sample1"

        result = ReportFileBuilder.build_file(SAMPLE1_PATH, destfile)
        assert result.success() is True
        assert destfile.exists() is False
        destfile = destfile.parent / (destfile.name + ZIPREPORT_FILE_EXTENSION)
        assert destfile.exists() is True

        # prepare rendering
        url = "https://{}:{}".format(api_host, api_port)
        zpt = ReportFileLoader.load(destfile)
        client = ZipReport(url, api_key)
        result = client.render_defaults(zpt, {"plot1": png_rectangle})
        assert result.success is True
        buf = result.report.read()
        assert len(buf) > 1000

    def test_render_pagedjs(self, api_host, api_port, api_key):
        destfile = Path(self.temp_dir) / "pagedjs"

        result = ReportFileBuilder.build_file(RPT_PAGEDJS_PATH, destfile)
        assert result.success() is True
        assert destfile.exists() is False
        destfile = destfile.parent / (destfile.name + ZIPREPORT_FILE_EXTENSION)
        assert destfile.exists() is True

        # prepare rendering
        data = {
            "date": "1 Jan 2023",
            "author": "ZipReport Team",
            "gen_graphics_1": "https://placehold.co/250",
            "graphics_1": "",
            "gen_graphics_2": "https://placehold.co/250",
            "graphics_2": ""
        }
        url = "https://{}:{}".format(api_host, api_port)
        zpt = ReportFileLoader.load(destfile)
        client = ZipReport(url, api_key)
        job = client.create_job(zpt)
        job.use_jsevent(True)
        result = client.render(job, data)
        assert result.success is True
        buf = result.report.read()
        assert len(buf) > 1000

    def test_render_weasyprint(self, api_host, api_port, api_key):
        destfile = Path(self.temp_dir) / "sample1"

        result = ReportFileBuilder.build_file(SAMPLE1_PATH, destfile)
        assert result.success() is True
        assert destfile.exists() is False
        destfile = destfile.parent / (destfile.name + ZIPREPORT_FILE_EXTENSION)
        assert destfile.exists() is True

        # prepare rendering
        zpt = ReportFileLoader.load(destfile)
        JinjaRender(zpt).render({"plot1": png_rectangle})
        job = ReportJob(zpt)
        result = WeasyPrintProcessor().process(job)
        assert result.success is True
        buf = result.report.read()
        assert len(buf) > 1000
