from jinja2 import select_autoescape, Environment

from zipreport.jinja2.loader import ReportLoader
from zipreport.report import ReportFile
from zipreport.report.const import INDEX_FILE_NAME, MANIFEST_PARAMETERS, REPORT_FILE_NAME
from zipreport.jinja2.filters.filters import placeholder

class JinjaRender:
    OPT_EXTENSIONS = 'extensions'
    OPT_STRICT_PARAMS = 'strict_params'

    default_options = {
        OPT_EXTENSIONS: [],
        OPT_STRICT_PARAMS: True,
    }

    def __init__(self, zpt: ReportFile, options: dict = None):
        self.zpt = zpt
        self.env = None
        self.options = self.default_options
        if options is not None:
            self.options = {**self.default_options, **options}

    def get_env(self):
        return Environment(
            loader=ReportLoader(self.zpt),
            autoescape=select_autoescape(['html', 'xml']),
            extensions=self.options[self.OPT_EXTENSIONS]
        )

    def check_params(self, data: dict) -> bool:
        expected = self.zpt.get_param(MANIFEST_PARAMETERS)
        for k in data.keys():
            if k not in expected:
                if self.options[self.OPT_STRICT_PARAMS]:
                    raise RuntimeError("Parameter '{}' missing on render() call".format(k))
                return False
        return True

    def render(self, data: dict = None, template=INDEX_FILE_NAME) -> str:
        if data is None:
            # @todo: load default template data
            data = {}
        template = self.get_env().get_template(template)
        contents = template.render(**data)
        self.zpt.add(REPORT_FILE_NAME, contents)
        return contents
