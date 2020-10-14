import json
from io import StringIO
from pathlib import Path
from zipfile import BadZipFile

from zipreport.fileutils import ZipFs, FsError
from zipreport.fileutils.backend.zip import InMemoryZip, InMemoryZipError
from zipreport.report.builder import ReportFileBuilder
from zipreport.report.const import MANIFEST_FILE_NAME
from zipreport.report.reportfile import ReportFile


class ReportFileLoaderError(Exception):
    pass


class ReportFileLoader:

    @staticmethod
    def load(source: str) -> ReportFile:
        """
        Load ReportFile from a source (either directory or a ZPT)
        :param source:
        :return: ReportFile
        """
        source = Path(source)
        if source.is_dir():
            return ReportFileLoader.load_dir(source)
        return ReportFileLoader.load_file(source)

    @staticmethod
    def load_dir(path: str) -> ReportFile:
        """
        Generate ReportFile from a directory with a valid report template
        :param path: template path
        :return: ReportFile
        """
        zstatus, zfs = ReportFileBuilder.build_zipfs(path, StringIO())
        if not zstatus.success():
            error_msg = "; ".join(zstatus.get_errors())
            raise ReportFileLoaderError("Error loading report from path '{}': '{}'".format(path, error_msg))
        try:
            manifest = json.loads(bytes(zfs.get(MANIFEST_FILE_NAME).getbuffer()))
        except Exception as e:
            raise ReportFileLoaderError("Error: {}".format(e))
        return ReportFile(zfs, manifest)

    @staticmethod
    def load_file(file: str) -> ReportFile:
        """
        Load ReportFile from a zpt file
        :param file: zpt file path
        :return: ReportFile
        """
        file = Path(file)
        if not file.exists() or not file.is_file():
            raise ReportFileLoaderError("Cannot find file '{}".format(file))

        try:
            zfs = ZipFs(InMemoryZip(file))
        except (FsError, InMemoryZipError, BadZipFile, ValueError) as e:
            raise ReportFileLoaderError("Error: {}".format(e))

        # load manifest & assemble report
        return ReportFileLoader.load_zipfs(zfs)

    @staticmethod
    def load_zipfs(zfs: ZipFs) -> ReportFile:
        """
        Generates a ReportFile from a ZipFs
        :param zfs: ZipFs
        :return: ReportFile
        """
        # load manifest
        status, manifest = ReportFileBuilder.valid_zpt(zfs)
        if not status.success():
            raise ReportFileLoaderError("Error: {}".format("; ".join(status.get_errors())))

        return ReportFile(zfs, manifest)
