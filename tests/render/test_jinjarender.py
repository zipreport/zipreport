import pytest

from tests.render.base import BaseTest
from zipreport.template import JinjaRender
from zipreport.report import REPORT_FILE_NAME


class TestJinjaRender(BaseTest):

    def test_render(self):
        # test render happy path
        zpt = self.build_zpt()
        render = JinjaRender(zpt)
        result = render.render()
        assert result is not None

        # check that output file was generated
        html_report = zpt.get(REPORT_FILE_NAME)
        assert html_report is not None
        html_report = str(html_report.read(), 'utf-8')
        assert html_report == str(result)
        assert html_report.find("Lorem ipsum dolor sit amet") > 0

    def test_exceptions(self):
        zpt = self.build_zpt()

        render = JinjaRender(zpt)
        # test exception if data keys don't match manifest.json specification
        with pytest.raises(RuntimeError):
            render.render({})

        # disable strict params
        render = JinjaRender(zpt, {JinjaRender.OPT_STRICT_PARAMS: False})
        render.render({})

    def test_discover_data(self):
        zpt = self.build_zpt()
        render = JinjaRender(zpt)

        # non-existing default data file
        empty_data = render._discover_data('non-existing-file')
        assert isinstance(empty_data, dict) is True
        assert len(empty_data.items()) == 0

        # existing default data file
        data = render._discover_data()
        assert isinstance(data, dict) is True
        assert len(data.items()) > 0

        # invalid data file
        with pytest.raises(RuntimeError):
            zpt.add('invalid.json', "")
            render._discover_data('invalid.json')
