import zipreport.report.job as j
from zipreport.report.const import *


class TestReportJob:
    def test_init(self):
        # fake job
        job = j.ReportJob(None)
        opts = job.get_options()
        assert type(opts) is dict
        assert len(opts) == len(j.ReportJob.DEFAULT_OPTIONS)

        # test valid settings
        for ps in VALID_PAGE_SIZES:
            assert job.set_page_size(ps) is True

        for ms in VALID_MARGINS:
            assert job.set_margins(ms) is True

        # test invalid settings
        assert job.set_page_size("A2") is False
        assert job.set_margins("something") is False
        assert job.set_settling_time(-3) is False
        assert job.set_js_timeout(-10) is False
        assert job.set_job_timeout(-20) is False

    def test_custom_options(self):
        job = j.ReportJob(None)

        # custom job parameters
        main_script = "dummy.html"
        job.set_page_size(PDF_PAGE_A3)
        job.set_margins(PDF_MARGIN_NONE)
        job.set_landscape(True)
        job.set_main_script(main_script)
        job.set_settling_time(100)
        job.set_js_timeout(33)
        job.set_job_timeout(40)
        job.use_jsevent(True)
        job.set_ignore_ssl_errors(True)

        opts = job.get_options()
        assert job.get_report() is None
        assert opts[OPT_PAGE_SIZE] == PDF_PAGE_A3
        assert opts[OPT_MARGIN_STYLE] == PDF_MARGIN_NONE
        assert opts[OPT_LANDSCAPE] is True
        assert opts[OPT_MAIN_SCRIPT] == main_script
        assert opts[OPT_SETTLING_TIME] == 100
        assert opts[OPT_JS_TIMEOUT] == 33
        assert opts[OPT_JOB_TIMEOUT] == 40
        assert opts[OPT_JS_EVENT] is True
        assert opts[OPT_IGNORE_SSL_ERRORS] is True
