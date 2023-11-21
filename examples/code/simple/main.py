# Simple ZipReport example
#
import sys
from pathlib import Path

from zipreport import ZipReport
from zipreport.report import ReportFileLoader

if __name__ == "__main__":

    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: python3 main.py <destination_file.pdf>")
        exit(1)
    pdf_name = Path(args[0])  # output file path

    if pdf_name.exists():
        print(f"{pdf_name} already exists")
        exit(1)

    report_path = Path('simple.zpt')
    if not report_path.exists():
        print("Missing report file. Did you run build.py first?")
        exit(1)

    # load report from file
    report = ReportFileLoader.load(report_path)

    # template variables
    report_data = {
        'title': "Example report using Jinja templating",
        'color_list': ['red', 'blue', 'green'],
        'description': 'a long text field with some filler description so the page isn\'t that empty',
    }

    # render using zipreport-cli processor
    result = ZipReport("https://127.0.0.1:6543", "somePassword").render_defaults(report, report_data)
    if not result.success:
        print("An error occured while generating the report:", result.error)
        exit(1)

    # save io.BytesIO buffer to file
    with open(pdf_name, 'wb') as f:
        f.write(result.report.read())

    print(f"Report generated to {pdf_name}")
