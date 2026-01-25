# ZipReport WeasyPrint Example
#
# Demonstrates PDF generation using WeasyPrint (no server required).
#
import sys
from pathlib import Path

from zipreport.processors.weasyprint import WeasyPrintProcessor
from zipreport.report import ReportFileBuilder, ReportFileLoader, ReportJob
from zipreport.template import JinjaRender

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: python3 main.py <destination_file.pdf>")
        exit(1)
    pdf_name = Path(args[0])  # output file path

    if pdf_name.exists():
        print("{} already exists".format(pdf_name))
        exit(1)

    # load the print_css report template from directory
    report_path = Path(__file__).parent / "../../reports/print_css"
    status, zfs = ReportFileBuilder.build_zipfs(report_path)
    if not status.success():
        print("Error loading the report")
        exit(1)
    report = ReportFileLoader.load_zipfs(zfs)

    # template variables
    report_data = {
        "title": "CSS Paged Media Report",
        "author": "ZipReport Team",
        "date": "January 2026",
        "chapters": [
            {
                "title": "Introduction",
                "content": "This report demonstrates modern CSS Paged Media features "
                "supported by WeasyPrint.",
            },
            {
                "title": "Page Layout",
                "content": "CSS Paged Media provides the @page rule for defining page "
                "dimensions, margins, and named pages.",
            },
            {
                "title": "Running Headers",
                "content": "Using margin boxes, we can place running content in the page "
                "margins with string-set and page counters.",
            },
        ],
    }

    # render the Jinja template
    JinjaRender(report).render(report_data)

    # create a WeasyPrint processor with optional extra CSS
    processor = WeasyPrintProcessor()

    # add_css() accepts weasyprint.CSS objects; example with inline CSS string:
    # from weasyprint import CSS
    # processor.add_css(CSS(string="body { font-size: 12pt; }"))

    # set_font_config() allows custom font configuration:
    # from weasyprint.text.fonts import FontConfiguration
    # font_config = FontConfiguration()
    # processor.set_font_config(font_config)

    # process the report job
    job = ReportJob(report)
    result = processor.process(job)

    if not result.success:
        print("An error occurred while generating the pdf:", result.error)
        exit(1)

    # save the PDF
    with open(pdf_name, "wb") as f:
        f.write(result.report.read())

    print("Report generated to {}".format(pdf_name))
