import json
from copy import deepcopy

from jinja2 import select_autoescape, Environment

from zipreport.template.jinjaloader import JinjaReportLoader
from zipreport.report import ReportFile
from zipreport.report.const import INDEX_FILE_NAME, MANIFEST_PARAMETERS, REPORT_FILE_NAME, DATA_FILE_NAME
# register filters
from zipreport.template.jinja import filters


class JinjaRender:
    OPT_EXTENSIONS = 'extensions'
    OPT_STRICT_PARAMS = 'strict_params'

    DEFAULT_OPTIONS = {
        OPT_EXTENSIONS: [],
        OPT_STRICT_PARAMS: True,
    }

    def __init__(self, zpt: ReportFile, options: dict = None):
        """
        jinja Renderer

        :param zpt: ReportFile to use
        :param options: extension details to be passed to jinja
        """
        self.zpt = zpt
        self.env = None
        self.options = deepcopy(self.DEFAULT_OPTIONS)
        if options is not None:
            self.options = {**self.options, **options}

    def get_env(self) -> Environment:
        """
        Build jinja environment

        :return:  Environment
        """
        return Environment(
            loader=JinjaReportLoader(self.zpt),
            autoescape=select_autoescape(['html', 'xml']),
            extensions=self.options[self.OPT_EXTENSIONS]
        )

    def check_params(self, data: dict):
        """
        Check that all parameters specified on the manifest file exist, if strict params enabled

        :param data: data to validate
        :return: bool
        """
        if not self.options[self.OPT_STRICT_PARAMS]:
            return

        expected = self.zpt.get_param(MANIFEST_PARAMETERS)
        for param in expected:
            if param not in data.keys():
                raise RuntimeError("Parameter '{}' missing on render() call".format(param))

    def render(self, data: dict = None, template: str = INDEX_FILE_NAME,
               default_data_file: str = DATA_FILE_NAME) -> str:
        """
        Render the template into REPORT_FILE_NAME, inside the ReportFile

        if data is None, render() will try to load a default json data file to use as data to be passed to the view
        Keep in mind, zipreport dynamic filters can't be used as default data

        :param data: data to be passed to the template
        :param template: main template file
        :param default_data_file: optional json data file to be used as default
        :return: result of the rendering
        """

        if data is None:
            data = self._discover_data(default_data_file)
        self.check_params(data)

        template = self.get_env().get_template(template)
        contents = template.render(**data)
        self.zpt.add(REPORT_FILE_NAME, contents)
        return contents

    def _discover_data(self, data_file: str = DATA_FILE_NAME) -> dict:
        """
        Loads default data from json, if data_file exists

        :param data_file:
        :return: dict
        """
        result = {}
        if self.zpt.exists(data_file):
            try:
                result = dict(json.loads(self.zpt.get(data_file).read()))
            except json.JSONDecodeError:
                raise RuntimeError("Default data file {} is invalid".format(data_file))
        return result
