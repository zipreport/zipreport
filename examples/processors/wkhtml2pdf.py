import sys

from zipreport import WkHtml2PdfReport
from zipreport.report import ReportFileLoader

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2:
        print("Usage: python3 wkhtml2pdf.py <path_to_wkhtmltopdf_binary> <destination_file.pdf>")
        exit(1)

    cli_path = args[0]
    output_file = args[1]

    # template variables
    report_data = {
        'title': "Example report using Jinja templating",
        'color_list': ['red', 'blue', 'green'],
        'description': 'a long text field with some filler description so the page isn\'t that empty',
    }

    # load report from file
    zpt = ReportFileLoader.load("reports/simple.zpt")

    # render the report with default job options
    result = WkHtml2PdfReport(cli_path).render_defaults(zpt, report_data)

    if result.success:
        with open(output_file, 'wb') as rpt:
            rpt.write(result.report.read())
    else:
        print(f"Render failed: {result.error}")