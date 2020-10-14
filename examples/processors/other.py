from zipreport import ZipReportCli
from zipreport.processors.zipreport import ZipReportClient, ZipReportProcessor
from zipreport.report import ReportFileLoader, ReportJob
from zipreport.template import JinjaRender

def generate_pdf_server(report:str, data: dict, output_file:str) -> bool:

    zpt = ReportFileLoader.load(report) # load zpt file
    JinjaRender(zpt).render(data)   # render jinja template with parameters

    job = ReportJob(zpt)        # create new rendering job
    job.set_jsevent(True)       # report uses event hook
    job.set_jsevent_timeout(500)
    job.set_process_timeout(600)
    job.set_render_timeout(600)

    client = ZipReportClient('http://127.0.0.1:6543', "")   # zipreport-server client
    result = ZipReportProcessor(client).process(job)    # render

    if result.success:
        with open(output_file, 'wb') as rpt:
            rpt.write(result.report.read())
        return True
    return False


def generate_pdf_cli(zipreport_cli:str, report: str, data: dict, output_file: str) -> bool:

    zpt = ReportFileLoader.load(report)  # load zpt file
    JinjaRender(zpt).render(data)  # render jinja template with parameters

    job = ReportJob(zpt)  # create new rendering job
    job.set_jsevent(True)  # report uses event hook
    job.set_jsevent_timeout(500)
    job.set_process_timeout(600)
    job.set_render_timeout(600)

    result = ZipReportCli(zipreport_cli).render(job, data)

    if result.success:
        with open(output_file, 'wb') as rpt:
            rpt.write(result.report.read())
        return True
    return False
