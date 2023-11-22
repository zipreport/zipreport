# FAQ

## Why another PDF generation library?

While there are many excellent free and open source libraries for report generation, Python seems to be a 
second-class citizen - existing libraries are either old/unmaintained or quite slow while supporting only a 
subset of features. ZipReport aims to be a faster alternative, while supporting modern HTML/CSS and JavaScript.

## What are the typical usage scenarios?

* Custom reports, mixing static and generated data;
* Dashboarding reports with dynamic composition via JavaScript;
* Transactional emails that require embedding of images (ex daily server reports with graphics);


## Does it run on Windows or Mac OS X?

ZipReport was only tested on Linux systems.


## What HTML/CSS/JS features are supported?

When using [zipreport-server](https://github.com/zipreport/zipreport-server), the rendering is executed by Chromium; all
features supported by a modern Chromium browsers can be used. When using WeasyPrint, basic WeasyPrint features ate supported.

## Is it fast?

Depends on the defintion of "fast". The complex report example may take 2-3 seconds to process. Huge documents may take longer.


## Is it thread-safe?

No. While zipreport can be used safely to render reports inside threads, 
the report processing subsystem is not thread safe. We recommend not to share ZipReport objects or state between threads.


## Does it work with alternative Python implementations besides cPython?

It was only tested with cPython. It may work, or it may not.
