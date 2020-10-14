import io

from jinja2 import BaseLoader, TemplateNotFound
from zipreport.report import ReportFile


class JinjaReportLoader(BaseLoader):

    def __init__(self, zpt: ReportFile):
        self.zpt = zpt

    def get_source(self, environment, template):
        def updated():
            return True

        if not self.zpt.exists(template):
            raise TemplateNotFound(template)
        source = io.TextIOWrapper(self.zpt.get(template), encoding='utf-8').read()
        return source, template, updated

    def get_report(self):
        """
        Retrieve Report Object
        :return: ReportFile
        """
        return self.zpt

    def list_templates(self):
        """Iterates over all templates.  If the loader does not support that
        it should raise a :exc:`TypeError` which is the default behavior.
        """
        raise TypeError("this loader cannot iterate over all templates")
