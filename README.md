# Alertmanager Pumble Agent

A lightweight proxy service that forwards Prometheus Alertmanager notifications to Pumble chat via webhooks.

## Overview

This service acts as a bridge between Prometheus Alertmanager and Pumble Chat. Since Prometheus Alertmanager doesn't natively support Pumble webhooks, this agent receives alerts from Alertmanager and forwards them to Pumble in a nicely formatted way.

## Features

- Converts JSON alert data to YAML format for better readability
- Adds status headers to messages for quick understanding of alert severity
- Configurable via environment variables
- Supports debug mode for troubleshooting
- Kubernetes and Docker deployment ready
- Lightweight Python-based implementation

## Requirements

- Python 3.9+
- Flask
- Requests
- PyYAML
- Gunicorn (for production deployment)

## Configuration

The service is configured via environment variables:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `PUMBLE_WEBHOOK_URL` | Your Pumble webhook URL | Yes | - |
| `DEBUG` | Enable debug logging | No | `false` |

## Deployment Options

### Docker

Build and run using Docker:

```bash
docker build -t pumble-alertmanager .
docker run -p 9094:9094 -e PUMBLE_WEBHOOK_URL=https://api.pumble.com/your-webhook-path -e DEBUG=false pumble-alertmanager
```

Or use the provided Docker Compose file:

```bash
# Edit docker-compose.yaml to add your webhook URL
docker-compose up -d
```

### Kubernetes

Apply the provided Kubernetes manifest:

```bash
# Edit k8s-pumble-proxy.yaml to add your webhook URL
kubectl apply -f k8s-pumble-proxy.yaml
```

## Local Development

```bash
# Install dependencies
pip install -r src/requirements.txt

# Set environment variables
export PUMBLE_WEBHOOK_URL=https://api.pumble.com/your-webhook-path
export DEBUG=true

# Run the application
python src/app.py
```

## Alert Format

Alerts are formatted in Pumble as:

```
🚨 *ALERT [STATUS]*: [Alert Name]

```yaml
[Full alert details in YAML format]
```

## Testing

You can test the webhook endpoint using curl:

```bash
curl -X POST http://localhost:9094/ \
  -H "Content-Type: application/json" \
  -d '{"status":"firing","groupLabels":{"alertname":"Test Alert"},"alerts":[{"status":"firing","labels":{"severity":"critical"}}]}'
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.