# ZipReport Filter Example
#
import sys
from pathlib import Path

import markupsafe
from jinja2 import Environment, pass_environment

from zipreport import ZipReport
from zipreport.report import ReportFileBuilder, ReportFileLoader
from zipreport.template import EnvironmentWrapper


@pass_environment
def defoxifier(*args, **kwargs) -> markupsafe.Markup:
    """
    Example filter that replaces "fox" with "racoon"
    """
    al = len(args)
    if al < 2:
        raise RuntimeError("Invalid number of arguments")

    text = args[1].replace("fox", "racoon")
    return markupsafe.Markup(text)


class MyCustomWrapper(EnvironmentWrapper):
    def wrap(self, e: Environment) -> Environment:
        # register our fancy defoxifier filter
        e.filters["defoxifier"] = defoxifier
        return e


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: python3 main.py <destination_file.pdf>")
        exit(1)
    pdf_name = Path(args[0])  # output file path

    if pdf_name.exists():
        print("{} already exists".format(pdf_name))
        exit(1)

    # Assemble report directly from the report folder, without using zpt file
    # ReportFileBuilder.build_zipfs() will create an in-memory zpt file suitable to be used by the library
    # Not: when using zpt files, this step, as well as the assembly of the ReportFile object is not necessary;
    # instead, it could be loaded the following way:
    #
    # report = ReportFileLoader.load(zpt_file_path)
    #
    report_path = Path("../../reports/env_wrapper/custom_filter_example").absolute()
    status, zfs = ReportFileBuilder.build_zipfs(report_path)
    if not status.success():
        print("Error loading the report")
        exit(1)

    # assemble ReportFile object from the in-memory zfs
    report = ReportFileLoader.load_zipfs(zfs)

    # template variables
    report_data = {
        "title_text": "the quick brown fox jumps over the lazy dog",
    }

    # create custom wrapper object
    my_wrapper = MyCustomWrapper()

    # render using zipreport processor
    result = ZipReport("https://127.0.0.1:6543", "somePassword").render_defaults(
        report, report_data, wrapper=my_wrapper
    )
    if not result.success:
        print("An error occured while generating the pdf:", result.error)
        exit(1)

    # save io.BytesIO buffer to file
    with open(pdf_name, "wb") as f:
        f.write(result.report.read())

    print("Report generated to {}".format(pdf_name))
