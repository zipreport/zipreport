import io
import sys
from pathlib import Path

from PIL import Image

from zipreport import ZipReportCli
from zipreport.report import ReportFileLoader


# dynamic png generation
def render_image(color='red') -> io.BytesIO:
    # generate a rectangle with the specified color
    img = Image.new('RGB', (256, 256), color=color)
    # save generated image to a memory buffer
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    # rewind to the beginning of the buffer
    buffer.seek(0)
    return buffer


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
        print("{} already exists".format(pdf_name))
        exit(1)

    report_name = "simple_report.zpt"
    report = ReportFileLoader.load(report_name)

    # template variables
    report_data = {
        # our callback function to generate the image
        'colored_rectangle_fn': render_image,
        # desired color to use
        'rectangle_color': 'pink',
    }

    # render using zipreport-cli processor
    result = ZipReportCli(zipreport_cli).render_defaults(report, report_data)
    if not result.success:
        print("An error occured while generating the pdf:", result.error)
        exit(1)

    # save io.BytesIO buffer to file
    with open(pdf_name, 'wb') as f:
        f.write(result.report.read())

    print("Report generated to {}".format(pdf_name))
