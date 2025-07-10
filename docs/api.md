# NetPulse API Documentation

Welcome to the NetPulse API documentation. This document provides a comprehensive overview of the available endpoints, request parameters, and response formats.

## Base URL

All API URLs referenced in this documentation have the following base:

`http://localhost:8000/api/v1`

## Authentication

The NetPulse API uses token-based authentication. To authenticate, you must include an `Authorization` header with your API requests.

`Authorization: Bearer <YOUR_ACCESS_TOKEN>`

## Endpoints

### Health Check

- **GET /health**
  - **Description:** Checks the health of the API.
  - **Response:**
    ```json
    {
      "status": "ok"
    }
    ```

### Devices

- **GET /devices**
  - **Description:** Retrieves a list of all monitored devices.
- **GET /devices/{device_id}**
  - **Description:** Retrieves details for a specific device.
- **POST /devices**
  - **Description:** Adds a new device to be monitored.
- **PUT /devices/{device_id}**
  - **Description:** Updates an existing device.
- **DELETE /devices/{device_id}**
  - **Description:** Removes a device from monitoring.

### Metrics

- **GET /metrics/{device_id}**
  - **Description:** Retrieves the latest metrics for a specific device.
- **GET /metrics/{device_id}/history**
  - **Description:** Retrieves historical metrics for a specific device.

### Alerts

- **GET /alerts**
  - **Description:** Retrieves a list of all alerts.
- **GET /alerts/{alert_id}**
  - **Description:** Retrieves details for a specific alert.
- **PUT /alerts/{alert_id}**
  - **Description:** Updates the status of an alert (e.g., acknowledge, resolve).
