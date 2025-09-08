# IR-Platform
🚨 Centralized Incident Response Platform

A web-based Incident Response (IR) platform with a unified dashboard to manage the full IR lifecycle:
Detection → Containment → Eradication → Recovery → Post-Incident

📌 Features

Detection: Live alerts from SIEM / IDS, suspicious IPs & traffic spikes.

Containment: Firewall/IPS integration to block malicious connections.

Eradication: Log analysis, threat intel integration, vulnerability status.

Recovery: Automated service restart, uptime monitoring, load balancing.

Post-Incident: Incident timeline, IOC documentation, automated reporting.

🛠️ Tech Stack

Backend: FastAPI + Uvicorn

Frontend: React (planned)

Database: SQLAlchemy (future)

Integrations: SIEM (Splunk/ELK), Firewall APIs, Threat Intel feeds

🚀 Setup Instructions
1. Clone the Project
git clone https://github.com/your-username/ir-platform.git
cd ir-platform

2. Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Linux/Mac

pip install fastapi uvicorn requests sqlalchemy

3. Run Backend Server
uvicorn main:app --reload --host 127.0.0.1 --port 8000


Now open: http://127.0.0.1:8000

You should see:

{"message": "IR Platform Backend is running"}

📂 Project Structure
IR-Platform/
│── backend/        # FastAPI backend
│   ├── main.py     # Entry point
│── frontend/       # React frontend (coming soon)
│── README.md       # Project guide

✅ Roadmap

 FastAPI backend setup

 React frontend with Detection page

 Containment → Firewall API integration

 Database for incident storage

 Automated incident reporting (PDF/HTML export)

👨‍💻 Author

Rounak Mishra – LinkedIn
