
# NetPulse 🌐

<div align="center">

[![Project Status](https://img.shie<div align="center">

| **Layer** | **Technology** | **Purpose** |
|-----------|----------------|-------------|
| **Frontend** | ![React](https://img.shields.io/badge/React-18.x-61DAFB?logo=react) ![Tailwind](https://img.shields.io/badge/Tailwind-3.x-06B6D4?logo=tailwindcss) ![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript) | Modern, responsive user interface |
| **Backend** | ![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi) ![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?logo=sqlalchemy) | High-performance API and ORM |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql) ![Redis](https://img.shields.io/badge/Redis-7.x-DC382D?logo=redis) | Primary database and caching |
| **Real-time** | ![WebSocket](https://img.shields.io/badge/WebSocket-Native-010101?logo=websocket) | Live data streaming |
| **Task Queue** | ![Celery](https://img.shields.io/badge/Celery-5.x-37B24D?logo=celery) | Background job processing |
| **Monitoring** | ![Prometheus](https://img.shields.io/badge/Prometheus-2.x-E6522C?logo=prometheus) ![Grafana](https://img.shields.io/badge/Grafana-10.x-F46800?logo=grafana) | System observability |
| **DevOps** | ![Docker](https://img.shields.io/badge/Docker-24.x-2496ED?logo=docker) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?logo=githubactions) | Containerization and CI/CD |
| **Cloud** | ![Render](https://img.shields.io/badge/Render-Backend-46E3B7?logo=render) ![Vercel](https://img.shields.io/badge/Vercel-Frontend-000000?logo=vercel) | Production deployment |

</div>dge/Status-In%20Development-orange?style=for-the-badge)](https://github.com/yourusername/netpulse)
[![Version](https://img.shields.io/badge/Version-1.0.0--beta-blue?style=for-the-badge)](https://github.com/yourusername/netpulse/releases)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)](https://github.com/yourusername/netpulse/actions)

**Real-time Network Operations Center (NOC) Monitoring Dashboard**

*Professional-grade network infrastructure monitoring for telecoms, ISPs, and enterprise environments*

[🚀 **Live Demo**](https://netpulse-demo.vercel.app) • [📖 **Documentation**](./docs) • [🏗️ **Architecture**](./ARCHITECTURE.md) • [🐛 **Report Bug**](https://github.com/yourusername/netpulse/issues)

</div>

---

## 📋 Overview

**NetPulse** is an enterprise-grade, real-time network monitoring dashboard engineered to replicate the comprehensive operations of a Network Operations Center (NOC). Designed with scalability, observability, and real-time feedback at its core, NetPulse empowers telecommunications providers, Internet Service Providers (ISPs), and infrastructure engineers to:

- **Monitor** critical network infrastructure in real-time
- **Detect** anomalies and performance degradation instantly  
- **Alert** teams through multiple notification channels
- **Visualize** network health through intuitive dashboards
- **Analyze** historical trends and performance metrics

---

## ✨ Key Features

### 🔍 **Real-time Monitoring**
- Live server metrics simulation (CPU, Memory, Network I/O, Disk Usage)
- Real-time device status indicators with health scoring
- Sub-second data refresh rates via WebSocket connections

### 📊 **Advanced Analytics**
- Interactive graphs and charts powered by Recharts
- Historical trend analysis and predictive insights
- Custom dashboards with drag-and-drop widgets
- Performance benchmarking and SLA tracking

### 🚨 **Intelligent Alerting**
- Multi-threshold alerting system with escalation policies
- Anomaly detection using statistical analysis
- Alert correlation and noise reduction
- Customizable notification rules and schedules

### 📱 **Multi-channel Notifications**
- SMS alerts via **Africa's Talking API**
- Email notifications through **SendGrid**
- Webhook integrations for third-party systems
- Mobile push notifications (planned)

### 🛠️ **Administrative Controls**
- Comprehensive admin panel for device management
- User role-based access control (RBAC)
- Audit logs and compliance reporting
- Bulk device import/export functionality

### 🔄 **High Availability**
- Fault-tolerant architecture with automatic failover
- Horizontal scaling support
- Background task processing with Celery
- Database replication and backup strategies

---

## 🏗️ Technology Stack

| Layer           | Technology               |
|----------------|--------------------------|
| Frontend        | React.js, Tailwind CSS, Recharts |
| Backend         | FastAPI (Python), SQLAlchemy, PostgreSQL |
| Realtime Engine | WebSocket (FastAPI native) |
| Task Queue      | Celery + Redis           |
| Notifications   | Africa’s Talking API (SMS), SendGrid (Email) |
| DevOps          | Docker + Docker Compose, GitHub Actions (CI/CD) |
| Deployment      | Render (Backend), Vercel (Frontend) |

---

## 📁 Project Architecture

```
netpulse/
├── 📂 netpulse_backend/          # FastAPI backend services
│   ├── 📂 app/
│   │   ├── 📂 api/               # REST API endpoints
│   │   ├── 📂 core/              # Configuration and security
│   │   ├── 📂 models/            # Database models
│   │   ├── 📂 services/          # Business logic
│   │   └── 📂 utils/             # Helper functions
│   ├── 📂 tests/                 # Backend test suite
│   ├── 📂 alembic/               # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
├── 📂 netpulse_frontend/         # React.js dashboard
│   ├── 📂 src/
│   │   ├── 📂 components/        # Reusable UI components
│   │   ├── 📂 pages/             # Application pages
│   │   ├── 📂 hooks/             # Custom React hooks
│   │   ├── 📂 services/          # API integration
│   │   └── 📂 utils/             # Frontend utilities
│   ├── 📂 public/                # Static assets
│   ├── package.json
│   └── Dockerfile
├── 📂 docs/                      # Documentation
├── 📂 scripts/                   # Deployment scripts
├── 📄 docker-compose.yml         # Multi-service orchestration
├── 📄 docker-compose.prod.yml    # Production configuration
├── 📄 ARCHITECTURE.md            # Detailed architecture guide
├── 📄 CONTRIBUTING.md            # Contribution guidelines
└── 📄 README.md                  # This file
```

> 📋 **For detailed system architecture, see [ARCHITECTURE.md](./ARCHITECTURE.md)**

---

## 🚀 Quick Start

### 📋 **Prerequisites**

Before getting started, ensure you have the following installed:

- **Docker** (v24.0 or higher) & **Docker Compose**
- **Git** for version control
- **Node.js** (v18.0 or higher) - for local development
- **Python** (v3.11 or higher) - for local development

### 🔧 **Installation Steps**

#### **Option 1: Docker Deployment (Recommended)**

```bash
# Clone the repository
git clone https://github.com/yourusername/netpulse.git
cd netpulse

# Start all services with Docker Compose
docker-compose up --build -d

# Verify all services are running
docker-compose ps
```

#### **Option 2: Local Development Setup**

```bash
# Clone and navigate to the project
git clone https://github.com/yourusername/netpulse.git
cd netpulse

# Backend setup
cd netpulse_backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup (in a new terminal)
cd netpulse_frontend
npm install
npm start
```

### 🌐 **Access Points**

Once deployed, access the application at:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend Dashboard** | [http://localhost:3000](http://localhost:3000) | Main monitoring interface |
| **Backend API** | [http://localhost:8000](http://localhost:8000) | REST API endpoints |
| **API Documentation** | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive Swagger UI |
| **Admin Panel** | [http://localhost:3000/admin](http://localhost:3000/admin) | Administrative interface |
| **Grafana** | [http://localhost:3001](http://localhost:3001) | System metrics dashboard |

### 🔍 **Health Checks**

Verify system health with these endpoints:

```bash
# Backend health check
curl http://localhost:8000/health

# Database connectivity
curl http://localhost:8000/health/db

# Redis connectivity  
curl http://localhost:8000/health/redis
```

---

## ⚙️ Configuration

### 📊 **Monitoring Configuration**

The system supports configurable monitoring parameters:

- **Metric Collection Interval**: 30 seconds (configurable)
- **Alert Thresholds**: CPU >85%, Memory >90%, Disk >95%
- **Device Simulation**: Up to 1000+ virtual network devices
- **Data Retention**: 90 days default (configurable)

### 🔧 **Environment Variables**

Create a `.env` file in the backend directory:

```env
# Database Configuration
DATABASE_URL=postgresql://netpulse:password@localhost:5432/netpulse
REDIS_URL=redis://localhost:6379/0

# API Keys
AFRICAS_TALKING_API_KEY=your_africas_talking_api_key
AFRICAS_TALKING_USERNAME=your_username
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=noreply@yourcompany.com

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Monitoring
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true
LOG_LEVEL=INFO

# Feature Flags
ENABLE_SMS_ALERTS=true
ENABLE_EMAIL_ALERTS=true
ENABLE_WEBHOOK_ALERTS=true
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Architecture Guide](./ARCHITECTURE.md) | Detailed system architecture and design decisions |
| [API Reference](./docs/api.md) | Complete REST API documentation |
| [Deployment Guide](./docs/deployment.md) | Production deployment instructions |
| [Contributing Guidelines](./CONTRIBUTING.md) | How to contribute to the project |
| [Security Policy](./SECURITY.md) | Security practices and vulnerability reporting |

---

## 🧪 Testing

### **Run Test Suite**

```bash
# Backend tests
cd netpulse_backend
python -m pytest tests/ -v --cov=app

# Frontend tests
cd netpulse_frontend
npm test

# End-to-end tests
npm run test:e2e
```

### **Test Coverage**

- **Backend**: >90% code coverage
- **Frontend**: >85% code coverage
- **Integration Tests**: Critical user journeys
- **Performance Tests**: Load testing up to 10k concurrent users

---

## 🚀 Deployment

### **Production Deployment**

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# Run database migrations
docker-compose exec backend alembic upgrade head
```

### **Cloud Platforms**

| Platform | Status | Configuration |
|----------|---------|---------------|
| **Render** | ✅ Supported | Backend API deployment |
| **Vercel** | ✅ Supported | Frontend static hosting |
| **AWS ECS** | 🔄 In Progress | Container orchestration |
| **Kubernetes** | 📋 Planned | Helm charts available |

---

## 🤝 Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](./CONTRIBUTING.md) for details.

### **Development Workflow**

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### **Code Standards**

- **Python**: Black formatting, Flake8 linting, Type hints required
- **JavaScript/TypeScript**: Prettier formatting, ESLint rules
- **Testing**: Minimum 80% test coverage for new features
- **Documentation**: Update relevant docs with changes

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author & Team

<div align="center">

**Dabwitso Mweemba**  
*Co-founder & Lead Developer*  
[Code Savanna](https://codesavanna.org) & [Learniva AI](https://learniva.ai)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/dabwitso-mweemba)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dabwitso)
[![Website](https://img.shields.io/badge/Website-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://codesavanna.org)

📍 **Lusaka, Zambia** 🇿🇲

</div>

---

## ⭐ Support

If you find NetPulse helpful, please consider:

- ⭐ **Starring** the repository
- 🐛 **Reporting bugs** and suggesting features
- 📢 **Sharing** with your network
- 💝 **Contributing** to the codebase

---

<div align="center">

**Built with ❤️ for the Network Operations Community**

*NetPulse - Empowering Network Engineers Worldwide*

</div>
