# NetPulse Architecture Documentation

<div align="center">

[![Architecture](https://img.shields.io/badge/Architecture-Microservices-blue?style=for-the-badge)](.)
[![Status](https://img.shields.io/badge/Status-v1.0-green?style=for-the-badge)](.)
[![Last Updated](https://img.shields.io/badge/Updated-July%202025-orange?style=for-the-badge)](.)

**Comprehensive System Architecture Guide for NetPulse**

*Real-time Network Operations Center (NOC) Monitoring Platform*

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Component Architecture](#-component-architecture)
- [Data Flow](#-data-flow)
- [Technology Stack](#-technology-stack)
- [Database Design](#-database-design)
- [Security Architecture](#-security-architecture)
- [Deployment Architecture](#-deployment-architecture)
- [Scalability Considerations](#-scalability-considerations)
- [Monitoring & Observability](#-monitoring--observability)

---

## 🏗️ Overview

NetPulse follows a **microservices architecture** with clear separation of concerns, designed for high availability, scalability, and maintainability. The system consists of multiple loosely coupled services that communicate through well-defined APIs and message queues.

### **Architectural Principles**

- **🔄 Microservices**: Loosely coupled, independently deployable services
- **📡 Event-Driven**: Asynchronous communication using message queues
- **🎯 Domain-Driven Design**: Services organized around business capabilities
- **🛡️ Security-First**: Zero-trust security model with comprehensive authentication
- **📊 Observable**: Comprehensive logging, metrics, and tracing
- **🚀 Cloud-Native**: Container-first design for cloud deployment

---

## 🎯 System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Dashboard]
        MOBILE[Mobile App]
        API_CLIENT[API Clients]
    end
    
    subgraph "Load Balancer"
        LB[nginx/CloudFlare]
    end
    
    subgraph "API Gateway"
        GATEWAY[FastAPI Gateway]
    end
    
    subgraph "Core Services"
        AUTH[Authentication Service]
        DEVICE[Device Management]
        MONITOR[Monitoring Service]
        ALERT[Alert Service]
        NOTIFY[Notification Service]
        REPORT[Reporting Service]
    end
    
    subgraph "Data Layer"
        POSTGRES[(PostgreSQL)]
        REDIS[(Redis Cache)]
        TIMESERIES[(TimescaleDB)]
    end
    
    subgraph "Message Queue"
        CELERY[Celery Workers]
        RABBIT[RabbitMQ]
    end
    
    subgraph "External Services"
        SENDGRID[SendGrid]
        AFRICAS[Africa's Talking]
        WEBHOOKS[Webhook Endpoints]
    end
    
    subgraph "Monitoring Stack"
        PROMETHEUS[Prometheus]
        GRAFANA[Grafana]
        JAEGER[Jaeger Tracing]
    end
    
    WEB --> LB
    MOBILE --> LB
    API_CLIENT --> LB
    
    LB --> GATEWAY
    GATEWAY --> AUTH
    GATEWAY --> DEVICE
    GATEWAY --> MONITOR
    GATEWAY --> ALERT
    GATEWAY --> NOTIFY
    GATEWAY --> REPORT
    
    AUTH --> POSTGRES
    DEVICE --> POSTGRES
    MONITOR --> TIMESERIES
    ALERT --> POSTGRES
    NOTIFY --> REDIS
    REPORT --> TIMESERIES
    
    MONITOR --> RABBIT
    ALERT --> RABBIT
    NOTIFY --> RABBIT
    
    RABBIT --> CELERY
    
    CELERY --> SENDGRID
    CELERY --> AFRICAS
    CELERY --> WEBHOOKS
    
    CELERY --> REDIS
    
    PROMETHEUS --> GATEWAY
    PROMETHEUS --> AUTH
    PROMETHEUS --> DEVICE
    PROMETHEUS --> MONITOR
    PROMETHEUS --> ALERT
    PROMETHEUS --> NOTIFY
    PROMETHEUS --> REPORT
    
    GRAFANA --> PROMETHEUS
    JAEGER --> GATEWAY
```

---

## 🧩 Component Architecture

### **Frontend Architecture**

```mermaid
graph TB
    subgraph "React Application"
        ROUTER[React Router]
        COMPONENTS[UI Components]
        HOOKS[Custom Hooks]
        CONTEXT[Context Providers]
    end
    
    subgraph "State Management"
        ZUSTAND[Zustand Store]
        REACT_QUERY[React Query]
    end
    
    subgraph "UI Framework"
        TAILWIND[Tailwind CSS]
        HEADLESS[Headless UI]
        CHARTS[Recharts]
    end
    
    subgraph "Communication"
        AXIOS[Axios HTTP]
        WEBSOCKET[WebSocket Client]
    end
    
    ROUTER --> COMPONENTS
    COMPONENTS --> HOOKS
    HOOKS --> CONTEXT
    
    CONTEXT --> ZUSTAND
    COMPONENTS --> REACT_QUERY
    
    COMPONENTS --> TAILWIND
    COMPONENTS --> HEADLESS
    COMPONENTS --> CHARTS
    
    HOOKS --> AXIOS
    HOOKS --> WEBSOCKET
```

**Key Frontend Components:**

- **Dashboard**: Real-time network overview with live metrics
- **Device Management**: CRUD operations for network devices
- **Alert Console**: Alert management and acknowledgment interface
- **Analytics**: Historical data visualization and reporting
- **Admin Panel**: User management and system configuration

### **Backend Architecture**

```mermaid
graph TB
    subgraph "FastAPI Application"
        MAIN[main.py]
        ROUTER[API Routers]
        MIDDLEWARE[Middleware Stack]
        DEPS[Dependencies]
    end
    
    subgraph "Core Modules"
        AUTH_MOD[Authentication]
        DEVICE_MOD[Device Management]
        MONITOR_MOD[Monitoring]
        ALERT_MOD[Alerting]
        NOTIFY_MOD[Notifications]
    end
    
    subgraph "Data Access Layer"
        MODELS[SQLAlchemy Models]
        SCHEMAS[Pydantic Schemas]
        CRUD[CRUD Operations]
    end
    
    subgraph "Business Logic"
        SERVICES[Service Layer]
        UTILS[Utility Functions]
        VALIDATORS[Data Validators]
    end
    
    MAIN --> ROUTER
    MAIN --> MIDDLEWARE
    ROUTER --> DEPS
    
    ROUTER --> AUTH_MOD
    ROUTER --> DEVICE_MOD
    ROUTER --> MONITOR_MOD
    ROUTER --> ALERT_MOD
    ROUTER --> NOTIFY_MOD
    
    AUTH_MOD --> SERVICES
    DEVICE_MOD --> SERVICES
    MONITOR_MOD --> SERVICES
    ALERT_MOD --> SERVICES
    NOTIFY_MOD --> SERVICES
    
    SERVICES --> CRUD
    CRUD --> MODELS
    CRUD --> SCHEMAS
    
    SERVICES --> UTILS
    SERVICES --> VALIDATORS
```

---

## 🔄 Data Flow

### **Real-time Monitoring Flow**

```mermaid
sequenceDiagram
    participant Device as Network Device
    participant Collector as Metric Collector
    participant Queue as Message Queue
    participant Worker as Celery Worker
    participant DB as TimescaleDB
    participant WS as WebSocket
    participant Client as Frontend
    
    Device->>Collector: SNMP/SSH Metrics
    Collector->>Queue: Queue Metric Data
    Queue->>Worker: Process Metrics
    Worker->>DB: Store Time-series Data
    Worker->>WS: Broadcast Real-time Updates
    WS->>Client: Live Dashboard Updates
    
    Note over Worker,DB: Anomaly Detection
    Worker->>Worker: Analyze Thresholds
    Worker->>Queue: Trigger Alerts
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

---

## 🗄️ Database Design

### **PostgreSQL Schema**

```sql
-- Core Tables
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    ip_address INET NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    location VARCHAR(255),
    status VARCHAR(20) DEFAULT 'unknown',
    last_seen TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id UUID REFERENCES devices(id),
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    acknowledged BOOLEAN DEFAULT false,
    acknowledged_by UUID REFERENCES users(id),
    acknowledged_at TIMESTAMP,
    resolved BOOLEAN DEFAULT false,
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Time-series data using TimescaleDB
CREATE TABLE device_metrics (
    time TIMESTAMPTZ NOT NULL,
    device_id UUID REFERENCES devices(id),
    metric_type VARCHAR(50) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20),
    PRIMARY KEY (time, device_id, metric_type)
);

-- Convert to hypertable for time-series optimization
SELECT create_hypertable('device_metrics', 'time');

-- Create indexes for performance
CREATE INDEX idx_device_metrics_device_time ON device_metrics (device_id, time DESC);
CREATE INDEX idx_devices_organization ON devices (organization_id);
CREATE INDEX idx_alerts_device_severity ON alerts (device_id, severity);
```

### **Redis Cache Structure**

```yaml
# User sessions
session:{session_id}: {user_data}

# Real-time metrics cache
metrics:{device_id}:latest: {latest_metrics}
metrics:{device_id}:history: {time_series_data}

# Alert counters
alerts:count:{organization_id}: {alert_count}
alerts:critical:{organization_id}: {critical_alerts}

# Device status cache
device:status:{device_id}: {current_status}
device:health:{device_id}: {health_score}

# Rate limiting
rate_limit:{user_id}:{endpoint}: {request_count}

# Background task results
celery-task-meta-{task_id}: {task_result}
```

---

## 🛡️ Security Architecture

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

## 🚀 Deployment Architecture

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

## 📈 Scalability Considerations

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

## 📊 Monitoring & Observability

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

## 🔄 Data Backup & Recovery

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

## 📚 Integration Architecture

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

## 🔮 Future Architecture Considerations

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

[🏠 Back to README](./README.md) • [📚 Documentation](./docs) • [🤝 Contributing](./CONTRIBUTING.md)

</div>
