import io
import subprocess
import tempfile
from pathlib import Path
from shutil import rmtree

from zipreport.processors import ProcessorInterface
import zipreport.report.const as const
from zipreport.report.job import ReportJob, JobResult


class WkHtml2PdfProcessor(ProcessorInterface):
    """
    wkhtmltopdf report processor
    """
    MARGIN_MINIMUM_MM = '5'

    def __init__(self, cli_path: str):
        """
        Constructor
        :param cli_path: full path to wkhtmltopdf binary
        """
        self._cli = cli_path

    def process(self, job: ReportJob) -> JobResult:
        """
        Execute a ReportJob by calling the wkhtmltopdf binary
        :param job: ReportJob
        :return: JobResult
        """
        report = None
        success = False
        error = ""
        path = None
        try:
            path = Path(tempfile.mkdtemp())
            cmd = self.build_cmd(job, path)
            job.get_report().get_fs().get_backend().zip().extractall(path)

            subprocess.run(cmd, cwd=path, check=True)
            report_file = path / const.PDF_FILE_NAME
            if report_file.exists():
                with open(report_file, 'rb') as f:
                    report = io.BytesIO(f.read())
                    success = True

        except (subprocess.CalledProcessError, FileNotFoundError, PermissionError, FileExistsError) as e:
            error = str(e)

        if path:
            rmtree(path)

        return JobResult(report, success, error)

    def build_cmd(self, job: ReportJob, path: Path, dest_file: str = const.PDF_FILE_NAME):
        """
        Parse ReportJob options and generate command-line arguments for wkhtmltopdf
        :param job: ReportJob
        :param path: full path for the report root
        :param dest_file: full path for PDF file to be generated
        :return: list
        """
        opts = job.get_options()
        args = [
            str(Path(self._cli)),
            '--enable-local-file-access',
            '--allow', str(path),
            '--no-stop-slow-scripts',
            '--page-size', opts[ReportJob.OPT_PAGE_SIZE],
            '--javascript-delay', str(opts[ReportJob.OPT_SETTLING_TIME]),
        ]

        # non-default margins
        if opts[ReportJob.OPT_MARGINS] == const.PDF_MARGIN_NONE:
            args.extend([
                '--margin-bottom', "0",
                '--margin-left', "0",
                '--margin-right', "0",
                '--margin-top', "0"
            ])

        if opts[ReportJob.OPT_MARGINS] == const.PDF_MARGIN_MINIMUM:
            args.extend([
                '--margin-bottom', self.MARGIN_MINIMUM_MM,
                '--margin-left', self.MARGIN_MINIMUM_MM,
                '--margin-right', self.MARGIN_MINIMUM_MM,
                '--margin-top', self.MARGIN_MINIMUM_MM,
            ])

        # page orientation
        if opts[ReportJob.OPT_LANDSCAPE]:
            args.append('--orientation')
            args.append('Landscape')

        args.extend([opts[ReportJob.OPT_MAIN_SCRIPT], dest_file])
        return args
