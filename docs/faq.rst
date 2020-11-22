.. _faq:

FAQ
===

Why another PDF generation library?
___________________________________

While there are many excellent free and open source libraries for report generation, Python seems to be a second-class citizen - existing libraries are either old/unmaintained or quite slow while supporting only a subset of features. ZipReport aims to be a faster alternative, while supporting modern HTML/CSS and JavaScript.

What are the typical usage scenarios?
_____________________________________

* Custom reports, mixing static and generated data;
* Dashboarding reports with dynamic composition via JavaScript;
* Transactional emails that require embedding of images (ex daily server reports with graphics);


Does it run on Windows or Mac OS X?
___________________________________

ZipReport was only tested on Linux systems.

What HTML/CSS/JS features are supported?
________________________________________

When using ZipReport backends, the rendering is executed by Chromium (as an Electron application), all features supported by a modern Chromium browsers can be used.
When using WeasyPrint, basic WeasyPrint features ate supported.

Is it fast?
___________

No. Expect PDF rendering time to be measured in seconds. Complex reports may take longer.

Is it thread-safe?
__________________

No. While zipreport can be used safely to render reports inside threads, the report processing subsystem is not thread safe. We recommend not to share ZipReport objects or state between threads.



Does it work with alternative Python implementations besides cPython?
_____________________________________________________________________

Not sure, maybe. It was only tested with cPython.