# NetPulse Architecture Documentation

<div align="center">

[![Architecture](https://img.shields.io/badge/Architecture-Microservices-blue?style=for-the-badge)](.)
[![Status](https://img.shields.io/badge/Status-v1.0-green?style=for-the-badge)](.)
[![Last Updated](https://img.shields.io/badge/Updated-July%202025-orange?style=for-the-badge)](.)

**Comprehensive System Architecture Guide for NetPulse**

*Real-time Network Operations Center (NOC) Monitoring Platform*

</div>

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Component Architecture](#component-architecture)
- [Data Flow](#data-flow)
- [Technology Stack](#technology-stack)
- [Database Design](#database-design)
- [Security Architecture](#security-architecture)
- [Deployment Architecture](#deployment-architecture)
- [Scalability Considerations](#scalability-considerations)
- [Monitoring & Observability](#monitoring--observability)

---

## Overview

NetPulse follows a **modern microservices architecture** with clear separation of concerns, designed for high availability, scalability, and maintainability. The system consists of **6 independent microservices** that communicate through well-defined APIs, message queues, and an API Gateway that handles routing and authentication.

### **Architectural Principles**

- **Microservices**: 6 independently deployable services with single responsibilities
- **API Gateway Pattern**: Centralized routing, authentication, and cross-cutting concerns
- **Event-Driven**: Asynchronous communication using RabbitMQ and Celery
- **Domain-Driven Design**: Services organized around business capabilities
- **Security-First**: JWT-based authentication with service-to-service verification
- **Observable**: Comprehensive logging, metrics, and distributed tracing
- **Cloud-Native**: Container-first design optimized for Kubernetes deployment

### **Service Overview**

| **Service** | **Port** | **Responsibility** | **Database** |
|-------------|----------|-------------------|--------------|
| **API Gateway** | 8000 | Request routing, authentication | None |
| **Auth Service** | 8001 | User authentication, JWT tokens | PostgreSQL |
| **Device Service** | 8002 | Device CRUD operations | PostgreSQL |
| **Monitoring Service** | 8003 | Real-time monitoring, WebSocket | TimescaleDB |
| **Alert Service** | 8004 | Alert processing, correlation | PostgreSQL |
| **Notification Service** | 8005 | Multi-channel notifications | None |
| **Reporting Service** | 8006 | Analytics, insights generation | PostgreSQL |

---

## System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Dashboard<br/>React + TypeScript]
        MOBILE[Mobile App<br/>React Native]
        API_CLIENT[API Clients<br/>External Systems]
    end
    
    subgraph "Load Balancer"
        LB[nginx/CloudFlare<br/>SSL Termination]
    end
    
    subgraph "API Gateway Layer"
        GATEWAY[API Gateway Service<br/>Port 8000<br/>FastAPI + Request Routing]
    end
    
    subgraph "Microservices"
        AUTH[Auth Service<br/>Port 8001<br/>JWT Authentication]
        DEVICE[Device Service<br/>Port 8002<br/>Device Management]
        MONITOR[Monitoring Service<br/>Port 8003<br/>Real-time Monitoring]
        ALERT[Alert Service<br/>Port 8004<br/>Alert Processing]
        NOTIFY[Notification Service<br/>Port 8005<br/>Multi-channel Notifications]
        REPORT[Reporting Service<br/>Port 8006<br/>Analytics & Reports]
    end
    
    subgraph "Data Layer"
        POSTGRES[(PostgreSQL 15<br/>Primary Database)]
        TIMESCALE[(TimescaleDB<br/>Time-series Metrics)]
        REDIS[(Redis 7<br/>Cache & Sessions)]
    end
    
    subgraph "Message Queue"
        RABBIT[RabbitMQ<br/>Message Broker]
        CELERY[Celery Workers<br/>Background Tasks]
    end
    
    subgraph "External Services"
        SENDGRID[SendGrid<br/>Email Service]
        AFRICAS[Africa's Talking<br/>SMS Service]
        WEBHOOKS[Webhook Endpoints<br/>External Integrations]
    end
    
    subgraph "Monitoring Stack"
        PROMETHEUS[Prometheus<br/>Metrics Collection]
        GRAFANA[Grafana<br/>Visualization]
        JAEGER[Jaeger<br/>Distributed Tracing]
    end
    
    %% Client connections
    WEB --> LB
    MOBILE --> LB
    API_CLIENT --> LB
    
    %% Load balancer to gateway
    LB --> GATEWAY
    
    %% Gateway to services
    GATEWAY --> AUTH
    GATEWAY --> DEVICE
    GATEWAY --> MONITOR
    GATEWAY --> ALERT
    GATEWAY --> NOTIFY
    GATEWAY --> REPORT
    
    %% Service to database connections
    AUTH --> POSTGRES
    DEVICE --> POSTGRES
    MONITOR --> TIMESCALE
    ALERT --> POSTGRES
    REPORT --> POSTGRES
    
    %% Cache connections
    AUTH --> REDIS
    GATEWAY --> REDIS
    MONITOR --> REDIS
    
    %% Message queue connections
    MONITOR --> RABBIT
    ALERT --> RABBIT
    NOTIFY --> RABBIT
    RABBIT --> CELERY
    
    %% External service connections
    NOTIFY --> SENDGRID
    NOTIFY --> AFRICAS
    NOTIFY --> WEBHOOKS
    
    %% Monitoring connections
    GATEWAY -.-> PROMETHEUS
    AUTH -.-> PROMETHEUS
    DEVICE -.-> PROMETHEUS
    MONITOR -.-> PROMETHEUS
    ALERT -.-> PROMETHEUS
    NOTIFY -.-> PROMETHEUS
    REPORT -.-> PROMETHEUS
    
    PROMETHEUS --> GRAFANA
    
    style GATEWAY fill:#e1f5fe
    style AUTH fill:#f3e5f5
    style DEVICE fill:#e8f5e8
    style MONITOR fill:#fff3e0
    style ALERT fill:#ffebee
    style NOTIFY fill:#f1f8e9
    style REPORT fill:#e3f2fd
```

---

## Component Architecture

### **Microservices Detailed Architecture**

#### **1. API Gateway Service (Port 8000)**

```mermaid
graph TB
    subgraph "API Gateway"
        MAIN[FastAPI Application]
        ROUTER[Request Router]
        AUTH_MID[Authentication Middleware]
        CORS[CORS Middleware]
        RATE_LIMIT[Rate Limiting]
    end
    
    subgraph "Routing Logic"
        ROUTE_MAP[Route Mapping]
        SERVICE_DISCO[Service Discovery]
        LOAD_BAL[Load Balancing]
    end
    
    subgraph "Security"
        JWT_VERIFY[JWT Verification]
        TOKEN_REFRESH[Token Refresh]
        RBAC[Role-based Access]
    end
    
    MAIN --> ROUTER
    MAIN --> AUTH_MID
    MAIN --> CORS
    MAIN --> RATE_LIMIT
    
    ROUTER --> ROUTE_MAP
    ROUTER --> SERVICE_DISCO
    ROUTER --> LOAD_BAL
    
    AUTH_MID --> JWT_VERIFY
    AUTH_MID --> TOKEN_REFRESH
    AUTH_MID --> RBAC
```

**Responsibilities:**
- Route requests to appropriate microservices
- JWT token validation and refresh
- Rate limiting and CORS handling
- Service discovery and load balancing
- Request/response transformation

#### **2. Authentication Service (Port 8001)**

```mermaid
graph TB
    subgraph "Auth Service"
        AUTH_API[FastAPI Endpoints]
        USER_MGR[User Management]
        ORG_MGR[Organization Management]
        TOKEN_MGR[Token Management]
    end
    
    subgraph "Security Layer"
        PWD_HASH[Password Hashing]
        JWT_GEN[JWT Generation]
        REFRESH[Token Refresh]
        VALIDATION[Token Validation]
    end
    
    subgraph "Database"
        USER_MODEL[User Model]
        ORG_MODEL[Organization Model]
        SESSION_MODEL[Session Model]
    end
    
    AUTH_API --> USER_MGR
    AUTH_API --> ORG_MGR
    AUTH_API --> TOKEN_MGR
    
    USER_MGR --> PWD_HASH
    TOKEN_MGR --> JWT_GEN
    TOKEN_MGR --> REFRESH
    TOKEN_MGR --> VALIDATION
    
    USER_MGR --> USER_MODEL
    ORG_MGR --> ORG_MODEL
    TOKEN_MGR --> SESSION_MODEL
```

**Responsibilities:**
- User registration and authentication
- JWT token generation and validation
- Organization management
- Role-based access control
- Session management

#### **3. Device Service (Port 8002)**

```mermaid
graph TB
    subgraph "Device Service"
        DEVICE_API[FastAPI Endpoints]
        DEVICE_CRUD[Device CRUD]
        STATUS_MGR[Status Management]
        CONFIG_MGR[Configuration Management]
    end
    
    subgraph "Business Logic"
        VALIDATION[Device Validation]
        INVENTORY[Inventory Management]
        GROUPING[Device Grouping]
        METADATA[Metadata Management]
    end
    
    subgraph "Database"
        DEVICE_MODEL[Device Model]
        CONFIG_MODEL[Configuration Model]
        GROUP_MODEL[Device Group Model]
    end
    
    DEVICE_API --> DEVICE_CRUD
    DEVICE_API --> STATUS_MGR
    DEVICE_API --> CONFIG_MGR
    
    DEVICE_CRUD --> VALIDATION
    STATUS_MGR --> INVENTORY
    CONFIG_MGR --> GROUPING
    CONFIG_MGR --> METADATA
    
    DEVICE_CRUD --> DEVICE_MODEL
    CONFIG_MGR --> CONFIG_MODEL
    GROUPING --> GROUP_MODEL
```

**Responsibilities:**
- Device registration and management
- Device status tracking
- Configuration management
- Device grouping and tagging
- Inventory management

#### **4. Monitoring Service (Port 8003)**

```mermaid
graph TB
    subgraph "Monitoring Service"
        MONITOR_API[FastAPI + WebSocket]
        HEALTH_CHECK[Health Checking]
        METRIC_COL[Metrics Collection]
        REALTIME[Real-time Streaming]
    end
    
    subgraph "Data Processing"
        PING_SERVICE[Ping Monitoring]
        SNMP_SERVICE[SNMP Collection]
        METRIC_PROC[Metrics Processing]
        THRESHOLD[Threshold Checking]
    end
    
    subgraph "Background Tasks"
        CELERY_TASKS[Celery Tasks]
        SCHEDULER[Task Scheduler]
        WORKER_POOL[Worker Pool]
    end
    
    subgraph "Data Storage"
        TIMESERIES[TimescaleDB]
        METRIC_MODEL[Metrics Model]
        REDIS_CACHE[Redis Cache]
    end
    
    MONITOR_API --> HEALTH_CHECK
    MONITOR_API --> METRIC_COL
    MONITOR_API --> REALTIME
    
    HEALTH_CHECK --> PING_SERVICE
    METRIC_COL --> SNMP_SERVICE
    METRIC_COL --> METRIC_PROC
    METRIC_PROC --> THRESHOLD
    
    HEALTH_CHECK --> CELERY_TASKS
    METRIC_COL --> SCHEDULER
    SCHEDULER --> WORKER_POOL
    
    METRIC_PROC --> TIMESERIES
    METRIC_COL --> METRIC_MODEL
    REALTIME --> REDIS_CACHE
```

**Responsibilities:**
- Real-time device monitoring
- Metrics collection and processing
- WebSocket streaming for live updates
- Background health checking
- Time-series data storage

#### **5. Alert Service (Port 8004)**

```mermaid
graph TB
    subgraph "Alert Service"
        ALERT_API[FastAPI Endpoints]
        ALERT_PROC[Alert Processing]
        CORRELATION[Alert Correlation]
        ESCALATION[Escalation Logic]
    end
    
    subgraph "Alert Logic"
        THRESHOLD[Threshold Engine]
        ANOMALY[Anomaly Detection]
        SUPPRESSION[Alert Suppression]
        GROUPING[Alert Grouping]
    end
    
    subgraph "Workflow"
        ACK_MGR[Acknowledgment]
        RESOLUTION[Resolution Tracking]
        SLA_TRACK[SLA Tracking]
        HISTORY[Alert History]
    end
    
    subgraph "Database"
        ALERT_MODEL[Alert Model]
        RULE_MODEL[Alert Rules Model]
        HISTORY_MODEL[History Model]
    end
    
    ALERT_API --> ALERT_PROC
    ALERT_API --> CORRELATION
    ALERT_API --> ESCALATION
    
    ALERT_PROC --> THRESHOLD
    ALERT_PROC --> ANOMALY
    CORRELATION --> SUPPRESSION
    CORRELATION --> GROUPING
    
    ESCALATION --> ACK_MGR
    ESCALATION --> RESOLUTION
    ESCALATION --> SLA_TRACK
    ESCALATION --> HISTORY
    
    ALERT_PROC --> ALERT_MODEL
    THRESHOLD --> RULE_MODEL
    HISTORY --> HISTORY_MODEL
```

**Responsibilities:**
- Alert processing and correlation
- Threshold-based alerting
- Alert acknowledgment and resolution
- Escalation workflows
- Alert history and reporting

#### **6. Notification Service (Port 8005)**

```mermaid
graph TB
    subgraph "Notification Service"
        NOTIFY_API[FastAPI Endpoints]
        CHANNEL_MGR[Channel Manager]
        TEMPLATE_MGR[Template Manager]
        DELIVERY[Delivery Engine]
    end
    
    subgraph "Notification Channels"
        EMAIL[Email Service]
        SMS[SMS Service]
        WEBHOOK[Webhook Service]
        SLACK[Slack Integration]
    end
    
    subgraph "External APIs"
        SENDGRID[SendGrid API]
        AFRICAS[Africa's Talking]
        SLACK_API[Slack API]
        CUSTOM_HOOKS[Custom Webhooks]
    end
    
    subgraph "Background Processing"
        QUEUE[Message Queue]
        RETRY[Retry Logic]
        BATCH[Batch Processing]
        TRACKING[Delivery Tracking]
    end
    
    NOTIFY_API --> CHANNEL_MGR
    NOTIFY_API --> TEMPLATE_MGR
    NOTIFY_API --> DELIVERY
    
    CHANNEL_MGR --> EMAIL
    CHANNEL_MGR --> SMS
    CHANNEL_MGR --> WEBHOOK
    CHANNEL_MGR --> SLACK
    
    EMAIL --> SENDGRID
    SMS --> AFRICAS
    SLACK --> SLACK_API
    WEBHOOK --> CUSTOM_HOOKS
    
    DELIVERY --> QUEUE
    DELIVERY --> RETRY
    DELIVERY --> BATCH
    DELIVERY --> TRACKING
```

**Responsibilities:**
- Multi-channel notification delivery
- Email, SMS, and webhook notifications
- Template management and personalization
- Delivery tracking and retry logic
- Integration with external services

#### **7. Reporting Service (Port 8006)**

```mermaid
graph TB
    subgraph "Reporting Service"
        REPORT_API[FastAPI Endpoints]
        ANALYTICS[Analytics Engine]
        EXPORT[Export Engine]
        SCHEDULER[Report Scheduler]
    end
    
    subgraph "Report Types"
        UPTIME[Uptime Reports]
        PERFORMANCE[Performance Reports]
        ALERT_RPT[Alert Reports]
        CUSTOM[Custom Reports]
    end
    
    subgraph "Data Sources"
        DEVICE_DATA[Device Data]
        METRIC_DATA[Metrics Data]
        ALERT_DATA[Alert Data]
        USER_DATA[User Data]
    end
    
    subgraph "Output Formats"
        PDF[PDF Export]
        CSV[CSV Export]
        JSON[JSON API]
        DASHBOARD[Dashboard Views]
    end
    
    REPORT_API --> ANALYTICS
    REPORT_API --> EXPORT
    REPORT_API --> SCHEDULER
    
    ANALYTICS --> UPTIME
    ANALYTICS --> PERFORMANCE
    ANALYTICS --> ALERT_RPT
    ANALYTICS --> CUSTOM
    
    UPTIME --> DEVICE_DATA
    PERFORMANCE --> METRIC_DATA
    ALERT_RPT --> ALERT_DATA
    CUSTOM --> USER_DATA
    
    EXPORT --> PDF
    EXPORT --> CSV
    EXPORT --> JSON
    EXPORT --> DASHBOARD
```

**Responsibilities:**
- Uptime and performance reporting
- Alert analytics and insights
- Scheduled report generation
- Multi-format export capabilities
- Custom dashboard creation

---

## Data Flow

### **Real-time Monitoring Flow**

```mermaid
sequenceDiagram
    participant Device as Network Device
    participant Monitor as Monitoring Service
    participant Queue as RabbitMQ
    participant Worker as Celery Worker
    participant DB as TimescaleDB
    participant WS as WebSocket
    participant Client as Frontend
    participant Alert as Alert Service
    
    Device->>Monitor: PING/SNMP Health Check
    Monitor->>Queue: Queue Metric Collection
    Queue->>Worker: Process Metrics
    Worker->>DB: Store Time-series Data
    Worker->>WS: Broadcast Real-time Updates
    WS->>Client: Live Dashboard Updates
    
    Note over Worker,DB: Threshold Analysis
    Worker->>Worker: Analyze Thresholds
    Worker->>Alert: Send Alert if Threshold Exceeded
    Alert->>Queue: Queue Alert for Processing
    Queue->>Worker: Process Alert
    Worker->>Client: Alert Notification
```

### **Alert Processing Flow**

```mermaid
flowchart TD
    START([Metric Received]) --> VALIDATE{Validate Data}
    VALIDATE -->|Valid| THRESHOLD{Check Thresholds}
    VALIDATE -->|Invalid| LOG[Log Error]
    
    THRESHOLD -->|Normal| STORE[Store Metric]
    THRESHOLD -->|Anomaly| CREATE_ALERT[Create Alert]
    
    CREATE_ALERT --> SEVERITY{Determine Severity}
    SEVERITY -->|Critical| IMMEDIATE[Immediate Notification]
    SEVERITY -->|Warning| QUEUE_ALERT[Queue for Batch]
    SEVERITY -->|Info| LOG_ONLY[Log Only]
    
    IMMEDIATE --> MULTI_CHANNEL[Multi-channel Notification]
    QUEUE_ALERT --> BATCH[Batch Processing]
    
    MULTI_CHANNEL --> SMS[SMS Alert]
    MULTI_CHANNEL --> EMAIL[Email Alert]
    MULTI_CHANNEL --> WEBHOOK[Webhook Alert]
    
    SMS --> TRACK[Track Delivery]
    EMAIL --> TRACK
    WEBHOOK --> TRACK
    
    STORE --> END([End])
    LOG --> END
    LOG_ONLY --> END
    TRACK --> END
    BATCH --> END
```

### **User Authentication Flow**

```mermaid
sequenceDiagram
    participant Client as Frontend
    participant Gateway as API Gateway
    participant Auth as Auth Service
    participant Device as Device Service
    participant Redis as Redis Cache
    
    Client->>Gateway: POST /auth/login
    Gateway->>Auth: Forward Login Request
    Auth->>Auth: Validate Credentials
    Auth->>Auth: Generate JWT Token
    Auth->>Redis: Store Session Data
    Auth->>Gateway: Return JWT Token
    Gateway->>Client: Login Response with Token
    
    Note over Client,Gateway: Subsequent API Calls
    Client->>Gateway: API Request with JWT
    Gateway->>Auth: Verify Token
    Auth->>Redis: Check Session
    Auth->>Gateway: Token Valid Response
    Gateway->>Device: Forward to Service
    Device->>Gateway: Service Response
    Gateway->>Client: Final Response
```

---

## Technology Stack

### **Microservices Technology Matrix**

| **Service** | **Framework** | **Database** | **Key Libraries** |
|-------------|---------------|--------------|-------------------|
| **API Gateway** | FastAPI 0.104 | Redis (cache) | `httpx`, `python-jose`, `uvicorn` |
| **Auth Service** | FastAPI 0.104 | PostgreSQL | `passlib`, `python-jose`, `sqlalchemy` |
| **Device Service** | FastAPI 0.104 | PostgreSQL | `sqlalchemy`, `pydantic`, `httpx` |
| **Monitoring Service** | FastAPI 0.104 | TimescaleDB | `celery`, `redis`, `websockets` |
| **Alert Service** | FastAPI 0.104 | PostgreSQL | `celery`, `sqlalchemy`, `redis` |
| **Notification Service** | FastAPI 0.104 | None | `requests`, `celery`, `sendgrid` |
| **Reporting Service** | FastAPI 0.104 | PostgreSQL | `pandas`, `matplotlib`, `sqlalchemy` |

### **Infrastructure Components**

| **Component** | **Technology** | **Version** | **Purpose** |
|---------------|----------------|-------------|-------------|
| **Container Runtime** | Docker | 24.x | Application containerization |
| **Orchestration** | Docker Compose | 2.x | Local development orchestration |
| **Load Balancer** | nginx | 1.25 | Request distribution and SSL termination |
| **Message Queue** | RabbitMQ | 3.12 | Asynchronous task processing |
| **Cache** | Redis | 7.x | Session storage and caching |
| **Database** | PostgreSQL | 15.x | Primary data storage |
| **Time-series DB** | TimescaleDB | 2.x | Metrics and time-series data |
| **Monitoring** | Prometheus | 2.x | Metrics collection |
| **Visualization** | Grafana | 10.x | Dashboards and alerting |
| **Tracing** | Jaeger | 1.x | Distributed tracing |

### **Development Tools**

| **Category** | **Tool** | **Purpose** |
|--------------|----------|-------------|
| **Code Quality** | Black, Flake8 | Python code formatting and linting |
| **Testing** | pytest, pytest-cov | Unit and integration testing |
| **API Documentation** | FastAPI/OpenAPI | Automatic API documentation |
| **Type Checking** | mypy | Static type checking |
| **Dependency Management** | pip-tools | Python dependency management |
| **CI/CD** | GitHub Actions | Continuous integration and deployment |

---

## Database Design

### **PostgreSQL Schema (Shared across services)**

```sql
-- Organizations table (used by auth-service)
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Users table (auth-service)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Devices table (device-service)
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    ip_address INET NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    location VARCHAR(255),
    status VARCHAR(20) DEFAULT 'unknown',
    last_seen TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Alerts table (alert-service)
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id UUID,
    organization_id UUID NOT NULL,
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('info', 'warning', 'critical')),
    message TEXT NOT NULL,
    acknowledged BOOLEAN DEFAULT false,
    acknowledged_by UUID,
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    resolved BOOLEAN DEFAULT false,
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Device metrics table (monitoring-service with TimescaleDB)
CREATE TABLE device_metrics (
    time TIMESTAMPTZ NOT NULL,
    device_id UUID NOT NULL,
    metric_type VARCHAR(50) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20),
    PRIMARY KEY (time, device_id, metric_type)
);

-- Convert to TimescaleDB hypertable for time-series optimization
SELECT create_hypertable('device_metrics', 'time');

-- Performance indexes
CREATE INDEX idx_users_organization ON users(organization_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_devices_organization ON devices(organization_id);
CREATE INDEX idx_devices_status ON devices(status);
CREATE INDEX idx_alerts_organization_severity ON alerts(organization_id, severity);
CREATE INDEX idx_alerts_device_time ON alerts(device_id, created_at DESC);
CREATE INDEX idx_device_metrics_device_time ON device_metrics(device_id, time DESC);
CREATE INDEX idx_device_metrics_type_time ON device_metrics(metric_type, time DESC);

-- Retention policies for time-series data
SELECT add_retention_policy('device_metrics', INTERVAL '90 days');
```

### **Redis Data Structures**

```yaml
# Session Management (auth-service)
session:{session_id}:
  user_id: UUID
  organization_id: UUID
  expires_at: timestamp
  permissions: array

# JWT Token Blacklist (auth-service)
blacklist:token:{jti}: expiration_timestamp

# Device Status Cache (monitoring-service)
device:status:{device_id}:
  status: online|offline|unknown
  last_seen: timestamp
  response_time: float

# Real-time Metrics Cache (monitoring-service)
metrics:{device_id}:latest:
  cpu: float
  memory: float
  network: float
  disk: float
  timestamp: timestamp

# Alert Counters (alert-service)
alerts:count:{organization_id}: integer
alerts:critical:{organization_id}: integer
alerts:unresolved:{organization_id}: integer

# Rate Limiting (api-gateway)
rate_limit:{user_id}:{endpoint}: request_count
rate_limit:{ip}:{endpoint}: request_count

# Background Task Results (celery)
celery-task-meta-{task_id}: task_result_json
```

---

## Security Architecture

### **Authentication & Authorization**

```mermaid
flowchart TD
    CLIENT[Client Request] --> GATEWAY[API Gateway]
    GATEWAY --> JWT_CHECK{JWT Valid?}
    
    JWT_CHECK -->|No| AUTH_SERVICE[Auth Service]
    AUTH_SERVICE --> LOGIN[User Login]
    LOGIN --> JWT_GENERATE[Generate JWT]
    JWT_GENERATE --> REDIS_SESSION[Store Session]
    
    JWT_CHECK -->|Yes| EXTRACT_CLAIMS[Extract Claims]
    EXTRACT_CLAIMS --> RBAC{Check Permissions}
    
    RBAC -->|Authorized| FORWARD[Forward to Service]
    RBAC -->|Denied| FORBIDDEN[403 Forbidden]
    
    FORWARD --> MICROSERVICE[Target Microservice]
    MICROSERVICE --> VALIDATE_ORG[Validate Organization]
    VALIDATE_ORG --> BUSINESS_LOGIC[Execute Business Logic]
    
    REDIS_SESSION --> RESPONSE[Return Response]
    BUSINESS_LOGIC --> RESPONSE
    FORBIDDEN --> RESPONSE
```

### **Security Layers**

| **Layer** | **Component** | **Security Measures** |
|-----------|---------------|----------------------|
| **Network** | nginx/Load Balancer | TLS 1.3, Rate limiting, DDoS protection |
| **API Gateway** | FastAPI Gateway | JWT validation, Request sanitization, CORS |
| **Service-to-Service** | Internal APIs | mTLS, Service mesh authentication |
| **Data** | PostgreSQL/Redis | Encryption at rest, Connection encryption |
| **Application** | Microservices | Input validation, SQL injection prevention |
| **Container** | Docker | Non-root users, Minimal base images |
| **Secrets** | Environment Variables | Encrypted environment variables, Vault integration |

### **Security Implementations**

```python
# JWT Token Structure
{
  "sub": "user_id",
  "org": "organization_id", 
  "exp": 1234567890,
  "iat": 1234567890,
  "jti": "token_unique_id",
  "permissions": ["device:read", "alert:write"],
  "scopes": ["monitoring", "alerts"]
}

# Role-Based Access Control
PERMISSIONS = {
    "admin": ["*"],
    "operator": ["device:read", "device:write", "alert:read", "alert:write"],
    "viewer": ["device:read", "alert:read", "report:read"],
    "api_user": ["device:read", "metrics:read"]
}

# Rate Limiting Rules
RATE_LIMITS = {
    "auth_endpoints": "5/minute",
    "api_endpoints": "100/minute", 
    "monitoring_endpoints": "1000/minute",
    "bulk_operations": "10/hour"
}
```

---

## Performance & Scalability

### **Performance Metrics**

| **Service** | **Expected Load** | **Response Time** | **Throughput** |
|-------------|-------------------|-------------------|----------------|
| **API Gateway** | 10k req/min | < 10ms | 1000 RPS |
| **Auth Service** | 1k req/min | < 100ms | 100 RPS |
| **Device Service** | 5k req/min | < 50ms | 500 RPS |
| **Monitoring Service** | 50k metrics/min | < 200ms | 2000 RPS |
| **Alert Service** | 1k alerts/min | < 100ms | 200 RPS |
| **Notification Service** | 500 notifications/min | < 500ms | 100 RPS |
| **Reporting Service** | 100 reports/hour | < 2s | 10 RPS |

### **Caching Strategy**

```mermaid
flowchart TD
    CLIENT[Client Request] --> NGINX[nginx Cache]
    NGINX -->|Cache Miss| GATEWAY[API Gateway]
    NGINX -->|Cache Hit| RETURN_CACHED[Return Cached Response]
    
    GATEWAY --> REDIS[Redis Cache]
    REDIS -->|Cache Hit| RETURN_REDIS[Return from Redis]
    REDIS -->|Cache Miss| SERVICE[Microservice]
    
    SERVICE --> DATABASE[Database Query]
    DATABASE --> CACHE_STORE[Store in Cache]
    CACHE_STORE --> RETURN_FRESH[Return Fresh Data]
    
    RETURN_CACHED --> CLIENT
    RETURN_REDIS --> CLIENT
    RETURN_FRESH --> CLIENT
```

### **Database Performance Optimizations**

```sql
-- TimescaleDB Optimizations
-- Continuous aggregates for real-time dashboards
CREATE MATERIALIZED VIEW device_metrics_hourly
WITH (timescaledb.continuous) AS
SELECT device_id,
       time_bucket('1 hour', time) as bucket,
       AVG(value) as avg_value,
       MAX(value) as max_value,
       MIN(value) as min_value,
       COUNT(*) as data_points
FROM device_metrics 
WHERE metric_type = 'cpu_usage'
GROUP BY device_id, bucket;

-- Retention policies
SELECT add_retention_policy('device_metrics', INTERVAL '90 days');
SELECT add_retention_policy('device_metrics_hourly', INTERVAL '1 year');

-- Compression policies
SELECT add_compression_policy('device_metrics', INTERVAL '7 days');

-- PostgreSQL optimizations
-- Partitioning for large tables
CREATE TABLE alerts_y2024 PARTITION OF alerts
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- Indexes for common queries
CREATE INDEX CONCURRENTLY idx_alerts_org_created 
ON alerts(organization_id, created_at DESC) 
WHERE resolved = false;

CREATE INDEX CONCURRENTLY idx_devices_status_location 
ON devices(status, location) 
WHERE is_active = true;
```

### **Horizontal Scaling Configuration**

```yaml
# docker-compose.prod.yml scaling
version: '3.8'
services:
  api-gateway:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
  
  auth-service:
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
  
  device-service:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
          
  monitoring-service:
    deploy:
      replicas: 5
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
          
  # Load balancer configuration
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api-gateway
```

---

## Monitoring & Observability

### **Metrics Collection**

```mermaid
flowchart TD
    SERVICES[Microservices] --> PROMETHEUS[Prometheus]
    SERVICES --> JAEGER[Jaeger Tracing]
    SERVICES --> LOGS[Centralized Logging]
    
    PROMETHEUS --> GRAFANA[Grafana Dashboards]
    PROMETHEUS --> ALERTMANAGER[Alert Manager]
    
    JAEGER --> TRACE_UI[Tracing UI]
    LOGS --> ELK[ELK Stack]
    
    GRAFANA --> ALERTS[Visual Alerts]
    ALERTMANAGER --> NOTIFICATION[Notification Channels]
    
    NOTIFICATION --> SLACK[Slack]
    NOTIFICATION --> EMAIL[Email]
    NOTIFICATION --> PAGERDUTY[PagerDuty]
```

### **Key Performance Indicators (KPIs)**

| **Category** | **Metric** | **Target** | **Alert Threshold** |
|--------------|------------|------------|-------------------|
| **Availability** | Service Uptime | 99.9% | < 99.5% |
| **Performance** | API Response Time | < 100ms | > 500ms |
| **Throughput** | Requests/second | 1000 RPS | < 500 RPS |
| **Errors** | Error Rate | < 0.1% | > 1% |
| **Resources** | CPU Utilization | < 70% | > 85% |
| **Resources** | Memory Usage | < 80% | > 90% |
| **Database** | Query Performance | < 50ms | > 200ms |
| **Queue** | Message Lag | < 1 minute | > 5 minutes |

### **Prometheus Metrics Examples**

```python
# Custom metrics in microservices
from prometheus_client import Counter, Histogram, Gauge

# Request counters
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# Response time histogram
REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Active connections gauge
ACTIVE_CONNECTIONS = Gauge(
    'active_database_connections',
    'Active database connections'
)

# Device-specific metrics
DEVICE_STATUS = Gauge(
    'device_online_status',
    'Device online status (1=online, 0=offline)',
    ['device_id', 'device_type']
)

ALERT_COUNT = Counter(
    'alerts_generated_total',
    'Total alerts generated',
    ['severity', 'alert_type']
)
```

### **Health Check Endpoints**

```python
# Health check implementation
@app.get("/health")
async def health_check():
    checks = {
        "database": await check_database_connection(),
        "redis": await check_redis_connection(), 
        "message_queue": await check_rabbitmq_connection(),
        "external_apis": await check_external_dependencies()
    }
    
    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503
    
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if all_healthy else "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": checks,
            "version": os.getenv("APP_VERSION", "unknown")
        }
    )

# Readiness probe
@app.get("/ready")
async def readiness_check():
    """Check if service is ready to handle requests"""
    return {"status": "ready", "timestamp": datetime.utcnow().isoformat()}

# Liveness probe  
@app.get("/alive")
async def liveness_check():
    """Check if service is alive"""
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}
```

---

## API Design Standards

### **RESTful API Conventions**

| **Resource** | **HTTP Method** | **Endpoint** | **Description** |
|--------------|-----------------|--------------|-----------------|
| **Devices** | GET | `/api/v1/devices` | List all devices |
| **Devices** | POST | `/api/v1/devices` | Create new device |
| **Devices** | GET | `/api/v1/devices/{id}` | Get device by ID |
| **Devices** | PUT | `/api/v1/devices/{id}` | Update device |
| **Devices** | DELETE | `/api/v1/devices/{id}` | Delete device |
| **Alerts** | GET | `/api/v1/alerts` | List alerts |
| **Alerts** | POST | `/api/v1/alerts/{id}/acknowledge` | Acknowledge alert |
| **Metrics** | GET | `/api/v1/devices/{id}/metrics` | Get device metrics |
| **Reports** | GET | `/api/v1/reports` | List reports |
| **Reports** | POST | `/api/v1/reports/generate` | Generate report |

### **API Response Format**

```json
// Success Response
{
  "success": true,
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Server-01",
    "status": "online"
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "v1",
    "request_id": "req_123456789"
  }
}

// Error Response
{
  "success": false,
  "error": {
    "code": "DEVICE_NOT_FOUND",
    "message": "Device with ID 123 not found",
    "details": {
      "device_id": "123",
      "organization_id": "org_456"
    }
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "v1",
    "request_id": "req_123456789"
  }
}

// Paginated Response
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total": 150,
    "total_pages": 3,
    "has_next": true,
    "has_prev": false
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "v1",
    "request_id": "req_123456789"
  }
}
```

### **Error Handling Standards**

```python
# Standard Error Codes
class ErrorCodes:
    # Authentication & Authorization
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"
    
    # Resource Errors
    DEVICE_NOT_FOUND = "DEVICE_NOT_FOUND"
    DEVICE_ALREADY_EXISTS = "DEVICE_ALREADY_EXISTS"
    INVALID_DEVICE_TYPE = "INVALID_DEVICE_TYPE"
    
    # Validation Errors
    INVALID_INPUT = "INVALID_INPUT"
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    INVALID_IP_ADDRESS = "INVALID_IP_ADDRESS"
    
    # System Errors
    DATABASE_ERROR = "DATABASE_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"

# Exception Handler
from fastapi import HTTPException
from fastapi.responses import JSONResponse

class NetPulseException(Exception):
    def __init__(self, code: str, message: str, details: dict = None, status_code: int = 400):
        self.code = code
        self.message = message
        self.details = details or {}
        self.status_code = status_code

@app.exception_handler(NetPulseException)
async def netpulse_exception_handler(request: Request, exc: NetPulseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            },
            "meta": {
                "timestamp": datetime.utcnow().isoformat(),
                "version": "v1",
                "request_id": request.headers.get("x-request-id")
            }
        }
    )
```

### **Request/Response Middleware**

```python
# Middleware for standardized responses
@app.middleware("http")
async def standardize_response_middleware(request: Request, call_next):
    # Add request ID
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Add correlation ID header
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-API-Version"] = "v1"
    
    return response

# Request validation middleware
@app.middleware("http") 
async def request_validation_middleware(request: Request, call_next):
    # Validate content type for POST/PUT requests
    if request.method in ["POST", "PUT", "PATCH"]:
        content_type = request.headers.get("content-type", "")
        if not content_type.startswith("application/json"):
            return JSONResponse(
                status_code=415,
                content={
                    "success": False,
                    "error": {
                        "code": "UNSUPPORTED_MEDIA_TYPE",
                        "message": "Content-Type must be application/json"
                    }
                }
            )
    
    return await call_next(request)
```

---

## Development Guidelines

### **Code Standards**

```python
# Service Structure Template
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

# Service Layer Pattern
class DeviceService:
    def __init__(self, db: Session):
        self.db = db
    
    async def create_device(self, device_data: DeviceCreate) -> Device:
        """Create a new device with validation"""
        # Validate IP address uniqueness
        existing = self.db.query(Device).filter(
            Device.ip_address == device_data.ip_address
        ).first()
        
        if existing:
            raise NetPulseException(
                code="DEVICE_ALREADY_EXISTS",
                message=f"Device with IP {device_data.ip_address} already exists",
                status_code=409
            )
        
        # Create device
        device = Device(
            id=uuid.uuid4(),
            **device_data.dict(),
            created_at=datetime.utcnow()
        )
        
        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        
        return device

# Repository Pattern for Database Access
class DeviceRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, device_id: str) -> Optional[Device]:
        return self.db.query(Device).filter(Device.id == device_id).first()
    
    def get_by_organization(self, org_id: str, skip: int = 0, limit: int = 100) -> List[Device]:
        return (
            self.db.query(Device)
            .filter(Device.organization_id == org_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
```

### **Testing Standards**

```python
# Unit Testing Template
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test Configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    """Create test database session"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_client():
    """Create test client"""
    return TestClient(app)

# Test Examples
class TestDeviceService:
    def test_create_device_success(self, test_db):
        service = DeviceService(test_db)
        device_data = DeviceCreate(
            name="Test Device",
            ip_address="192.168.1.100",
            device_type="server"
        )
        
        device = await service.create_device(device_data)
        
        assert device.name == "Test Device"
        assert device.ip_address == "192.168.1.100"
        assert device.id is not None
    
    def test_create_device_duplicate_ip_fails(self, test_db):
        service = DeviceService(test_db)
        device_data = DeviceCreate(
            name="Test Device",
            ip_address="192.168.1.100",
            device_type="server"
        )
        
        # Create first device
        await service.create_device(device_data)
        
        # Attempt to create duplicate should fail
        with pytest.raises(NetPulseException) as exc_info:
            await service.create_device(device_data)
        
        assert exc_info.value.code == "DEVICE_ALREADY_EXISTS"

# Integration Testing
class TestDeviceAPI:
    def test_create_device_endpoint(self, test_client):
        response = test_client.post(
            "/api/v1/devices",
            json={
                "name": "Test Device",
                "ip_address": "192.168.1.100", 
                "device_type": "server"
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "Test Device"
```

### **Deployment Checklist**

- [ ] **Code Quality**
  - [ ] All tests passing (unit, integration, e2e)
  - [ ] Code coverage > 80%
  - [ ] Linting checks passed (flake8, black)
  - [ ] Type checking passed (mypy)
  - [ ] Security scan completed (bandit)

- [ ] **Configuration**
  - [ ] Environment variables configured
  - [ ] Database migrations applied
  - [ ] Redis cache configured
  - [ ] RabbitMQ queues created
  - [ ] SSL certificates installed

- [ ] **Monitoring**
  - [ ] Health checks implemented
  - [ ] Prometheus metrics exposed
  - [ ] Grafana dashboards configured
  - [ ] Alert rules configured
  - [ ] Log aggregation setup

- [ ] **Security**
  - [ ] JWT secret keys rotated
  - [ ] Database passwords updated
  - [ ] API rate limiting configured
  - [ ] CORS policies configured
  - [ ] Security headers implemented

- [ ] **Performance**
  - [ ] Database indexes optimized
  - [ ] Cache warming scripts run
  - [ ] Load testing completed
  - [ ] Resource limits configured
  - [ ] Auto-scaling policies set

---

## Future Improvements

### **Short-term Enhancements (Next 3 months)**

1. **Enhanced Monitoring**
   - Real-time alerting improvements
   - Custom dashboard builder
   - Mobile push notifications
   - Alert correlation and noise reduction

2. **Performance Optimizations**
   - Database query optimization
   - Caching layer improvements
   - Background job optimization
   - API response time improvements

3. **User Experience**
   - Single Sign-On (SSO) integration
   - Multi-tenant improvements
   - Advanced filtering and search
   - Bulk operations UI

### **Medium-term Goals (3-6 months)**

1. **Advanced Analytics**
   - Machine learning-based anomaly detection
   - Predictive maintenance alerts
   - Trend analysis and forecasting
   - Automated root cause analysis

2. **Integration Capabilities**
   - Third-party monitoring tool integrations
   - Webhook customization
   - API gateway for external integrations
   - Plugin architecture

3. **Scalability Improvements**
   - Kubernetes deployment
   - Auto-scaling implementation
   - Multi-region deployment
   - Event-driven architecture

### **Long-term Vision (6+ months)**

1. **AI-Powered Features**
   - Intelligent alerting with ML
   - Automated remediation
   - Natural language query interface
   - Predictive capacity planning

2. **Enterprise Features**
   - Advanced RBAC with custom roles
   - Audit logging and compliance
   - Multi-cloud monitoring
   - White-label solution

3. **Platform Evolution**
   - Microservices mesh implementation
   - Event sourcing and CQRS
   - Real-time collaboration features
   - API marketplace

---

*This architecture document serves as the technical blueprint for NetPulse's microservices-based network monitoring platform. For implementation details, refer to the service-specific documentation and code comments.*

## Security Architecture

### **Authentication & Authorization**

```mermaid
graph TB
    subgraph "Client Authentication"
        LOGIN[Login Request]
        JWT[JWT Token]
        REFRESH[Refresh Token]
    end
    
    subgraph "API Gateway Security"
        RATE_LIMIT[Rate Limiting]
        CORS[CORS Policy]
        CSRF[CSRF Protection]
    end
    
    subgraph "Service Security"
        RBAC[Role-Based Access]
        PERMISSIONS[Permission System]
        AUDIT[Audit Logging]
    end
    
    subgraph "Data Security"
        ENCRYPTION[Data Encryption]
        HASHING[Password Hashing]
        SANITIZATION[Input Sanitization]
    end
    
    LOGIN --> JWT
    JWT --> REFRESH
    
    JWT --> RATE_LIMIT
    RATE_LIMIT --> CORS
    CORS --> CSRF
    
    CSRF --> RBAC
    RBAC --> PERMISSIONS
    PERMISSIONS --> AUDIT
    
    AUDIT --> ENCRYPTION
    ENCRYPTION --> HASHING
    HASHING --> SANITIZATION
```

**Security Measures:**

- **JWT Authentication**: Stateless authentication with refresh tokens
- **RBAC**: Role-based access control with granular permissions
- **Rate Limiting**: API rate limiting to prevent abuse
- **Input Validation**: Comprehensive input sanitization and validation
- **HTTPS Only**: All communications encrypted in transit
- **Database Encryption**: Sensitive data encrypted at rest
- **Audit Logging**: Complete audit trail of all user actions

---

## Deployment Architecture

### **Container Architecture**

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "Load Balancer"
            LB[nginx/CloudFlare]
        end
        
        subgraph "Application Tier"
            API1[FastAPI Instance 1]
            API2[FastAPI Instance 2]
            API3[FastAPI Instance 3]
        end
        
        subgraph "Worker Tier"
            WORKER1[Celery Worker 1]
            WORKER2[Celery Worker 2]
            WORKER3[Celery Worker 3]
        end
        
        subgraph "Data Tier"
            POSTGRES_PRIMARY[(PostgreSQL Primary)]
            POSTGRES_REPLICA[(PostgreSQL Replica)]
            REDIS_CLUSTER[(Redis Cluster)]
        end
        
        subgraph "Monitoring"
            PROMETHEUS[Prometheus]
            GRAFANA[Grafana]
            ALERTS[AlertManager]
        end
    end
    
    LB --> API1
    LB --> API2
    LB --> API3
    
    API1 --> POSTGRES_PRIMARY
    API2 --> POSTGRES_PRIMARY
    API3 --> POSTGRES_PRIMARY
    
    API1 --> REDIS_CLUSTER
    API2 --> REDIS_CLUSTER
    API3 --> REDIS_CLUSTER
    
    WORKER1 --> POSTGRES_PRIMARY
    WORKER2 --> POSTGRES_PRIMARY
    WORKER3 --> POSTGRES_PRIMARY
    
    POSTGRES_PRIMARY --> POSTGRES_REPLICA
    
    PROMETHEUS --> API1
    PROMETHEUS --> API2
    PROMETHEUS --> API3
    
    GRAFANA --> PROMETHEUS
    ALERTS --> PROMETHEUS
```

### **Docker Compose Architecture**

```yaml
# docker-compose.prod.yml structure
version: '3.8'

services:
  # Frontend
  frontend:
    image: netpulse/frontend:latest
    ports:
      - "3000:80"
    environment:
      - REACT_APP_API_URL=https://api.netpulse.com
    
  # Backend API
  backend:
    image: netpulse/backend:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/netpulse
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    
  # Celery Workers
  worker:
    image: netpulse/backend:latest
    command: celery -A app.worker worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/netpulse
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
      - rabbitmq
    
  # Message Queue
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"
    
  # Databases
  postgres:
    image: timescale/timescaledb:latest-pg14
    environment:
      - POSTGRES_DB=netpulse
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    
  # Monitoring
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  postgres_data:
  redis_data:
  grafana_data:
```

---

## Scalability Considerations

### **Horizontal Scaling Strategy**

| Component | Scaling Method | Considerations |
|-----------|----------------|----------------|
| **Frontend** | CDN + Multiple Replicas | Stateless React app, easy to scale |
| **API Gateway** | Load Balancer + Auto-scaling | Stateless FastAPI instances |
| **Celery Workers** | Queue-based Scaling | Auto-scale based on queue length |
| **PostgreSQL** | Read Replicas + Sharding | Primary-replica setup with read scaling |
| **Redis** | Cluster Mode | Redis Cluster for high availability |
| **Message Queue** | RabbitMQ Cluster | Clustered message queue for reliability |

### **Performance Optimizations**

- **Database Connection Pooling**: Efficient database connections
- **Query Optimization**: Indexed queries and query optimization
- **Caching Strategy**: Multi-level caching (Redis, Application, CDN)
- **Async Processing**: Non-blocking operations using asyncio
- **Background Tasks**: CPU-intensive tasks offloaded to workers
- **WebSocket Optimization**: Efficient real-time data streaming

---

## Monitoring & Observability

### **Metrics Collection**

```yaml
# Prometheus metrics configuration
- Application Metrics:
  - Request rate and latency
  - Error rates and status codes
  - Database query performance
  - Cache hit/miss ratios
  
- Business Metrics:
  - Active devices count
  - Alert generation rate
  - User activity metrics
  - SLA compliance metrics
  
- Infrastructure Metrics:
  - CPU and memory usage
  - Disk I/O and network traffic
  - Container resource usage
  - Database performance
```

### **Logging Strategy**

```yaml
# Structured logging configuration
- Log Levels:
  - ERROR: Application errors and exceptions
  - WARN: Performance degradation warnings
  - INFO: Business logic events
  - DEBUG: Detailed debugging information
  
- Log Aggregation:
  - Centralized logging with ELK stack
  - Log correlation with trace IDs
  - Real-time log analysis
  - Log retention policies
```

### **Alerting Rules**

```yaml
# Alert manager configuration
- Critical Alerts:
  - Service down (>5 minutes)
  - High error rate (>5% for 2 minutes)
  - Database connection failure
  - Memory usage >90%
  
- Warning Alerts:
  - High response time (>2s for 5 minutes)
  - Disk usage >80%
  - Queue backlog >1000 items
  - Cache miss rate >50%
```

---

## Data Backup & Recovery

### **Backup Strategy**

```yaml
PostgreSQL Backups:
  - Full backup: Daily at 2 AM UTC
  - Incremental backup: Every 6 hours
  - Point-in-time recovery: 30-day retention
  - Cross-region replication: Primary + DR site

Redis Backups:
  - RDB snapshots: Every hour
  - AOF replication: Real-time
  - Cluster backup: Coordinated snapshots

Application Backups:
  - Configuration backup: Version controlled
  - Static assets: CDN with backup regions
  - Container images: Multi-registry storage
```

### **Disaster Recovery**

```yaml
Recovery Time Objectives (RTO):
  - Critical services: 15 minutes
  - Full system recovery: 2 hours
  - Data recovery: 4 hours

Recovery Point Objectives (RPO):
  - Real-time data: 5 minutes
  - Historical data: 1 hour
  - Configuration data: 24 hours

DR Procedures:
  - Automated failover: Database and cache
  - Manual failover: Application services
  - Data validation: Post-recovery checks
  - Rollback procedures: Emergency rollback
```

---

## Integration Architecture

### **External Service Integration**

```mermaid
graph LR
    subgraph "NetPulse Core"
        CORE[NetPulse API]
    end
    
    subgraph "Notification Services"
        SENDGRID[SendGrid Email]
        AFRICAS[Africa's Talking SMS]
        SLACK[Slack Webhooks]
        TEAMS[Microsoft Teams]
    end
    
    subgraph "Monitoring Integrations"
        PAGER[PagerDuty]
        OPSGENIE[OpsGenie]
        DATADOG[DataDog]
    end
    
    subgraph "Network Equipment"
        SNMP[SNMP Devices]
        SSH[SSH Monitoring]
        API_DEVICES[API-based Devices]
    end
    
    CORE --> SENDGRID
    CORE --> AFRICAS
    CORE --> SLACK
    CORE --> TEAMS
    
    CORE --> PAGER
    CORE --> OPSGENIE
    CORE --> DATADOG
    
    SNMP --> CORE
    SSH --> CORE
    API_DEVICES --> CORE
```

---

## Future Architecture Considerations

### **Planned Enhancements**

- **Microservices Migration**: Break monolith into smaller services
- **Event Sourcing**: Implement event sourcing for audit and replay
- **CQRS Pattern**: Separate read and write models for better performance
- **API Gateway**: Dedicated API gateway for better routing and security
- **Service Mesh**: Istio/Linkerd for advanced service communication
- **Multi-tenant Architecture**: Support for multiple organizations
- **Machine Learning Pipeline**: Predictive analytics and anomaly detection
- **Mobile-first Design**: Progressive Web App and native mobile apps

### **Technology Evolution**

- **Container Orchestration**: Migration to Kubernetes
- **Serverless Functions**: AWS Lambda/Azure Functions for event processing
- **Edge Computing**: Edge nodes for distributed monitoring
- **Blockchain Integration**: Immutable audit logs using blockchain
- **AI/ML Integration**: Advanced analytics and predictive monitoring

---

<div align="center">

**NetPulse Architecture v1.0**

*Engineered for Scale, Security, and Performance*

[Back to README](./README.md) • [Documentation](./docs) • [Contributing](./CONTRIBUTING.md)

</div>
