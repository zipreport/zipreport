import json
import os
import sys
from pathlib import Path
from typing import Tuple, Union

from zipreport.fileutils import ZipFs, FsInterface, DiskFs
from zipreport.fileutils.backend.zip import InMemoryZip
from zipreport.report.const import (
    MANIFEST_FILE_NAME,
    ZIPREPORT_FILE_EXTENSION,
    INDEX_FILE_NAME,
    MANIFEST_REQUIRED_FIELDS,
)


class BuildResult:
    def __init__(self, error=None):
        self._err = []
        self.add_error(error)

    def add_error(self, error):
        if type(error) is list:
            self._err.extend(error)
        elif error is not None:
            self._err.append(error)
        return self

    def get_errors(self) -> list:
        return self._err

    def success(self) -> bool:
        return len(self._err) == 0


class ReportFileBuilder:
    """
    Report building object
    """

    @staticmethod
    def build_file(
        path: str, output_file: str, console=sys.stdout, overwrite: bool = False
    ) -> BuildResult:
        """
        Assemble a report file from a specific path
        :param path: report dir path
        :param output_file: destination report file
        :param console: console writer
        :param overwrite: if True, overwrite destination if exists
        :return: BuildResult
        """
        status = BuildResult()
        path = Path(path)
        output_file = Path(output_file)
        if output_file.suffix != ZIPREPORT_FILE_EXTENSION:
            output_file = output_file.parent / (
                output_file.name + ZIPREPORT_FILE_EXTENSION
            )

        console.write(f"\n== Building Report {output_file} ==\n")

        # check paths
        if not path.exists():
            return status.add_error(f"Path '{path}' not found")

        if not path.is_dir():
            return status.add_error(f"Path '{path}' is not a directory")

        if output_file.exists():
            if not output_file.is_file():
                return status.add_error(
                    f"Output file '{output_file}' already exists and doesn't seem to be a file"
                )
            if not overwrite:
                return status.add_error(f"Output file '{output_file}' already exists")
        elif not output_file.parent.exists():
            return status.add_error(f"Invalid path for output file: '{output_file}'")

        # build ZipFs
        zfs_status, zfs = ReportFileBuilder.build_zipfs(path, console)
        if not zfs_status.success():
            return zfs_status

        try:
            # save zpt
            console.write(f"Generating {output_file}...\n")
            if output_file.exists():
                console.write("Report file exists, overwriting...\n")
                output_file.unlink()
            zfs.get_backend().save(output_file)

        except Exception as e:
            return status.add_error(f"Error saving zpt file: {e}")

        console.write("Done!\n")
        return status

    @staticmethod
    def build_zipfs(
        path: str, console=sys.stdout
    ) -> Tuple[BuildResult, Union[ZipFs, None]]:
        """
        Assemble a ZipFs structure from a specific path
        :param path: report dir path
        :param console: console writer
        :return: [BuildResult, ZipFs]
        """
        status = BuildResult()
        path = Path(path)

        if not path.exists():
            return status.add_error(f"Path '{path}' not found"), None

        if not path.is_dir():
            return status.add_error(f"Path '{path}' is not a directory"), None

        # try to load & validate manifest
        console.write("Checking manifest & index file...\n")

        # valid_zpt() works only on FsInterface
        dfs = DiskFs(path)
        fstatus, _ = ReportFileBuilder.valid_zpt(dfs)
        if not fstatus.success():
            return fstatus, None

        # build ZPT and copy files
        console.write("Building...\n")
        zfs = ZipFs(InMemoryZip())
        names = []
        for dirname, dirs, files in os.walk(path):
            dirname = Path(dirname)
            names.extend(dirname / Path(f) for f in files)
        for name in names:
            dest_name = name.relative_to(path)
            console.write(f"Copying {dest_name}...\n")
            try:
                with open(name, "rb") as f:
                    zfs.add(dest_name, f.read())
            except Exception as e:
                return status.add_error(f"Error copying file {name}: {e}"), None
        return status, zfs

    @staticmethod
    def valid_zpt(fs: FsInterface) -> Tuple[BuildResult, Union[dict, None]]:
        """
        Validates if a FsInterface is a valid report
        :param fs: FsInterface
        :return: (BuildResult, manifest_contents)
        """
        status = BuildResult()
        # check manifest
        try:
            manifest = json.loads(bytes(fs.get(MANIFEST_FILE_NAME).getbuffer()))
        except Exception as e:
            return status.add_error(f"Error processing manifest: {e}"), None

        if type(manifest) is not dict:
            return status.add_error("Invalid manifest format"), None
        for field, _type in MANIFEST_REQUIRED_FIELDS.items():
            if field not in manifest.keys():
                status.add_error(f"Missing mandatory field '{field}' in manifest file")
            elif type(manifest[field]) != _type:
                status.add_error(f"Invalid type in manifest field '{field}'")

        if not status.success():
            return status, None

        # check index.html
        try:
            fs.get(INDEX_FILE_NAME)
        except Exception as e:
            return status.add_error(f"Index file '{INDEX_FILE_NAME}' not found"), None

        return status, manifest
