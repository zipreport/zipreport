import pytest
from jinja2 import TemplateNotFound

from tests.render.base import BaseTest
from zipreport.template import JinjaReportLoader


class TestJinjaRender(BaseTest):

    def test_loader(self):
        # test render happy path
        zpt = self.build_zpt()
        loader = JinjaReportLoader(zpt)

        src, template, update = loader.get_source(None, 'index.html')
        assert len(src) > 0
        assert template == 'index.html'
        assert update() is True

        with pytest.raises(TemplateNotFound):
            loader.get_source(None, 'non-existing-template.html')
