from abc import ABC, abstractmethod

from zipreport.report import ReportJob, JobResult


class ProcessorInterface(ABC):
    @abstractmethod
    def process(self, job: ReportJob) -> JobResult:
        pass
