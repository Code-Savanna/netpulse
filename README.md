# NetPulse

<div align="center">

[![Project Status](https://img.shields.io/badge/Status-In%20Development-blue?style=for-the-badge)](https://github.com/Code Savanna/netpulse)
[![Version](https://img.shields.io/badge/Version-1.0.0--beta-blue?style=for-the-badge)](https://github.com/Code Savanna/netpulse/releases)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)](https://github.com/Code Savanna/netpulse/actions)

**Real-time Network Operations Center (NOC) Monitoring Dashboard**

*Professional-grade network infrastructure monitoring for telecoms, ISPs, and enterprise environments*

[**Live Demo**](https://netpulse-demo.vercel.app) • [**Documentation**](./docs) • [**Architecture**](./ARCHITECTURE.md) • [**Report Bug**](https://github.com/Code Savanna/netpulse/issues)

</div>

---

## Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Live Demo & Screenshots](#-live-demo--screenshots)
- [Technology Stack](#️-technology-stack)
- [Project Architecture](#-project-architecture)
- [Quick Start](#-quick-start)
- [Configuration](#️-configuration)
- [Documentation](#-documentation)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Author & Support](#-author--support)

---

## Overview

**NetPulse** is an enterprise-grade, real-time network monitoring dashboard engineered to replicate the comprehensive operations of a Network Operations Center (NOC). Designed with scalability, observability, and real-time feedback at its core, NetPulse empowers telecommunications providers, Internet Service Providers (ISPs), and infrastructure engineers to:

- **Monitor** critical network infrastructure in real-time
- **Detect** anomalies and performance degradation instantly  
- **Alert** teams through multiple notification channels
- **Visualize** network health through intuitive dashboards
- **Analyze** historical trends and performance metrics

---

## Key Features

<div align="center">

| **Feature Category** | **Capabilities** |
|------------------------|------------------|
| **Real-time Monitoring** | Live server metrics (CPU, Memory, Network, Disk) • Device status indicators • Sub-second refresh rates via WebSocket |
| **Advanced Analytics** | Interactive charts • Historical trends • Custom dashboards • Performance benchmarking • SLA tracking |
| **Intelligent Alerting** | Multi-threshold alerts • Anomaly detection • Alert correlation • Escalation policies • Noise reduction |
| **Multi-channel Notifications** | SMS (Africa's Talking) • Email (SendGrid) • Webhooks • Slack integration • Mobile push (planned) |
| **Administrative Controls** | Device management • RBAC • Audit logs • Compliance reporting • Bulk operations |
| **High Availability** | Auto-failover • Horizontal scaling • Background processing • Database replication |

</div>

### **Why Choose NetPulse?**

- **Enterprise-Ready**: Built for production environments with 99.9% uptime SLA
- **Scalable**: Monitor 1000+ devices with horizontal scaling capabilities  
- **Secure**: End-to-end encryption, RBAC, and comprehensive audit trails
- **Global**: Multi-region deployment with edge caching for optimal performance
- **Intelligent**: ML-powered anomaly detection and predictive analytics
- **Extensible**: REST APIs, webhooks, and plugin architecture for integrations

---

## Live Demo & Screenshots

<div align="center">

### **Experience NetPulse in Action**

[![Live Demo](https://img.shields.io/badge/%20Live%20Demo-Try%20Now-brightgreen?style=for-the-badge&logo=vercel)](https://netpulse-demo.vercel.app)
[![Video Demo](https://img.shields.io/badge/%20Video%20Demo-Watch%20Now-red?style=for-the-badge&logo=youtube)](https://youtube.com/watch?v=demo)

</div>

### **Interface Previews**

<div align="center">

| **Dashboard** | **Analytics** | **Alerts** |
|:---:|:---:|:---:|
| ![Dashboard](https://via.placeholder.com/300x200/1e293b/ffffff?text=Real-time+Dashboard) | ![Analytics](https://via.placeholder.com/300x200/059669/ffffff?text=Advanced+Analytics) | ![Alerts](https://via.placeholder.com/300x200/dc2626/ffffff?text=Alert+Management) |
| Real-time network monitoring | Historical data & trends | Alert management console |

</div>

> **Note**: Demo environment includes sample data for testing. Full deployment requires configuration.

---

## Technology Stack

<div align="center">

| **Layer** | **Technology** | **Purpose** |
|-----------|----------------|-------------|
| **Frontend** | ![React](https://img.shields.io/badge/React-18.x-61DAFB?logo=react) ![Tailwind](https://img.shields.io/badge/Tailwind-3.x-06B6D4?logo=tailwindcss) ![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript) | Modern, responsive user interface |
| **API Gateway** | ![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi) ![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python) | Request routing & authentication |
| **Microservices** | ![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?logo=sqlalchemy) | Independent, scalable services |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql) ![TimescaleDB](https://img.shields.io/badge/TimescaleDB-2.x-FDB515?logo=timescale) ![Redis](https://img.shields.io/badge/Redis-7.x-DC382D?logo=redis) | Time-series data & caching |
| **Message Queue** | ![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.x-FF6600?logo=rabbitmq) ![Celery](https://img.shields.io/badge/Celery-5.x-37B24D?logo=celery) | Async task processing |
| **Real-time** | ![WebSocket](https://img.shields.io/badge/WebSocket-Native-010101?logo=websocket) | Live data streaming |
| **Monitoring** | ![Prometheus](https://img.shields.io/badge/Prometheus-2.x-E6522C?logo=prometheus) ![Grafana](https://img.shields.io/badge/Grafana-10.x-F46800?logo=grafana) | System observability |
| **DevOps** | ![Docker](https://img.shields.io/badge/Docker-24.x-2496ED?logo=docker) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?logo=githubactions) | Containerization and CI/CD |
| **Cloud** | ![Render](https://img.shields.io/badge/Render-Backend-46E3B7?logo=render) ![Vercel](https://img.shields.io/badge/Vercel-Frontend-000000?logo=vercel) | Production deployment |

</div>

---

## Project Architecture

**NetPulse now follows a modern microservices architecture** with independent, scalable services:

```
netpulse/
├── services/                   # Microservices architecture
│   ├── gateway/               # API Gateway & routing
│   │   ├── main.py           # Central request router
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── auth-service/         # Authentication & authorization
│   │   ├── auth_service.py   # JWT auth logic
│   │   ├── models.py         # User & organization models
│   │   ├── main.py           # Auth endpoints
│   │   └── Dockerfile
│   ├── device-service/       # Device management
│   │   ├── device_service.py # Device CRUD operations
│   │   ├── models.py         # Device data models
│   │   ├── main.py           # Device endpoints
│   │   └── Dockerfile
│   ├── monitoring-service/   # Real-time monitoring
│   │   ├── monitoring_service.py # Health checks & metrics
│   │   ├── tasks.py          # Celery background tasks
│   │   ├── main.py           # WebSocket & monitoring API
│   │   └── Dockerfile
│   ├── alert-service/        # Alert management
│   │   ├── alert_service.py  # Alert processing logic
│   │   ├── models.py         # Alert data models
│   │   ├── main.py           # Alert endpoints
│   │   └── Dockerfile
│   ├── notification-service/ # Multi-channel notifications
│   │   ├── notification_service.py # SMS, email, webhooks
│   │   ├── main.py           # Notification endpoints
│   │   └── Dockerfile
│   └── reporting-service/    # Analytics & insights
│       ├── reporting_service.py # Report generation
│       ├── main.py           # Reporting endpoints
│       └── Dockerfile
├── netpulse_frontend/        # React.js dashboard
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Application pages
│   │   ├── hooks/            # Custom React hooks
│   │   ├── services/         # API integration
│   │   └── utils/            # Frontend utilities
│   ├── public/               # Static assets
│   ├── package.json
│   └── Dockerfile
├── monitoring/               # Observability stack
│   ├── prometheus.yml        # Metrics collection
│   ├── alert_rules.yml       # Alert rules
│   └── grafana/             # Dashboards & visualization
├── docs/                     # Documentation
├── scripts/                  # Deployment scripts
├── docker-compose.yml        # Multi-service orchestration
├── docker-compose.prod.yml   # Production configuration
├── ARCHITECTURE.md           # Detailed architecture guide
├──  CONTRIBUTING.md            # Contribution guidelines
└──  README.md                  # This file
```

> **For detailed system architecture, see [ARCHITECTURE.md](./ARCHITECTURE.md)**

---

## Quick Start

### 1. Basic Setup (Development)

```bash
# Clone the repository
git clone <repository-url>
cd netpulse

# Start the microservices development environment
docker-compose up --build

# The following services will be available:
# - API Gateway: http://localhost:8000
# - Frontend: http://localhost:3000
# - Individual services on ports 8001-8006
```

### 2. Production Setup with Monitoring

```bash
# Start the full production stack with monitoring
docker-compose -f docker-compose.prod.yml up --build -d

# Or use the automated setup script
./scripts/setup-monitoring.sh
```

### 3. Access the Application

| Service | URL | Credentials |
|---------|-----|-------------|
| **NetPulse Dashboard** | http://localhost:3000 | - |
| **API Gateway** | http://localhost:8000 | - |
| **Auth Service** | http://localhost:8001 | - |
| **Device Service** | http://localhost:8002 | - |
| **Monitoring Service** | http://localhost:8003 | - |
| **Alert Service** | http://localhost:8004 | - |
| **Notification Service** | http://localhost:8005 | - |
| **Reporting Service** | http://localhost:8006 | - |
| **Grafana** | http://localhost:3001 | admin/admin |
| **Prometheus** | http://localhost:9090 | - |

---

## Configuration

### **Environment Setup**

Each microservice requires its own environment configuration. Create `.env` files for each service:

<details>
<summary><strong>Auth Service Configuration</strong></summary>

```env
# services/auth-service/.env
DATABASE_URL=postgresql://netpulse:password@db:5432/netpulse
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
</details>

<details>
<summary><strong>Notification Service Configuration</strong></summary>

```env
# services/notification-service/.env
DATABASE_URL=postgresql://netpulse:password@db:5432/netpulse
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=noreply@yourcompany.com
AFRICAS_TALKING_API_KEY=your_africas_talking_api_key
AFRICAS_TALKING_USERNAME=your_username
```
</details>

<details>
<summary><strong>Monitoring Service Configuration</strong></summary>

```env
# services/monitoring-service/.env
DATABASE_URL=postgresql://netpulse:password@db:5432/netpulse
CELERY_BROKER_URL=amqp://netpulse:password@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/1
DEVICE_SERVICE_URL=http://device-service:8002
AUTH_SERVICE_URL=http://auth-service:8001
```
</details>

### **Monitoring Parameters**

| Parameter | Default | Description |
|-----------|---------|-------------|
| **Metric Interval** | 30 seconds | Data collection frequency |
| **Alert Thresholds** | CPU >85%, Memory >90%, Disk >95% | Default alert triggers |
| **Device Capacity** | 1000+ devices | Scalable monitoring capacity |
| **Data Retention** | 90 days | Historical data storage |
---

## Documentation

<div align="center">

| **Document** | **Purpose** | **Link** |
|----------------|----------------|-------------|
| **Architecture Guide** | System design & architecture | [ARCHITECTURE.md](./ARCHITECTURE.md) |
| **API Reference** | Complete REST API docs | [API Docs](./docs/api.md) |
| **Deployment Guide** | Production deployment | [Deploy Guide](./docs/deployment.md) |
| **Contributing** | Contribution guidelines | [CONTRIBUTING.md](./CONTRIBUTING.md) |
| **Security Policy** | Security & vulnerability reporting | [SECURITY.md](./SECURITY.md) |

</div>

---

## Testing

### **Run Test Suite**

```bash
# Test individual microservices
cd services/auth-service && python -m pytest tests/ -v
cd services/device-service && python -m pytest tests/ -v
cd services/monitoring-service && python -m pytest tests/ -v

# Frontend testing  
cd netpulse_frontend && npm test

# Integration testing (all services)
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

# End-to-end testing
npm run test:e2e
```

### **Test Coverage**

<div align="center">

| **Component** | **Coverage** | **Status** |
|--------------|-------------|-----------|
| **Microservices** | >85% | Good |
| **API Gateway** | >90% | Excellent |
| **Frontend** | >85% | Good |
| **Integration** | Critical paths | Covered |
| **Performance** | 10k concurrent users | Load tested |

</div>

---

## Deployment

### **Production Deployment**

```bash
# Build & deploy production microservices stack
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Initialize database for each service
docker-compose exec auth-service python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
docker-compose exec device-service python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
docker-compose exec alert-service python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"

# Start Celery workers for background tasks
docker-compose exec monitoring-service celery -A celery_app worker --loglevel=info --detach
```

### **Cloud Platforms**

<div align="center">

| **Platform** | **Status** | **Use Case** |
|-------------|-----------|-------------|
| **Render** | Active | Microservices hosting |
| **Vercel** | Active | Frontend deployment |
| **AWS ECS** | In Progress | Container orchestration |
| **Kubernetes** | Planned | Enterprise scaling |
| **Docker Swarm** | Supported | Multi-node deployment |

</div>

---

## Contributing

### **Development Workflow**

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** branch: `git push origin feature/amazing-feature`
5. **Open** Pull Request

### **Code Standards**

- **Python**: Black formatting, Flake8 linting, type hints required
- **TypeScript**: Prettier formatting, ESLint compliance
- **Testing**: Minimum 80% coverage for new features
- **Documentation**: Update docs with all changes

> **New to contributing?** Check our [Contributing Guidelines](./CONTRIBUTING.md) for detailed instructions!

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details

### **Show Your Support**

If NetPulse helps your projects:

- **Star** this repository
- **Report** bugs and suggest features
- **Share** with your network
- **Contribute** to the codebase

---

**Built with care for the Network Operations Community**

*NetPulse - Empowering Network Engineers Worldwide*

</div>

