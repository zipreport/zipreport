# CSS Paged Media example using zipreport-server
#
# Demonstrates CSS Paged Media features supported by Chromium:
# - @page rules with margin boxes
# - Page counters (counter(page), counter(pages))
# - Page breaks (break-before, break-after, break-inside)
# - Widows and orphans control
# - Named pages
#
# Note: For running headers (string-set/string()) and TOC page numbers
# (target-counter), use WeasyPrint instead - see the weasyprint example.
#
import os
import sys
from pathlib import Path

from zipreport import ZipReport
from zipreport.report import ReportFileLoader

ZIPREPORT_URL = os.getenv("ZIPREPORT_URL", "https://127.0.0.1:6543")
ZIPREPORT_KEY = os.getenv("ZIPREPORT_KEY", "somePassword")

# Path to Chrome-compatible print_css report template
REPORT_PATH = Path(__file__).parent / ".." / ".." / "reports" / "print_css_chrome"


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
        print("Report template not found at {}".format(REPORT_PATH))
        exit(1)

    # Load report directly from directory
    report = ReportFileLoader.load(REPORT_PATH)

    # Template variables demonstrating CSS Paged Media features
    report_data = {
        "title": "CSS Paged Media Report",
        "author": "ZipReport Team",
        "date": "January 2026",
        "chapters": [
            {
                "title": "Introduction to Paged Media",
                "content": "This report demonstrates CSS Paged Media features supported "
                "by Chromium's headless PDF renderer. These features allow control over "
                "page layout, page breaks, and page numbering when generating PDF "
                "documents from HTML templates.",
            },
            {
                "title": "Page Layout and Margins",
                "content": "The @page rule defines page dimensions and margins. This "
                "template uses A4 page size with customized margins. Named pages allow "
                "different sections to have distinct layouts - the cover page uses zero "
                "margins for a full-bleed design.",
            },
            {
                "title": "Page Counters and Numbering",
                "content": "Chromium supports page counters using counter(page) for the "
                "current page and counter(pages) for the total. These are displayed in "
                "margin boxes defined within @page rules, showing 'Page X of Y' format.",
            },
            {
                "title": "Page Breaks and Fragmentation",
                "content": "The break-before, break-after, and break-inside properties "
                "control content flow across pages. Each chapter uses break-before: page "
                "to start on a new page. Tables and figures use break-inside: avoid.",
            },
            {
                "title": "Widows and Orphans",
                "content": "The widows and orphans properties prevent awkward text breaks "
                "at page boundaries. This template ensures at least three lines appear "
                "at the top and bottom of each page for professional typography.",
            },
        ],
    }

    # Render using zipreport-server processor
    result = ZipReport(ZIPREPORT_URL, ZIPREPORT_KEY).render_defaults(report, report_data)
    if not result.success:
        print("An error occurred while generating the report:", result.error)
        exit(1)

    # Save PDF to file
    with open(pdf_name, "wb") as f:
        f.write(result.report.read())

    print("Report generated to {}".format(pdf_name))
