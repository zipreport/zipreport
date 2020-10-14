import hashlib
from email.policy import SMTP

from tests.processors.base import BaseTest
from tests.utils import RPT_NEWSLETTER_PATH
from zipreport.processors.mime import ResourceParser, MIMEProcessor
from zipreport.report import ReportJob
from zipreport.template import JinjaRender


class TestMimeResourceParser(BaseTest):
    resource_parser_data = """
    <html>
    <head>
        <!-- CSS tests -->
        <link rel="stylesheet" type="text/css" HREF="style1.css">
        <link rel="stylesheet" type="text/css" href="/css/style2.css">
        <link rel="stylesheet" type="text/css" href="//style3.css">
        <link rel="stylesheet" type="text/css" href="https://css/style4.css">                
        <link rel="stylesheet" type="text/css" href="HTTP://css/style5.css">   
        <!-- JS tests -->        
        <script src="script1.js"></script>             
        <script src="/script/script2.js"></script>
        <script src="//script3.js"></script>        
        <script src="http://script4.js"></script>
        <script src="HTTPS://script5.js"></script>
    </head>
    <body>
     <!-- anchor ignore test -->
     <a href="file1.html">file1</a> 
     <a href="file2.html">file2</a>
     <a href="/file3.html">file3</a>
     
     <!-- IMG tests -->
      <img SRC='/some/image1.jpg' />
      <img src="//other/image2.jpg" />
      <img src="http://other/image3.jpg" />
      <img src="https://other/image4.jpg" />
      <img src="HTTP://other/image5.jpg" />
      <img src="HTTPS://other/image6.jpg" />       
      <img src="image7.png" />           
    </body>
    </html>
    """
    expected_src_list = [
        "script1.js",
        "/script/script2.js",
        "/some/image1.jpg",
        "image7.png",
    ]
    expected_href_list = [
        "style1.css",
        "/css/style2.css",
    ]

    expected_size = 154000  # ballpark value for embedded mime newsletter

    def test_resourceparser(self):
        parser = ResourceParser()
        parser.feed(self.resource_parser_data)

        src = parser.get_src_list()
        assert len(src) == len(self.expected_src_list)
        for item in src:
            assert item in self.expected_src_list

        href = parser.get_href_list()
        assert len(href) == len(self.expected_href_list)
        for item in href:
            assert item in self.expected_href_list

    def test_mime_processor(self):
        zpt = self.build_zpt(RPT_NEWSLETTER_PATH)
        render = JinjaRender(zpt)
        result = render.render()
        assert result is not None

        job = ReportJob(zpt)
        result = MIMEProcessor().process(job)
        assert result.success is True
        assert len(result.error) == 0
        assert result.report is not None

        payload = result.report.as_bytes(policy=SMTP)
        assert len(payload) >= self.expected_size
