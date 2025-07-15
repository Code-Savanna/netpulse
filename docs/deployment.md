# NetPulse Deployment Guide

This guide provides comprehensive instructions for deploying NetPulse's microservices architecture to production environments.

## Prerequisites

- Docker and Docker Compose v2.0+
- A registered domain name
- A server with at least 4GB RAM and 2 CPU cores
- PostgreSQL 15+ and Redis 7+ (if using external databases)
- SSL certificates for HTTPS

## Architecture Overview

NetPulse uses a microservices architecture with the following components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   API Gateway   │    │  Microservices  │
│    (nginx)      │───▶│   (Port 8000)   │───▶│  (Ports 8001-6) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
          │                       │                       │
          │                       │                       │
          ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Frontend    │    │    Database     │    │  Message Queue  │
│   React App     │    │   PostgreSQL    │    │    RabbitMQ     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Development Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/dabwitso/netpulse.git
cd netpulse
```

### 2. Configure Environment Variables

Create environment files for each service:

#### **Database Configuration (shared)**
```bash
# Create shared database config
cat > .env.shared << EOF
DATABASE_URL=postgresql://netpulse:password@db:5432/netpulse
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=amqp://netpulse:password@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/1
EOF
```

#### **Auth Service Configuration**
```bash
mkdir -p services/auth-service
cat > services/auth-service/.env << EOF
DATABASE_URL=postgresql://netpulse:password@db:5432/netpulse
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF
```

#### **Notification Service Configuration**
```bash
mkdir -p services/notification-service
cat > services/notification-service/.env << EOF
DATABASE_URL=postgresql://netpulse:password@db:5432/netpulse
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=noreply@yourcompany.com
AFRICAS_TALKING_API_KEY=your_africas_talking_api_key
AFRICAS_TALKING_USERNAME=your_username
EOF
```

### 3. Start Development Environment

```bash
# Start all services
docker-compose up --build

# Or start in background
docker-compose up --build -d

# View logs
docker-compose logs -f
```

### 4. Verify Service Health

```bash
# Check API Gateway
curl http://localhost:8000/health

# Check individual services
curl http://localhost:8001/health  # Auth Service
curl http://localhost:8002/health  # Device Service
curl http://localhost:8003/health  # Monitoring Service
curl http://localhost:8004/health  # Alert Service
curl http://localhost:8005/health  # Notification Service
curl http://localhost:8006/health  # Reporting Service
```

### 5. Initialize Database

```bash
# Create database tables for each service
docker-compose exec auth-service python -c "
from database import engine
from models import Base
Base.metadata.create_all(bind=engine)
print('Auth service database initialized')
"

docker-compose exec device-service python -c "
from database import engine
from models import Base
Base.metadata.create_all(bind=engine)
print('Device service database initialized')
"

docker-compose exec alert-service python -c "
from database import engine
from models import Base
Base.metadata.create_all(bind=engine)
print('Alert service database initialized')
"

# Initialize TimescaleDB for monitoring service
docker-compose exec monitoring-service python -c "
from database import engine
from models import Base
Base.metadata.create_all(bind=engine)
print('Monitoring service database initialized')
"
```

## Production Deployment

### 1. Environment Configuration

Create production environment files:

#### **Production Database Configuration**
```bash
cat > .env.prod << EOF
# Database
DATABASE_URL=postgresql://netpulse_user:secure_password@your-db-host:5432/netpulse_prod
REDIS_URL=redis://your-redis-host:6379/0

# Message Queue
CELERY_BROKER_URL=amqp://netpulse:secure_password@your-rabbitmq-host:5672//
CELERY_RESULT_BACKEND=redis://your-redis-host:6379/1

# Security
SECRET_KEY=your-super-secure-production-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# External Services
SENDGRID_API_KEY=your_production_sendgrid_key
SENDGRID_FROM_EMAIL=alerts@yourcompany.com
AFRICAS_TALKING_API_KEY=your_production_africas_talking_key
AFRICAS_TALKING_USERNAME=your_username

# Service URLs (internal)
AUTH_SERVICE_URL=http://auth-service:8001
DEVICE_SERVICE_URL=http://device-service:8002
MONITORING_SERVICE_URL=http://monitoring-service:8003
ALERT_SERVICE_URL=http://alert-service:8004
NOTIFICATION_SERVICE_URL=http://notification-service:8005
REPORTING_SERVICE_URL=http://reporting-service:8006
EOF
```

### 2. SSL Certificate Setup

```bash
# Create SSL directory
mkdir -p ssl

# Copy your SSL certificates
cp your-domain.crt ssl/
cp your-domain.key ssl/
cp ca-bundle.crt ssl/  # If using CA bundle
```

### 3. Production Build and Deploy

```bash
# Build all services for production
docker-compose -f docker-compose.prod.yml build

# Deploy with production configuration
docker-compose -f docker-compose.prod.yml up -d

# Check service status
docker-compose -f docker-compose.prod.yml ps
```

### 4. Database Migration and Setup

```bash
# Run production database initialization
./scripts/init-production-db.sh

# Or manually initialize each service
docker-compose -f docker-compose.prod.yml exec auth-service python -c "
import os
os.environ['DATABASE_URL'] = 'your-production-db-url'
from database import engine
from models import Base
Base.metadata.create_all(bind=engine)
"
```

### 5. Start Background Workers

```bash
# Start Celery workers for monitoring
docker-compose -f docker-compose.prod.yml exec monitoring-service celery -A celery_app worker --loglevel=info --detach

