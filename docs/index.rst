.. ZipReport documentation

Welcome to ZipReport documentation
==================================

Version: |version|


ZipReport is a python library to aid the generation of visually appealing PDF documents from HTML templates. It combines
Jinja2 template capabilities with PDF generation powered by a headless Chromium browser daemon. By leveraging
the browser rendering capabilities, it is possible to use CSS and JS for composition of the document, just as if it
was any other web page. Available polyfills such as https://pagedjs.org can be used to generate headers,
footers, page numbers, chapter numbers and even table of contents. It is also possible to generate graphics using popular
JS libraries, such as https://d3js.org, or even embed runtime-generated graphics generated via Python functions.

However, these capabilities come at a price; While ZipReport by itself is quite fast, PDF generation is slow. The more
complex the document is, the slower will be the rendering process.

Features
========

* Design reports in HTML using Jinja templates;
* Reports are packaged on a single file for easy reuse/distribution;
* Pluggable rendering backends;
* Full support for CSS3 and client-side Javascript (when using ZipReport-Server/ZipReport-cli);
* Page numbers, headers, footers, ToC, etc. via polyfills (using https://pagedjs.org);
* Jinja tags for dynamic image generation in Python;
* CLI utility to aid development and packaging of reports;
* MIME multipart email message generation (with all local resources embedded on a single message);

Documentation
=============

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   install
   how_it_works
   build_templates
   cli
   faq
   security

Report Samples
==============

The code for these samples resides in examples_ and the report template files in reports_. These examples
generate the following reports:

- :download:`simple report<samples/simple.pdf>`
- :download:`dynamic image generation example <samples/filter_example.pdf>`
- :download:`MIME newsletter example (.eml file, use 'save as...') <samples/newsletter.eml>`
- :download:`paged.js report with page numbers, ToC and front page <samples/pagedjs.pdf>`


Package documentation
=====================
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   source/zipreport.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _examples: https://github.com/zipreport/zipreport/tree/master/examples/code
.. _reports:  https://github.com/zipreport/zipreport/tree/master/examples/reports
