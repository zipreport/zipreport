# CSS Paged Media example using Chromium/zipreport-server
#
# This example demonstrates CSS Paged Media features supported by Chromium:
# - @page rules with margin boxes
# - Page counters (counter(page), counter(pages))
# - Page breaks (break-before, break-after, break-inside)
# - Widows and orphans control
# - Named pages
#
import json
import os
import sys
from pathlib import Path

from zipreport import ZipReport
from zipreport.report import ReportFileBuilder, ReportFileLoader

ZIPREPORT_URL = os.getenv("ZIPREPORT_URL", "https://127.0.0.1:6543")
ZIPREPORT_KEY = os.getenv("ZIPREPORT_KEY", "somePassword")

# Path to the report template directory
REPORT_PATH = Path(__file__).parent.parent.parent / "reports" / "print_css_chrome"


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: python3 main.py <destination_file.pdf>")
        exit(1)
    pdf_name = Path(args[0])

    if pdf_name.exists():
        print("{} already exists".format(pdf_name))
        exit(1)

    if not REPORT_PATH.exists():
        print("Report template not found at: {}".format(REPORT_PATH))
        exit(1)

    # Build report from directory - returns (status, zipfs)
    status, zfs = ReportFileBuilder.build_zipfs(REPORT_PATH)
    if not status.success():
        print("Error building report: {}".format(status.error()))
        exit(1)

    # Load ReportFile from the in-memory zipfs
    report = ReportFileLoader.load_zipfs(zfs)

    # Load sample data from data.json
    data_file = REPORT_PATH / "data.json"
    if data_file.exists():
        with open(data_file, "r") as f:
            report_data = json.load(f)
    else:
        # Fallback data if data.json doesn't exist
        report_data = {
            "title": "CSS Paged Media Report",
            "author": "ZipReport Team",
            "date": "January 2026",
            "chapters": [
                {
                    "title": "Introduction",
                    "content": "This is an example report demonstrating CSS Paged Media features."
                }
            ]
        }

    # Render using zipreport-server processor (Chromium)
    result = ZipReport(ZIPREPORT_URL, ZIPREPORT_KEY).render_defaults(report, report_data)
    if not result.success:
        print("An error occurred while generating the report:", result.error)
        exit(1)

    # Save PDF to file
    with open(pdf_name, "wb") as f:
        f.write(result.report.read())

    print("Report generated to {}".format(pdf_name))
