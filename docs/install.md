# Installation

## Required dependencies

* jinja2_ >= 3.1
* requests_ >= 2.22.0
* WeasyPrint_ >= 58.0 (optional, see below)

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
autentication.

```shell
 $ docker run -d -p 6543:6543 ghcr.io/zipreport/zipreport-server:latest \
    -e ZIPREPORT_API_KEY="my-api-mey" 
```


## Installing from source

Clone the ZipReport repository:
```shell
$ git clone https://github.com/zipreport/zipreport.git
```

Install the package:
```shell
$ python3 setup.py install
```
