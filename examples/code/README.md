# ZipReport examples

Most examples require a zipreport-server instance running locally. A Docker-based instance can be run with the following commands:

```shell
$ docker run -d -p 6543:6543 ghcr.io/zipreport/zipreport-server:latest -e ZIPREPORT_API_KEY="somePassword"
```