from zipreport.report import ReportJob, JobResult


class ProcessorInterface:

    def process(self, job: ReportJob) -> JobResult:
        pass