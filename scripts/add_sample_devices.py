#!/usr/bin/env python3
"""
Script to add sample devices to the database for testing
"""
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models import models
from app.services.device_service import DeviceService
from app.models.schemas import DeviceCreate

def create_sample_devices():
    """Create sample devices for testing"""
    db = SessionLocal()
    device_service = DeviceService(db)
    
    sample_devices = [
        DeviceCreate(
            name="Main Router",
            ip_address="192.168.1.1",
            device_type="router",
            location="Network Closet A"
        ),
        DeviceCreate(
            name="Core Switch",
            ip_address="192.168.1.2",
            device_type="switch",
            location="Server Room"
        ),
        DeviceCreate(
            name="Web Server",
            ip_address="192.168.1.10",
            device_type="server",
            location="Data Center"
        ),
        DeviceCreate(
            name="DNS Server",
            ip_address="8.8.8.8",
            device_type="server",
            location="External"
        ),
        DeviceCreate(
            name="Office WiFi AP",
            ip_address="192.168.1.100",
            device_type="access_point",
            location="Office Floor 1"
        )
    ]
    
    for device_data in sample_devices:
        try:
            device = device_service.create_device(device_data)
            print(f"Created device: {device.name} ({device.ip_address})")
        except Exception as e:
            print(f"Error creating device {device_data.name}: {e}")
    
    db.close()
    print("Sample devices created successfully!")

if __name__ == "__main__":
    create_sample_devices()
