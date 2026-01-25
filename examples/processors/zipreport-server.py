import os
import sys
from pathlib import Path

from zipreport import ZipReport
from zipreport.report import ReportFileBuilder, ReportFileLoader

ZIPREPORT_URL = os.getenv("ZIPREPORT_URL", "https://127.0.0.1:6543")
ZIPREPORT_KEY = os.getenv("ZIPREPORT_KEY", "somePassword")

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: python3 zipreport-server.py <destination_file.pdf>")
        exit(1)

    output_file = args[0]

    # template variables
    report_data = {
        "title": "Example report using Jinja templating",
        "color_list": ["red", "blue", "green"],
        "description": "a long text field with some filler description so the page isn't that empty",
    }

    # load report from directory
    report_path = Path(__file__).parent / "../reports/simple"
    status, zfs = ReportFileBuilder.build_zipfs(report_path)
    if not status.success():
        print("Error loading the report")
        exit(1)
    zpt = ReportFileLoader.load_zipfs(zfs)

    # render the report with default job options
    result = ZipReport(ZIPREPORT_URL, ZIPREPORT_KEY).render_defaults(
        zpt, report_data
    )

    if not result.success:
        print("An error occurred while generating the report:", result.error)
        exit(1)

    with open(output_file, "wb") as rpt:
        rpt.write(result.report.read())

    print("Report generated to {}".format(output_file))
