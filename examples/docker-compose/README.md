# Docker Compose Example

Demonstrates running a Python application alongside zipreport-server using Docker Compose.

## Running

```bash
docker compose up --build
```

The generated PDF will be written to `./output/report.pdf`.

## Configuration

### Server Configuration

The zipreport-server (v2.3.0+) uses a JSON configuration file. Edit `config/config.json` to change the API key:

```json
{
  "apiServer": {
    "options": {
      "authTokenSecret": "somePassword"
    }
  }
}
```

### App Environment Variables

| Variable         | Description                            | Default                        |
|------------------|----------------------------------------|--------------------------------|
| `ZIPREPORT_URL`  | Server URL (used by the app container) | `http://zipreport-server:6543` |
| `ZIPREPORT_KEY`  | API key (must match config.json)       | `somePassword`                 |

## Customizing the Report Template

The `app` service mounts `../reports` as `/reports` inside the container. The default script loads the template from
`/reports/simple`. To use a different template:

1. Place your report directory under `../reports/`
2. Update the `REPORT_PATH` in `app/main.py` to point to your template
3. Update `report_data` with the parameters expected by your template's `manifest.json`
