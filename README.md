# NetPulse

[![Project Status](https://img.shields.io/badge/Status-In%20Development-blue?style=flat-square)](https://github.com/Code-Savanna/netpulse)
[![Version](https://img.shields.io/badge/Version-1.0.0--beta-blue?style=flat-square)](https://github.com/Code-Savanna/netpulse/releases)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=flat-square)](https://github.com/Code-Savanna/netpulse/actions)

NetPulse is an enterprise-grade, real-time network monitoring dashboard for Network Operations Centers (NOCs). It provides comprehensive infrastructure monitoring for telecommunications providers, ISPs, and enterprise environments.

## Quick Links

- [Live Demo](https://netpulse-demo.vercel.app)
- [Documentation](./docs)
- [Architecture Guide](./ARCHITECTURE.md)
- [Report Issues](https://github.com/Code-Savanna/netpulse/issues)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [Testing](#testing)
- [Deployment](#deployment)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Overview

NetPulse empowers network operations teams with real-time monitoring capabilities designed for enterprise environments. The platform provides comprehensive visibility into network infrastructure health and performance.

### Key Capabilities

- **Real-time Monitoring**: Live server metrics with sub-second refresh rates via WebSocket
- **Intelligent Alerting**: Multi-threshold alerts with anomaly detection and escalation policies
- **Multi-channel Notifications**: SMS, email, webhooks, and Slack integration
- **Advanced Analytics**: Interactive charts, historical trends, and performance benchmarking
- **Enterprise Security**: End-to-end encryption, RBAC, and comprehensive audit trails
- **Horizontal Scaling**: Monitor 1000+ devices with auto-failover capabilities

### Why NetPulse?

- **Production Ready**: Built for 99.9% uptime SLA requirements
- **Microservices Architecture**: Independent, scalable services for enterprise deployment
- **ML-Powered**: Anomaly detection and predictive analytics
- **API-First**: REST APIs, webhooks, and plugin architecture for integrations
## Features

### Core Monitoring Capabilities

| Feature | Description |
|---------|-------------|
| **Real-time Monitoring** | Live server metrics (CPU, Memory, Network, Disk) with sub-second refresh rates |
| **Device Management** | Comprehensive device inventory with status tracking and bulk operations |
| **Alert Management** | Multi-threshold alerts with anomaly detection and escalation policies |
| **Notification System** | SMS, email, webhooks, and Slack integration with delivery confirmation |
| **Analytics Dashboard** | Interactive charts, historical trends, and performance benchmarking |
| **Access Control** | Role-based access control (RBAC) with comprehensive audit trails |

### Technical Highlights

- **Microservices Architecture**: 7 independent services for optimal scalability
- **High Availability**: Auto-failover with horizontal scaling capabilities
- **Time-series Database**: TimescaleDB for efficient metric storage and analysis
- **Message Queue**: RabbitMQ with Celery for reliable background processing
- **Distributed Tracing**: Jaeger integration for microservices observability

## Getting Started

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum (8GB recommended)
- 2 CPU cores minimum

### Quick Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Code-Savanna/netpulse.git
   cd netpulse
   ```

2. **Start development environment**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Dashboard: http://localhost:3000
   - API Gateway: http://localhost:8000
   - Grafana: http://localhost:3001 (admin/admin)

### Production Deployment

For production environments, use the production configuration:

```bash
# Start production stack
docker-compose -f docker-compose.prod.yml up --build -d

# Initialize databases
./scripts/init-production-db.sh

# Start monitoring stack
./scripts/setup-monitoring.sh
```

## Architecture

NetPulse implements a microservices architecture with the following components:

### Service Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   API Gateway   │    │  Microservices  │
│      nginx      │───▶│   Port 8000     │───▶│  Ports 8001-6   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
          │                       │                       │
          ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Database      │    │ Message Queue   │
│   React App     │    │   PostgreSQL    │    │   RabbitMQ      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Project Structure

```
netpulse/
├── services/                 # Microservices
│   ├── gateway/             # API Gateway & routing
│   ├── auth-service/        # Authentication & authorization
│   ├── device-service/      # Device management
│   ├── monitoring-service/  # Real-time monitoring
│   ├── alert-service/       # Alert management
│   ├── notification-service/# Multi-channel notifications
│   └── reporting-service/   # Analytics & insights
├── netpulse_frontend/       # React.js dashboard
├── monitoring/              # Observability stack
├── docs/                    # Documentation
└── scripts/                 # Deployment scripts
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | React 18, TypeScript, Tailwind CSS | User interface |
| **API Gateway** | FastAPI, Python 3.11 | Request routing |
| **Microservices** | FastAPI, SQLAlchemy | Business logic |
| **Database** | PostgreSQL 15, TimescaleDB, Redis | Data storage |
| **Message Queue** | RabbitMQ, Celery | Async processing |
| **Monitoring** | Prometheus, Grafana, Jaeger | Observability |
| **Deployment** | Docker, Docker Compose | Containerization |

For detailed architecture information, see [ARCHITECTURE.md](./ARCHITECTURE.md).

## Configuration

### Environment Variables

Each microservice requires environment configuration. Create `.env` files for each service:

#### Auth Service
```env
# services/auth-service/.env
DATABASE_URL=postgresql://netpulse:password@db:5432/netpulse
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Notification Service
```env
# services/notification-service/.env
DATABASE_URL=postgresql://netpulse:password@db:5432/netpulse
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=noreply@yourcompany.com
AFRICAS_TALKING_API_KEY=your_africas_talking_api_key
AFRICAS_TALKING_USERNAME=your_username
```

#### Monitoring Service
```env
# services/monitoring-service/.env
DATABASE_URL=postgresql://netpulse:password@db:5432/netpulse
CELERY_BROKER_URL=amqp://netpulse:password@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/1
DEVICE_SERVICE_URL=http://device-service:8002
AUTH_SERVICE_URL=http://auth-service:8001
```

### Default Parameters

| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| Metric Interval | 30 seconds | Data collection frequency |
| Alert Thresholds | CPU >85%, Memory >90%, Disk >95% | Default alert triggers |
| Device Capacity | 1000+ devices | Scalable monitoring capacity |
| Data Retention | 90 days | Historical data storage |

## Testing

### Running Tests

Test individual microservices:
```bash
cd services/auth-service && python -m pytest tests/ -v
cd services/device-service && python -m pytest tests/ -v
cd services/monitoring-service && python -m pytest tests/ -v
```

Test frontend components:
```bash
cd netpulse_frontend && npm test
```

Run integration tests:
```bash
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

### Test Coverage

| Component | Coverage | Status |
|-----------|----------|--------|
| Microservices | >85% |  Good |
| API Gateway | >90% |  Excellent |
| Frontend | >85% |  Good |
| Integration | Critical paths |  Covered |
| Performance | 10k concurrent users |  Load tested |

## Deployment

### Production Deployment

1. **Build and deploy services**
   ```bash
   docker-compose -f docker-compose.prod.yml build
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Initialize databases**
   ```bash
   docker-compose exec auth-service python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
   docker-compose exec device-service python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
   docker-compose exec alert-service python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
   ```

3. **Start background workers**
   ```bash
   docker-compose exec monitoring-service celery -A celery_app worker --loglevel=info --detach
   ```

### Cloud Platforms

| Platform | Status | Use Case |
|----------|--------|----------|
| Render |  Active | Microservices hosting |
| Vercel |  Active | Frontend deployment |
| AWS ECS |  In Progress | Container orchestration |
| Kubernetes |  Planned | Enterprise scaling |
| Docker Swarm |  Supported | Multi-node deployment |

## Documentation

| Document | Description |
|----------|-------------|
| [Architecture Guide](./ARCHITECTURE.md) | System design and microservices architecture |
| [API Reference](./docs/api.md) | Complete REST API documentation |
| [Deployment Guide](./docs/deployment.md) | Production deployment procedures |
| [Monitoring Guide](./docs/monitoring.md) | Observability and alerting setup |
| [Contributing Guidelines](./CONTRIBUTING.md) | Development workflow and standards |
| [Security Policy](./SECURITY.md) | Security practices and vulnerability reporting |

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and add tests
4. Ensure all tests pass: `npm test` and `python -m pytest`
5. Follow code formatting standards (Black for Python, Prettier for TypeScript)
6. Commit your changes: `git commit -m 'Add new feature'`
7. Push to your branch: `git push origin feature/your-feature`
8. Open a Pull Request

### Code Standards

- **Python**: Black formatting, Flake8 linting, type hints required
- **TypeScript**: Prettier formatting, ESLint compliance
- **Testing**: Minimum 80% coverage for new features
- **Documentation**: Update relevant docs with changes

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Support

-  **Documentation**: Check our [documentation](./docs) for detailed guides
-  **Bug Reports**: [Create an issue](https://github.com/Code-Savanna/netpulse/issues)
-  **Feature Requests**: [Start a discussion](https://github.com/Code-Savanna/netpulse/discussions)
-  **Community**: Join our discussions for help and collaboration

---

The Network Operations Community by [Code Savanna](https://github.com/Code-Savanna)

</div>

