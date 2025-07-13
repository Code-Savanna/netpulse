#!/bin/bash

# NetPulse Monitoring Setup Script
# This script sets up and validates the monitoring infrastructure

set -e

echo "🚀 NetPulse Monitoring Setup Script"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if Docker and Docker Compose are installed
check_dependencies() {
    print_step "Checking dependencies..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_status "Dependencies check passed"
}

# Check if monitoring directory exists
check_monitoring_files() {
    print_step "Checking monitoring configuration files..."
    
    local required_files=(
        "monitoring/prometheus.yml"
        "monitoring/alert_rules.yml"
        "monitoring/alertmanager.yml"
        "monitoring/grafana/dashboards/netpulse-overview.json"
        "monitoring/grafana/dashboards/device-details.json"
    )
    
    local missing_files=()
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            missing_files+=("$file")
        fi
    done
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        print_error "Missing monitoring configuration files:"
        for file in "${missing_files[@]}"; do
            echo "  - $file"
        done
        print_error "Please ensure all monitoring files are created before running this script."
        exit 1
    fi
    
    print_status "All monitoring configuration files found"
}

# Start the monitoring stack
start_services() {
    print_step "Starting NetPulse monitoring stack..."
    
    # Stop any existing services
    print_status "Stopping existing services..."
    docker-compose -f docker-compose.prod.yml down --remove-orphans
    
    # Build and start services
    print_status "Building and starting services..."
    docker-compose -f docker-compose.prod.yml up --build -d
    
    print_status "Services started successfully"
}

# Wait for services to be ready
wait_for_services() {
    print_step "Waiting for services to be ready..."
    
    local services=(
        "http://localhost:8000/health:Backend"
        "http://localhost:3001/api/health:Grafana"
        "http://localhost:9090/-/ready:Prometheus"
        "http://localhost:9093/-/ready:AlertManager"
    )
    
    for service in "${services[@]}"; do
        IFS=':' read -r url name <<< "$service"
        print_status "Waiting for $name to be ready..."
        
        local max_attempts=30
        local attempt=1
        
        while [[ $attempt -le $max_attempts ]]; do
            if curl -s "$url" >/dev/null 2>&1; then
                print_status "$name is ready"
                break
            fi
            
            if [[ $attempt -eq $max_attempts ]]; then
                print_warning "$name is not responding after $max_attempts attempts"
                break
            fi
            
            sleep 2
            ((attempt++))
        done
    done
}

# Import Grafana dashboards
import_dashboards() {
    print_step "Importing Grafana dashboards..."
    
    # Wait a bit more for Grafana to be fully ready
    sleep 10
    
    local dashboards=(
        "monitoring/grafana/dashboards/netpulse-overview.json"
        "monitoring/grafana/dashboards/device-details.json"
    )
    
    for dashboard in "${dashboards[@]}"; do
        if [[ -f "$dashboard" ]]; then
            print_status "Importing $(basename "$dashboard")..."
            
            # Import dashboard using Grafana API
            curl -s -X POST \
                -H "Content-Type: application/json" \
                -u admin:admin \
                -d @"$dashboard" \
                http://localhost:3001/api/dashboards/db >/dev/null 2>&1 || \
                print_warning "Failed to import $(basename "$dashboard") - may already exist"
        fi
    done
    
    print_status "Dashboard import completed"
}

# Validate monitoring setup
validate_setup() {
    print_step "Validating monitoring setup..."
    
    # Check Prometheus targets
    print_status "Checking Prometheus targets..."
    local targets_response=$(curl -s http://localhost:9090/api/v1/targets)
    if echo "$targets_response" | grep -q '"health":"up"'; then
        print_status "Prometheus targets are healthy"
    else
        print_warning "Some Prometheus targets may be down"
    fi
    
    # Check if metrics are available
    print_status "Checking metrics availability..."
    local metrics_response=$(curl -s http://localhost:8000/api/v1/metrics/metrics)
    if [[ -n "$metrics_response" ]]; then
        print_status "Backend metrics are available"
    else
        print_warning "Backend metrics endpoint may not be working"
    fi
    
    print_status "Validation completed"
}

# Display access information
show_access_info() {
    print_step "Setup completed! Access information:"
    echo ""
    echo "🌐 Web Interfaces:"
    echo "  NetPulse App:    http://localhost:3000"
    echo "  Grafana:         http://localhost:3001 (admin/admin)"
    echo "  Prometheus:      http://localhost:9090"
    echo "  AlertManager:    http://localhost:9093"
    echo "  Flower (Celery): http://localhost:5555"
    echo ""
    echo "📊 Dashboards:"
    echo "  Network Overview: http://localhost:3001/d/netpulse-noc/netpulse-network-operations-center"
    echo "  Device Details:   http://localhost:3001/d/device-details/device-details-dashboard"
    echo ""
    echo "🔧 Configuration Files:"
    echo "  Prometheus:    monitoring/prometheus.yml"
    echo "  AlertManager:  monitoring/alertmanager.yml"
    echo "  Alert Rules:   monitoring/alert_rules.yml"
    echo ""
    echo "📚 Documentation:"
    echo "  See docs/monitoring.md for detailed configuration and troubleshooting"
    echo ""
    echo "🚀 Next Steps:"
    echo "  1. Add devices through the NetPulse web interface"
    echo "  2. Configure alert notifications in monitoring/alertmanager.yml"
    echo "  3. Customize dashboards in Grafana"
    echo "  4. Set up backup procedures for monitoring data"
}

# Show service status
show_service_status() {
    print_step "Service Status:"
    docker-compose -f docker-compose.prod.yml ps
}

# Main execution
main() {
    check_dependencies
    check_monitoring_files
    start_services
    wait_for_services
    import_dashboards
    validate_setup
    show_service_status
    show_access_info
    
    echo ""
    print_status "NetPulse monitoring setup completed successfully! 🎉"
}

# Handle script interruption
trap 'print_error "Setup interrupted"; exit 1' INT TERM

# Run main function
main "$@"
