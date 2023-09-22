# ZipReport Filter Example
#
import io
import sys
from pathlib import Path

import svgwrite
from PIL import Image

from zipreport import ZipReportCli
from zipreport.report import ReportFileBuilder, ReportFileLoader


def render_image(color='red', format='PNG'):
    img = Image.new('RGB', (256, 256), color=color)
    buffer = io.BytesIO()
    img.save(buffer, format=format)
    buffer.seek(0)
    return buffer


def render_png(data):
    return render_image(data, 'PNG')


def render_gif(data):
    return render_image(data, 'GIF')


def render_jpg(data):
    return render_image(data, 'JPEG')


def render_svg(data):
    dwg = svgwrite.Drawing(profile='tiny')
    shapes = dwg.add(dwg.g(id='shapes', fill=data))
    shapes.add(dwg.rect(insert=(0, 0), size=(100, 100), fill=data))
    # StringIO is used because buffer.write() needs to accept string-like data
    buffer = io.StringIO()
    dwg.write(buffer)
    buffer.seek(0)
    # convert string buffer into bytes
    return bytes(buffer.read(), encoding='utf-8')


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

    # Assemble report directly from the report folder, without using zpt file
    # ReportFileBuilder.build_zipfs() will create an in-memory zpt file suitable to be used by the library
    # Not: when using zpt files, this step, as well as the assembly of the ReportFile object is not necessary;
    # instead, it could be loaded the following way:
    #
    # report = ReportFileLoader.load(zpt_file_path)
    #
    report_path = Path("../../reports/filter_example").absolute()
    status, zfs = ReportFileBuilder.build_zipfs(report_path)
    if not status.success():
        print("Error loading the report")
        exit(1)

    # assemble ReportFile object from the in-memory zfs
    report = ReportFileLoader.load_zipfs(zfs)

    # template variables
    report_data = {
        'png_graphic': render_png,
        'png_graphic_data': 'pink',
        'gif_graphic': render_gif,
        'gif_graphic_data': 'blue',
        'jpg_graphic': render_jpg,
        'jpg_graphic_data': 'green',
        'svg_graphic': render_svg,
        'svg_graphic_data': 'yellow',
    }

    # render using zipreport-cli processor
    result = ZipReportCli(zipreport_cli).render_defaults(report, report_data)
    if not result.success:
        print("An error occured while generating the pdf:", result.error)
        exit(1)

    # save io.BytesIO buffer to file
    with open(pdf_name, 'wb') as f:
        f.write(result.report.read())

    print(f"Report generated to {pdf_name}")
