# Monitoring Stack Health Check Script
import requests
import json
import time
import sys
from datetime import datetime

def check_service_health():
    """Check the health of all monitoring services"""
    services = {
        "Backend": "http://localhost:8000/health",
        "Grafana": "http://localhost:3001/api/health",
        "Prometheus": "http://localhost:9090/-/ready",
        "AlertManager": "http://localhost:9093/-/ready",
        "Node Exporter": "http://localhost:9100/metrics"
    }
    
    print("NetPulse Monitoring Health Check")
    print("=" * 40)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_healthy = True
    
    for service_name, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"[PASS] {service_name:<15} - HEALTHY")
            else:
                print(f"[FAIL] {service_name:<15} - UNHEALTHY (HTTP {response.status_code})")
                all_healthy = False
        except requests.exceptions.RequestException as e:
            print(f"[FAIL] {service_name:<15} - UNREACHABLE ({str(e)[:50]}...)")
            all_healthy = False
    
    return all_healthy

def check_prometheus_targets():
    """Check Prometheus targets status"""
    try:
        response = requests.get("http://localhost:9090/api/v1/targets", timeout=5)
        if response.status_code == 200:
            data = response.json()
            active_targets = data.get('data', {}).get('activeTargets', [])
            
            print("\nPrometheus Targets:")
            print("-" * 25)
            
            for target in active_targets:
                job = target.get('labels', {}).get('job', 'unknown')
                health = target.get('health', 'unknown')
                last_scrape = target.get('lastScrape', 'unknown')
                
                status_icon = "[PASS]" if health == "up" else "[FAIL]"
                print(f"{status_icon} {job:<20} - {health.upper()}")
            
            healthy_targets = len([t for t in active_targets if t.get('health') == 'up'])
            total_targets = len(active_targets)
            print(f"\nTarget Health: {healthy_targets}/{total_targets} healthy")
            
            return healthy_targets == total_targets
        else:
            print("[FAIL] Could not fetch Prometheus targets")
            return False
    except Exception as e:
        print(f"[FAIL] Error checking Prometheus targets: {e}")
        return False

def check_grafana_datasources():
    """Check Grafana data sources"""
    try:
        response = requests.get(
            "http://localhost:3001/api/datasources",
            auth=("admin", "admin"),
            timeout=5
        )
        
        if response.status_code == 200:
            datasources = response.json()
            print("\nGrafana Data Sources:")
            print("-" * 26)
            
            for ds in datasources:
                name = ds.get('name', 'unknown')
                type_name = ds.get('type', 'unknown')
                print(f"[PASS] {name:<15} - {type_name}")
            
            return len(datasources) > 0
        else:
            print("[FAIL] Could not fetch Grafana data sources")
            return False
    except Exception as e:
        print(f"[FAIL] Error checking Grafana data sources: {e}")
        return False

def check_metrics_availability():
    """Check if metrics are being generated"""
    try:
        response = requests.get("http://localhost:8000/api/v1/metrics/metrics", timeout=5)
        if response.status_code == 200:
            metrics_data = response.text
            metric_lines = [line for line in metrics_data.split('\n') if line and not line.startswith('#')]
            
            print("\nMetrics Availability:")
            print("-" * 24)
            print(f"[PASS] Metrics endpoint responding")
            print(f"[PASS] {len(metric_lines)} metric samples available")
            
            # Check for specific NetPulse metrics
            netpulse_metrics = [
                'device_status',
                'device_response_time_ms',
                'device_uptime_seconds'
            ]
            
            for metric in netpulse_metrics:
                if metric in metrics_data:
                    print(f"[PASS] {metric} metric found")
                else:
                    print(f"[WARN] {metric} metric missing")
            
            return True
        else:
            print("[FAIL] Metrics endpoint not responding")
            return False
    except Exception as e:
        print(f"[FAIL] Error checking metrics: {e}")
        return False

def check_alertmanager_status():
    """Check AlertManager status"""
    try:
        response = requests.get("http://localhost:9093/api/v1/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("\nAlertManager Status:")
            print("-" * 23)
            print("[PASS] AlertManager is running")
            
            # Check for active alerts
            alerts_response = requests.get("http://localhost:9093/api/v1/alerts", timeout=5)
            if alerts_response.status_code == 200:
                alerts = alerts_response.json().get('data', [])
                active_alerts = [a for a in alerts if a.get('status', {}).get('state') == 'active']
                print(f"Active alerts: {len(active_alerts)}")
            
            return True
        else:
            print("[FAIL] AlertManager not responding")
            return False
    except Exception as e:
        print(f"[FAIL] Error checking AlertManager: {e}")
        return False

def main():
    """Main health check function"""
    print("Starting comprehensive health check...\n")
    
    checks = [
        ("Service Health", check_service_health),
        ("Prometheus Targets", check_prometheus_targets),
        ("Grafana Data Sources", check_grafana_datasources),
        ("Metrics Availability", check_metrics_availability),
        ("AlertManager Status", check_alertmanager_status)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"[FAIL] Error in {check_name}: {e}")
            results.append((check_name, False))
        
        time.sleep(1)  # Brief pause between checks
    
    # Summary
    print("\n" + "=" * 40)
    print("HEALTH CHECK SUMMARY")
    print("=" * 40)
    
    passed_checks = 0
    total_checks = len(results)
    
    for check_name, result in results:
        status_icon = "[PASS]" if result else "[FAIL]"
        status_text = "PASS" if result else "FAIL"
        print(f"{status_icon} {check_name:<25} - {status_text}")
        if result:
            passed_checks += 1
    
    print(f"\nOverall Status: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("All systems operational!")
        return 0
    else:
        print("Some issues detected. Check logs and configuration.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
