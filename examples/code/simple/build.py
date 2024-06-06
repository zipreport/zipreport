# Builds a ZipReport zpt file on the current directory from the 'simple' report, programmatically
# Reports can be built via command-line using the "zipreport build" command
#
from pathlib import Path

from zipreport.report import ReportFileBuilder

if __name__ == "__main__":
    report_path = Path("../../reports/simple").absolute()
    report = Path("simple.zpt")

    if report.exists():
        print("Destination file {} already exists, skipping...".format(report))
        exit(1)

    result = ReportFileBuilder.build_file(report_path, report)
    if not result.success():
        print("Error:", ";".join(result.get_errors()))
        exit(1)
    print("Generated ZipReport file {} from template in {}".format(report, report_path))
