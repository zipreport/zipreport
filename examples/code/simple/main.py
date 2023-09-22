# Simple ZipReport example
#
import sys
from pathlib import Path

from zipreport import ZipReportCli
from zipreport.report import ReportFileLoader

if __name__ == "__main__":

    args = sys.argv[1:]
    if len(args) != 2:
        print("Usage: python3 main.py <path_to_zptcli_binary> <destination_file.pdf>")
        exit(1)
    zipreport_cli = Path(args[0])  # zipreport-cli binary path
    pdf_name = Path(args[1])  # output file path

    if not zipreport_cli.exists() or zipreport_cli.is_dir():
        print("zpt-cli not found")
        exit(1)

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
    result = ZipReportCli(zipreport_cli).render_defaults(report, report_data)
    if not result.success:
        print("An error occured while generating the report:", result.error)
        exit(1)

    # save io.BytesIO buffer to file
    with open(pdf_name, 'wb') as f:
        f.write(result.report.read())

    print(f"Report generated to {pdf_name}")
