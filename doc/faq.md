# FAQ

### Why another PDF generation library?

While there are many excellent free and open source libraries for report generation, Python seems to be a second-class citizen - existing libraries are either old/unmaintained or quite slow while supporting only a subset of features. ZipReport aims to be a faster alternative, while supporting modern HTML/CSS and JavaScript.



### What are the typical usage scenarios?

- Custom reports, mixing static and generated data;
- Dashboarding reports with dynamic composition via JavaScript;
- Transactional emails that require embedding of images (ex daily server reports with graphics);



### Does it run on Windows or Mac OS X?

ZipReport was only tested on Linux systems.



### What HTML/CSS/JS features are supported?

Due to the fact that the rendering is executed by Chromium (as an Electron application), all features supported by a modern Chromium browsers can be used.



### Is it fast?

No. Expect PDF rendering time to be measured in seconds. Complex reports may take longer.



### Is it thread-safe?

No. While zipreport can be used safely to render reports inside threads, the report processing subsystem is not thread safe. We recommend not to share ZipReport objects or state between threads.



### Does it work with alternative Python implementations besides cPython?

Not sure, maybe. It was only tested with cPython.