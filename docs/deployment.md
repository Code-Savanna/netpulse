# NetPulse Deployment Guide

This guide provides instructions for deploying NetPulse to a production environment.

## Prerequisites

- Docker and Docker Compose
- A registered domain name
- A server with a public IP address

## Production Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/dabwitso/netpulse.git
cd netpulse
```

### 2. Configure Environment Variables

Create a `.env` file in the `netpulse_backend` directory and configure the production settings.

### 3. Build and Deploy

```bash
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

### 4. Run Database Migrations

```bash
docker-compose exec backend alembic upgrade head
```

## Cloud Platforms

NetPulse is designed to be deployed on various cloud platforms. Here are some recommended options:

- **Render:** For hosting the backend API.
- **Vercel:** For deploying the frontend application.
- **AWS ECS:** For container orchestration at scale.
- **Kubernetes:** For enterprise-grade deployments.
