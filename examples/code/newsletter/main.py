# Newsletter MIMEProcessor example
#
import sys
from pathlib import Path
from email.policy import SMTP

from zipreport import MIMEReport
from zipreport.report import ReportFileBuilder, ReportFileLoader

if __name__ == "__main__":

    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: python3 main.py <destination_file.eml>")
        exit(1)

    email_name = Path(args[0])  # output file path
    if email_name.exists():
        print(f"{email_name} already exists")
        exit(1)

    # Assemble report directly from the report folder, without using zpt file
    # ReportFileBuilder.build_zipfs() will create an in-memory zpt file suitable to be used by the library
    # Not: when using zpt files, this step, as well as the assembly of the ReportFile object is not necessary;
    # instead, it could be loaded the following way:
    #
    # report = ReportFileLoader.load(zpt_file_path)
    #
    report_path = Path("../../reports/newsletter").absolute()
    status, zfs = ReportFileBuilder.build_zipfs(report_path)
    if not status.success():
        print("Error loading the report")
        exit(1)

    # assemble ReportFile object from the in-memory zfs
    report = ReportFileLoader.load_zipfs(zfs)

    # template variables
    report_data = {
        'name': "John Connor",
    }

    # render using zipreport-cli processor
    result = MIMEReport().render_defaults(report, report_data)
    if not result.success:
        print("An error occured while generating the email:", result.error)
        exit(1)

    # save io.BytesIO buffer to file
    # result.report is of type EmailMessage()
    with open(email_name, 'wb') as f:
        f.write(result.report.as_bytes(policy=SMTP))

    print(f"Email generated to {email_name}")
