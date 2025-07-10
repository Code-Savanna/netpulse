
```markdown
# NetPulse

**NetPulse** is a real-time **Network Monitoring Dashboard** designed to simulate the operations of a Network Operations Center (NOC) for telecoms, ISPs, and infrastructure engineers. Built with scalability, observability, and real-time feedback in mind, NetPulse helps teams monitor server health, generate alerts, and visualize key network metrics.

---

##  Features

-  Real-time server metric simulation (CPU, memory, uptime, status)
-  Live dashboard with device status indicators (Up/Down)
-  Graphs and analytics for usage trends and uptime
-  Alerting system for abnormal conditions (e.g. CPU > 90%)
-  SMS and Email notifications using **Africa's Talking** and **SendGrid**
-  WebSocket support for pushing updates to the frontend
-  Admin panel with device management and alert logs

---

## Tech Stack

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

## Project Structure

```

netpulse/
├── netpulse\_backend/        # FastAPI backend with Celery + PostgreSQL
├── netpulse\_frontend/       # React.js dashboard with Tailwind CSS
├── docker-compose.yml       # Multi-service Docker configuration
└── README.md

````

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/netpulse.git
cd netpulse
````

### 2. Launch Services with Docker

```bash
docker-compose up --build
```

### 3. Access the App

* Backend API: [http://localhost:8000](http://localhost:8000)
* Frontend Dashboard: [http://localhost:3000](http://localhost:3000)

---

## Simulated Device Metrics

Server metrics are generated periodically using a background Celery worker. You can configure:

* Interval of metric updates
* Alert thresholds
* Number of devices

---

## Environment Variables

Create a `.env` file for the backend:

```env
DATABASE_URL=postgresql://netpulse:secret@db:5432/netpulse
REDIS_URL=redis://redis:6379/0
AFRICAS_TALKING_API_KEY=your_key
SENDGRID_API_KEY=your_key
```


## License

This project is licensed under the MIT License.

---

##  Author

**Dabwitso Mweemba**
Cofounder – Code Savanna & Learniva AI
 Lusaka, Zambia
 [LinkedIn](https://www.linkedin.com/) | [codesavanna.org](https://codesavanna.org)

---

##  Contributions

Pull requests, feature suggestions, and forks are welcome!
