# NetPulse API Documentation

Welcome to the NetPulse API documentation. This document provides a comprehensive overview of the microservices architecture and available endpoints.

## Microservices Architecture

NetPulse follows a microservices architecture with the following services:

| Service | Port | Base URL | Responsibility |
|---------|------|----------|----------------|
| **API Gateway** | 8000 | `http://localhost:8000` | Request routing & authentication |
| **Auth Service** | 8001 | `http://localhost:8001` | User authentication & authorization |
| **Device Service** | 8002 | `http://localhost:8002` | Device management |
| **Monitoring Service** | 8003 | `http://localhost:8003` | Real-time monitoring & metrics |
| **Alert Service** | 8004 | `http://localhost:8004` | Alert processing & management |
| **Notification Service** | 8005 | `http://localhost:8005` | Multi-channel notifications |
| **Reporting Service** | 8006 | `http://localhost:8006` | Analytics & reporting |

## API Gateway

All client requests should go through the API Gateway at `http://localhost:8000`. The gateway handles:
- Request routing to appropriate microservices
- JWT token validation
- Rate limiting and CORS
- Request/response transformation

### Base URL
`http://localhost:8000`

## Authentication

The NetPulse API uses JWT-based authentication. Include the token in the Authorization header:

`Authorization: Bearer <YOUR_ACCESS_TOKEN>`

### Authentication Endpoints

#### **POST /auth/register**
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "John Doe",
  "organization_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

#### **POST /auth/token**
Authenticate and receive access token.

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### **GET /auth/verify-token**
Verify JWT token validity.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "organization_id": "123e4567-e89b-12d3-a456-426614174000",
  "is_active": true
}
```

## Device Management

### **GET /devices**
Retrieve all devices for the authenticated user's organization.

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum records to return (default: 100)

**Response:**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Router-01",
    "ip_address": "192.168.1.1",
    "device_type": "router",
    "location": "Data Center A",
    "status": "online",
    "last_seen": "2025-07-15T10:30:00Z",
    "created_at": "2025-07-01T09:00:00Z",
    "updated_at": "2025-07-15T10:30:00Z"
  }
]
```

### **POST /devices**
Add a new device to monitoring.

**Request Body:**
```json
{
  "name": "Switch-01",
  "ip_address": "192.168.1.2",
  "device_type": "switch",
  "location": "Data Center A"
}
```

### **GET /devices/{device_id}**
Get details for a specific device.

### **PUT /devices/{device_id}**
Update device information.

### **DELETE /devices/{device_id}**
Remove device from monitoring.

## Monitoring & Metrics

### **GET /metrics/{device_id}**
Get latest metrics for a specific device.

**Query Parameters:**
- `metric_type` (str): Filter by metric type (cpu, memory, network, ping)
- `hours` (int): Hours of historical data (default: 24)

**Response:**
```json
[
  {
    "device_id": "123e4567-e89b-12d3-a456-426614174000",
    "metric_type": "cpu",
    "value": 75.5,
    "unit": "%",
    "time": "2025-07-15T10:30:00Z"
  }
]
```

### **POST /metrics**
Submit new metrics (typically used by monitoring agents).

### **GET /devices/{device_id}/status**
Check real-time device status and perform ping test.

### **WebSocket /ws**
Real-time monitoring updates via WebSocket connection.

**Message Format:**
```json
{
  "type": "device_status_change",
  "data": {
    "device_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "offline",
    "timestamp": "2025-07-15T10:30:00Z"
  }
}
```

## Alert Management

### **GET /alerts**
Get alerts for the user's organization.

**Query Parameters:**
- `skip` (int): Number of records to skip
- `limit` (int): Maximum records to return

**Response:**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "device_id": "123e4567-e89b-12d3-a456-426614174000",
    "alert_type": "high_cpu",
    "severity": "warning",
    "message": "CPU usage is high: 85%",
    "acknowledged": false,
    "resolved": false,
    "created_at": "2025-07-15T10:30:00Z"
  }
]
```

### **POST /alerts**
Create a new alert.

### **PUT /alerts/{alert_id}/acknowledge**
Acknowledge an alert.

### **PUT /alerts/{alert_id}/resolve**
Mark alert as resolved.

## Notifications

### **POST /notifications/send**
Send notification via multiple channels.

**Request Body:**
```json
{
  "type": "email",
  "recipients": ["admin@example.com"],
  "subject": "Network Alert",
  "message": "Device Router-01 is offline",
  "data": {
    "device_id": "123e4567-e89b-12d3-a456-426614174000",
    "severity": "critical"
  }
}
```

### **POST /notifications/send-email**
Send email notification.

### **POST /notifications/send-sms**
Send SMS notification.

## Reporting

### **GET /reports/uptime-report/{organization_id}**
Generate device uptime report.

**Query Parameters:**
- `days` (int): Number of days to include (default: 30)

### **GET /reports/alert-summary/{organization_id}**
Generate alert summary report.

### **GET /reports/overview/{organization_id}**
Get organization overview with key metrics.

**Response:**
```json
{
  "organization_id": "123e4567-e89b-12d3-a456-426614174000",
  "device_stats": {
    "total_devices": 25,
    "online_devices": 23,
    "offline_devices": 2,
    "uptime_percentage": 92.0
  },
  "alert_stats": {
    "recent_alerts_24h": 5,
    "critical_unresolved": 1
  },
  "last_updated": "2025-07-15T10:30:00Z"
}
```

## Health Checks

### **GET /health**
API Gateway health check.

### **GET /{service}/health**
Individual service health checks:
- `/auth/health` - Auth service
- `/devices/health` - Device service  
- `/monitoring/health` - Monitoring service
- `/alerts/health` - Alert service
- `/notifications/health` - Notification service
- `/reports/health` - Reporting service

## Error Handling

All APIs return consistent error responses:

```json
{
  "detail": "Error description",
  "status_code": 400,
  "timestamp": "2025-07-15T10:30:00Z"
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error
- `503` - Service Unavailable

## Rate Limiting

The API Gateway implements rate limiting:
- **Authenticated users**: 1000 requests per hour
- **Unauthenticated users**: 100 requests per hour

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1626345600
```

- **GET /alerts**
  - **Description:** Retrieves a list of all alerts.
- **GET /alerts/{alert_id}**
  - **Description:** Retrieves details for a specific alert.
- **PUT /alerts/{alert_id}**
  - **Description:** Updates the status of an alert (e.g., acknowledge, resolve).
