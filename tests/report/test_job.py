import zipreport.report.job as j
import zipreport.report.const as const


class TestReportJob:

    def test_init(self):
        # fake job
        job = j.ReportJob(None)
        opts = job.get_options()
        assert type(opts) is dict
        assert len(opts) == len(j.ReportJob.DEFAULT_OPTIONS)

        # test valid settings
        for ps in const.VALID_PAGE_SIZES:
            assert job.set_page_size(ps) is True

        for ms in const.VALID_MARGINS:
            assert job.set_margins(ms) is True

        # test invalid settings
        assert job.set_page_size("A2") is False
        assert job.set_margins("something") is False
        assert job.set_settling_time(-3) is False
        assert job.set_render_timeout(-5) is False
        assert job.set_jsevent_timeout(-10) is False
        assert job.set_process_timeout(-20) is False

    def test_custom_options(self):
        job = j.ReportJob(None)

        # custom job parameters
        main_script = "dummy.html"
        job.set_page_size(const.PDF_PAGE_A3)
        job.set_margins(const.PDF_MARGIN_NONE)
        job.set_landscape(True)
        job.set_main_script(main_script)
        job.set_settling_time(100)
        job.set_render_timeout(32)
        job.set_jsevent_timeout(33)
        job.set_process_timeout(40)
        job.set_jsevent(True)
        job.set_no_insecure_content(True)
        job.set_ignore_ssl_errors(True)

        opts = job.get_options()
        assert job.get_report() is None
        assert opts[j.ReportJob.OPT_PAGE_SIZE] == const.PDF_PAGE_A3
        assert opts[j.ReportJob.OPT_MARGINS] == const.PDF_MARGIN_NONE
        assert opts[j.ReportJob.OPT_LANDSCAPE] is True
        assert opts[j.ReportJob.OPT_MAIN_SCRIPT] == main_script
        assert opts[j.ReportJob.OPT_SETTLING_TIME] == 100
        assert opts[j.ReportJob.OPT_RENDER_TIMEOUT] == 32
        assert opts[j.ReportJob.OPT_JS_TIMEOUT] == 33
        assert opts[j.ReportJob.OPT_PROCESS_TIMEOUT] == 40
        assert opts[j.ReportJob.OPT_JS_EVENT] is True
        assert opts[j.ReportJob.OPT_NO_INSECURE_CONTENT] is True
        assert opts[j.ReportJob.OPT_IGNORE_SSL_ERRORS] is True
