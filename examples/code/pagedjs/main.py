# ZipReport PagedJS Example
import io
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from zipreport import ZipReport
from zipreport.report import ReportFileBuilder, ReportFileLoader, ReportJob, ReportFile

# required to support 3d plotting
from mpl_toolkits.mplot3d import Axes3D

class PagedJSReport:

    def render(self, zpt: ReportFile, output='report.pdf') -> bool:
        """
        Render a report
        :param zpt: ReportFile to use
        :param output: output file
        :return: True if operation was successful
        """
        data = {
            'date': datetime.today().strftime('%Y-%m-%d'),
            'author': 'ZipReport library',

            # data for first graphic
            'graphics_1': {
                'x-axis': 'time',
                'g1-y-axis': 's1 and s2',
                'g2-y-axies': 'coherence',
            },

            # data for second graphic
            'graphics_2': {
                'title': '3D surface',
            },

            # encapsulate class methods into a lambda for callback
            'gen_graphics_1': lambda args: self.plot_graphics_1(args),
            'gen_graphics_2': lambda args: self.plot_graphics_2(args),
        }

        # create job
        job = ReportJob(zpt)
        job.use_jsevent(True)

        # generate PDF
        result = ZipReport("https://127.0.0.1:6543", "somePassword").render(job, data)

        # save and return
        if result.success:
            with open(output, 'wb') as rpt:
                rpt.write(result.report.read())
            return True
        return False

    def plot_graphics_1(self, data):
        """
        Callback function for graphics generation
        MatPlotLib example "Plotting the coherence of two singals"
        From https://matplotlib.org/gallery/lines_bars_and_markers/cohere.html#sphx-glr-gallery-lines-bars-and-markers-cohere-py

        :param data:
        :return:
        """
        # Fixing random state for reproducibility
        np.random.seed(19680801)

        dt = 0.01
        t = np.arange(0, 30, dt)
        nse1 = np.random.randn(len(t))  # white noise 1
        nse2 = np.random.randn(len(t))  # white noise 2

        # Two signals with a coherent part at 10Hz and a random part
        s1 = np.sin(2 * np.pi * 10 * t) + nse1
        s2 = np.sin(2 * np.pi * 10 * t) + nse2

        fig, axs = plt.subplots(2, 1)
        axs[0].plot(t, s1, t, s2)
        axs[0].set_xlim(0, 2)
        axs[0].set_xlabel(data['x-axis'])
        axs[0].set_ylabel(data['g1-y-axis'])
        axs[0].grid(True)

        cxy, f = axs[1].cohere(s1, s2, 256, 1. / dt)
        axs[1].set_ylabel(data['g1-y-axis'])

        fig.tight_layout()

        # save generated image to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf.read()

    def plot_graphics_2(self, data):
        """
        Callback function for graphics generation
        MatPlotLib 3d surface example
        From: https://matplotlib.org/gallery/mplot3d/surface3d.html#sphx-glr-gallery-mplot3d-surface3d-py

        :param data:
        :return:
        """
        plt.title(data['title'])
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        # Make data.
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X ** 2 + Y ** 2)
        Z = np.sin(R)

        # Plot the surface.
        surf = ax.plot_surface(X, Y, Z, cmap=cm.get_cmap('coolwarm'),
                               linewidth=0, antialiased=False)

        # Customize the z axis.
        ax.set_zlim(-1.01, 1.01)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5)
        fig.set_dpi(100)
        plt.tight_layout()

        # save generated image to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf.read()


if __name__ == "__main__":

    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: python3 main.py <destination_file.pdf>")
        exit(1)
    pdf_name = Path(args[0])  # output file path

    if pdf_name.exists():
        print("{} already exists".format(pdf_name))
        exit(1)

    # Assemble report directly from the report folder, without using zpt file
    # ReportFileBuilder.build_zipfs() will create an in-memory zpt file suitable to be used by the library
    # Not: when using zpt files, this step, as well as the assembly of the ReportFile object is not necessary;
    # instead, it could be loaded the following way:
    #
    # report = ReportFileLoader.load(zpt_file_path)
    #
    report_path = Path("../../pagedjs/example_report").absolute()
    status, zfs = ReportFileBuilder.build_zipfs(report_path)
    if not status.success():
        print("Error loading the report")
        exit(1)

    # assemble ReportFile object from the in-memory zfs
    report = ReportFileLoader.load_zipfs(zfs)

    # use a custom class to render the report
    my_report = PagedJSReport()
    if my_report.render(report, pdf_name):
        print("Report generated to {}".format(pdf_name))
    else:
        print("Error generating the report")
