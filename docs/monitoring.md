# NetPulse Monitoring & Alerting Setup

This document describes the comprehensive monitoring and alerting system for NetPulse.

## Overview

NetPulse includes a complete monitoring stack with:

- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization dashboards
- **AlertManager**: Alert routing and notifications
- **Node Exporter**: System metrics
- **Flower**: Celery task monitoring

## Quick Start

### 1. Start the Full Monitoring Stack

```bash
# Build and start all services including monitoring
docker-compose -f docker-compose.prod.yml up --build -d

# Verify all services are running
docker-compose -f docker-compose.prod.yml ps
```

### 2. Access the Monitoring Interfaces

| Service | URL | Credentials |
|---------|-----|-------------|
| **Grafana** | http://localhost:3001 | admin/admin |
| **Prometheus** | http://localhost:9090 | - |
| **AlertManager** | http://localhost:9093 | - |
| **Flower** | http://localhost:5555 | - |
| **Node Exporter** | http://localhost:9100/metrics | - |

### 3. Configure Alerting (Optional)

Edit `monitoring/alertmanager.yml` to configure your notification channels:

```yaml
# For Slack notifications
slack_configs:
  - api_url: 'YOUR_SLACK_WEBHOOK_URL'
    channel: '#alerts'

# For email notifications
email_configs:
  - to: 'ops-team@yourcompany.com'
    from: 'netpulse-alerts@yourcompany.com'
    smarthost: 'smtp.yourcompany.com:587'
```

## Dashboards

### 1. NetPulse Overview Dashboard
- **URL**: http://localhost:3001/d/netpulse-noc/netpulse-network-operations-center
- **Description**: High-level view of network health, device status, and alerts
- **Key Metrics**:
  - Total/Online/Offline device counts
  - Device status distribution
  - Response time trends
  - Active alerts summary

### 2. Device Details Dashboard
- **URL**: http://localhost:3001/d/device-details/device-details-dashboard
- **Description**: Detailed view of individual device performance
- **Features**:
  - Device selection dropdown
  - Response time trends
  - Uptime statistics (24h, 7d, 30d)
  - Packet loss monitoring
  - Event timeline

## Metrics

### Device Metrics

| Metric | Description | Labels |
|--------|-------------|--------|
| `device_status` | Device online status (1=online, 0=offline) | device_name, ip_address, device_type, location |
| `device_response_time_ms` | Device response time in milliseconds | device_name, ip_address |
| `device_uptime_seconds` | Device uptime in seconds | device_name, ip_address |
| `device_packet_loss_percent` | Packet loss percentage | device_name, ip_address |
| `device_info` | Device metadata (always 1) | device_name, ip_address, device_type, location, status |

### Application Metrics

| Metric | Description | Labels |
|--------|-------------|--------|
| `device_status_changes_total` | Total device status changes | device_name, old_status, new_status |
| `monitoring_checks_total` | Total monitoring checks performed | device_name |
| `monitoring_errors_total` | Total monitoring errors | device_name, error_type |

## Alerts

### Critical Alerts

1. **DeviceOffline**: Device has been offline for more than 1 minute
2. **NetPulseBackendDown**: Backend service is down for more than 30 seconds
3. **HighMemoryUsage**: Memory usage above 90% for more than 5 minutes

### Warning Alerts

1. **DeviceHighResponseTime**: Response time above 5 seconds for more than 2 minutes
2. **HighDeviceOfflineRate**: More than 20% of devices going offline
3. **HighCPUUsage**: CPU usage above 80% for more than 5 minutes
4. **DiskSpaceLow**: Disk usage above 85% for more than 10 minutes

### Alert Routing

- **Critical alerts**: Sent to email and Slack immediately
- **Warning alerts**: Sent to email and Slack with grouping
- **Inhibition**: Critical alerts suppress related warning alerts

## Customization

### Adding Custom Metrics

1. **Backend**: Add metrics to `app/api/endpoints/metrics.py`
2. **Prometheus**: Metrics are automatically scraped from `/api/v1/metrics/metrics`
3. **Grafana**: Create new panels using PromQL queries

### Creating Custom Dashboards

1. Access Grafana at http://localhost:3001
2. Create new dashboard or import existing ones
3. Use Prometheus as data source
4. Save dashboards to `monitoring/grafana/dashboards/` for persistence

### Custom Alert Rules

Edit `monitoring/alert_rules.yml` to add new alerts:

```yaml
- alert: CustomAlert
  expr: your_metric > threshold
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Custom alert fired"
    description: "Your custom alert description"
```

## Troubleshooting

### Common Issues

1. **Grafana shows "No data"**
   - Check Prometheus is running: http://localhost:9090
   - Verify Prometheus can scrape backend: http://localhost:9090/targets
   - Check backend metrics endpoint: http://localhost:8000/api/v1/metrics/metrics

2. **Alerts not firing**
   - Check alert rules in Prometheus: http://localhost:9090/alerts
   - Verify AlertManager configuration: http://localhost:9093

3. **Missing device metrics**
   - Ensure devices are added through the NetPulse UI
   - Check monitoring service is running (Celery worker)
   - Verify database connectivity

### Logs

```bash
# View service logs
docker-compose -f docker-compose.prod.yml logs prometheus
docker-compose -f docker-compose.prod.yml logs grafana
docker-compose -f docker-compose.prod.yml logs alertmanager

# View NetPulse backend logs
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs worker
```

## Performance Tuning

### Prometheus Retention

Default retention is 200h (8+ days). Adjust in `docker-compose.prod.yml`:

```yaml
command:
  - '--storage.tsdb.retention.time=720h'  # 30 days
```

### Scrape Intervals

Adjust scraping frequency in `monitoring/prometheus.yml`:

```yaml
global:
  scrape_interval: 30s  # Increase for less load
```

### Grafana Performance

- Use appropriate time ranges
- Limit number of series in queries
- Use recording rules for complex queries

## Security Considerations

1. **Change default passwords** in production
2. **Configure HTTPS** for external access
3. **Restrict network access** to monitoring ports
4. **Use authentication** for Prometheus and AlertManager in production
5. **Secure webhook URLs** and API keys

## Backup and Recovery

### Important Files to Backup

- `monitoring/` directory (configurations)
- Grafana dashboards and data sources
- Prometheus data (if historical data is important)
- AlertManager configuration and silences

### Recovery Process

1. Restore configuration files
2. Restart monitoring stack
3. Re-import Grafana dashboards if needed
4. Verify all alerts are working

## Integration Examples

### Slack Integration

```yaml
# In alertmanager.yml
slack_configs:
  - api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
    channel: '#netpulse-alerts'
    title: 'NetPulse Alert'
    text: |
      {{ range .Alerts }}
      *{{ .Annotations.summary }}*
      {{ .Annotations.description }}
      {{ end }}
```

### Email Integration

```yaml
# In alertmanager.yml
email_configs:
  - to: 'network-team@company.com'
    from: 'netpulse@company.com'
    smarthost: 'smtp.company.com:587'
    auth_username: 'netpulse@company.com'
    auth_password: 'your-password'
    subject: 'NetPulse Alert: {{ .GroupLabels.alertname }}'
```

### Webhook Integration

```yaml
# In alertmanager.yml
webhook_configs:
  - url: 'https://your-webhook-endpoint.com/alerts'
    send_resolved: true
```

For more information, see the official documentation:
- [Prometheus](https://prometheus.io/docs/)
- [Grafana](https://grafana.com/docs/)
- [AlertManager](https://prometheus.io/docs/alerting/latest/alertmanager/)