# Start Celery beat scheduler
docker-compose -f docker-compose.prod.yml exec monitoring-service celery -A celery_app beat --loglevel=info --detach

# Verify workers are running
docker-compose -f docker-compose.prod.yml exec monitoring-service celery -A celery_app inspect active
```

## Cloud Platform Deployments

### **Render Deployment**

```bash
# Build and push to Render
render-cli build --service-id your-auth-service-id
render-cli build --service-id your-device-service-id
render-cli build --service-id your-monitoring-service-id
render-cli build --service-id your-alert-service-id
render-cli build --service-id your-notification-service-id
render-cli build --service-id your-reporting-service-id
```

### **AWS ECS Deployment**

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com

# Tag and push each service
services=("auth-service" "device-service" "monitoring-service" "alert-service" "notification-service" "reporting-service")

for service in "${services[@]}"; do
  docker tag netpulse-${service}:latest your-account.dkr.ecr.us-east-1.amazonaws.com/netpulse-${service}:latest
  docker push your-account.dkr.ecr.us-east-1.amazonaws.com/netpulse-${service}:latest
done

# Deploy using ECS CLI or CloudFormation
ecs-cli compose --file docker-compose.prod.yml service up --cluster netpulse-cluster
```

### **Kubernetes Deployment**

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/configmaps.yaml
kubectl apply -f k8s/services/
kubectl apply -f k8s/deployments/

# Check deployment status
kubectl get pods -n netpulse
kubectl get services -n netpulse
```

### **Docker Swarm Deployment**

```bash
# Initialize Docker Swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.prod.yml netpulse

# Check services
docker service ls
docker stack ps netpulse
```

## Monitoring and Observability

### **Prometheus and Grafana Setup**

```bash
# Start monitoring stack
docker-compose -f docker-compose.monitoring.yml up -d

# Access Grafana
open http://localhost:3001  # admin/admin

# Access Prometheus
open http://localhost:9090
```

### **Health Check Endpoints**

```bash
# Create health check script
cat > scripts/health-check.sh << 'EOF'
#!/bin/bash
services=("gateway:8000" "auth-service:8001" "device-service:8002" "monitoring-service:8003" "alert-service:8004" "notification-service:8005" "reporting-service:8006")

echo "=== NetPulse Health Check ==="
for service in "${services[@]}"; do
  name="${service%:*}"
  port="${service#*:}"
  if curl -s "http://localhost:${port}/health" > /dev/null; then
    echo "[PASS] ${name} - Healthy"
  else
    echo "[FAIL] ${name} - Unhealthy"
  fi
done
EOF

chmod +x scripts/health-check.sh
./scripts/health-check.sh
```

## Backup and Recovery

### **Database Backup**

```bash
# Create backup script
cat > scripts/backup-db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup PostgreSQL
docker-compose exec -T db pg_dump -U netpulse netpulse > "$BACKUP_DIR/netpulse_db.sql"

# Backup Redis
docker-compose exec -T redis redis-cli BGSAVE
docker cp $(docker-compose ps -q redis):/data/dump.rdb "$BACKUP_DIR/redis_dump.rdb"

echo "Backup completed: $BACKUP_DIR"
EOF

chmod +x scripts/backup-db.sh
```

### **Service Recovery**

```bash
# Restart specific service
docker-compose restart auth-service

# Scale service
docker-compose up -d --scale monitoring-service=3

# Rolling update
docker-compose up -d --force-recreate --no-deps auth-service
```

## Performance Optimization

### **Database Optimization**

```sql
-- Create indexes for better performance
CREATE INDEX CONCURRENTLY idx_devices_organization_id ON devices(organization_id);
CREATE INDEX CONCURRENTLY idx_alerts_created_at ON alerts(created_at);
CREATE INDEX CONCURRENTLY idx_device_metrics_time_device ON device_metrics(time, device_id);

-- Enable TimescaleDB for time-series data
SELECT create_hypertable('device_metrics', 'time');
```

### **Caching Configuration**

```bash
# Redis configuration for production
cat > redis.conf << EOF
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
EOF
```

### **Load Balancing**

```nginx
# nginx.conf for load balancing
upstream api_gateway {
    server gateway:8000;
}

upstream auth_service {
    server auth-service-1:8001;
    server auth-service-2:8001;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://api_gateway;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Troubleshooting

### **Common Issues**

1. **Service communication failures**
   ```bash
   # Check service logs
   docker-compose logs auth-service
   docker-compose logs device-service
   
   # Test inter-service connectivity
   docker-compose exec gateway ping auth-service
   ```

2. **Database connection issues**
   ```bash
   # Check database status
   docker-compose exec db psql -U netpulse -c "SELECT version();"
   
   # Test connection from service
   docker-compose exec auth-service python -c "
   from database import engine
   print(engine.execute('SELECT 1').scalar())
   "
   ```

3. **Message queue issues**
   ```bash
   # Check RabbitMQ status
   docker-compose exec rabbitmq rabbitmqctl status
   
   # Check queue status
   docker-compose exec rabbitmq rabbitmqctl list_queues
   ```

### **Log Aggregation**

```bash
# Centralized logging with ELK stack
docker-compose -f docker-compose.logging.yml up -d

# View aggregated logs
open http://localhost:5601  # Kibana
```

This comprehensive deployment guide covers all aspects of deploying NetPulse's microservices architecture from development to production environments.
