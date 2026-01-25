# Installation

## Required dependencies

* jinja2 >= 3.1
* requests >= 2.22.0
* markupsafe >= 2.0
* WeasyPrint >= 68.0 (optional, see below)

## **Step 1:** install ZipReport library

To install ZipReport library, use pip:

```shell
$ python3 -m pip install zipreport-lib
```

Or if [WeasyPrint](https://weasyprint.org/) backend is required, install:

```shell
$ python3 -m pip install zipreport-lib[weasyprint]
```

## **Step 2:** choose and install a rendering backend

### Available backends:

* [ZipReport-Server](https://github.com/zipreport/zipreport-server/), an API-based PDF rendering server (recommended)
* [WeasyPrint](https://weasyprint.org/), experimental, available for compatibility purposes only
* MIME, an internal MIME Processor that has no external dependencies

### Using zipreport-server

ZipReport communicates with zipreport-server via REST API, using multipart/form-data format. Check the
[zipreport-server repository](https://github.com/zipreport/zipreport-server) for additional details and setup configuration.

On AMD64 systems, an existing prebuilt Docker image can be used. Don't forget to change your API key, used for
authentication.

```shell
$ docker run -d -p 6543:6543 -e ZIPREPORT_API_KEY="my-api-key" \
    ghcr.io/zipreport/zipreport-server:2.3.1
```


## Installing from source

Clone the ZipReport repository:
```shell
$ git clone https://github.com/zipreport/zipreport.git
```

Install the package:
```shell
$ pip install .
```
