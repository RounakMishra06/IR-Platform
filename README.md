# Centralized Incident Response Platform

A comprehensive incident response platform with automated workflows for Detection, Containment, Eradication, Recovery, and Post-Incident phases.

## 🏗️ Architecture

### Frontend (React + TypeScript)
- Dashboard with phase-based navigation tabs
- Real-time notifications and action buttons
- Interactive dashboards for each IR phase
- Material-UI components for professional UI

### Backend (FastAPI + Python)
- RESTful API for each incident response phase
- Integrations with SIEM, Firewall, Threat Intel
- Automated response capabilities
- Incident documentation and reporting
- SQLAlchemy ORM with PostgreSQL

### Database (PostgreSQL)
- Incident tracking and documentation
- User management and audit logs
- Configuration and integration settings

## 📁 Project Structure

```
incident-response-platform/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/          # Phase-specific pages
│   │   ├── context/        # React context providers
│   │   └── services/       # API communication
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/routes/     # API routes for each phase
│   │   ├── core/           # Core configurations
│   │   ├── integrations/   # External service integrations
│   │   └── models/         # Database models
├── docker-compose.yml      # Docker orchestration
├── setup.py               # Python setup script
├── setup.bat             # Windows setup script
└── setup.sh             # Unix setup script
```

## ⚡ Features

### 1. 🔍 Detection Phase
- Live alerts from SIEM & IDS systems
- Suspicious IP address analysis
- Traffic pattern monitoring
- Attack confirmation workflow

### 2. 🛡️ Containment Phase
- Automated IP blocking via firewall APIs
- Real-time connection monitoring
- Rate limiting controls
- Containment status tracking

### 3. 🧹 Eradication Phase
- Advanced log analysis dashboard
- Threat intelligence integration
- Vulnerability patch management
- Malware analysis and removal

### 4. 🔄 Recovery Phase
- System health monitoring
- Automated service recovery
- Load balancer configuration
- Performance metrics tracking

### 5. 📝 Post-Incident Phase
- Automated timeline generation
- Comprehensive documentation tools
- Incident report generation
- Lessons learned tracking

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**Unix/Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**Python (Cross-platform):**
```bash
python setup.py
```

### Option 2: Manual Setup

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd incident-response-platform
```

2. **Backend Setup:**
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Unix: source venv/bin/activate
pip install -r requirements.txt
```

3. **Frontend Setup:**
```bash
cd frontend
npm install
```

4. **Environment Configuration:**
   - Copy `backend/.env` and configure your integrations
   - Update database settings and API keys

5. **Run the Application:**

Backend:
```bash
cd backend
uvicorn main:app --reload
```

Frontend:
```bash
cd frontend
npm start
```

### Option 3: Docker Deployment

```bash
docker-compose up --build
```

## 🌐 Access URLs

- **Frontend Dashboard:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Interactive API:** http://localhost:8000/redoc

## 🔧 Configuration

### Environment Variables (backend/.env)

```bash
# Database
DATABASE_URL=postgresql://incident_user:incident_password@localhost/incident_response_db

# SIEM Integration (Optional)
SPLUNK_HOST=your-splunk-server.com
SPLUNK_TOKEN=your-splunk-token
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200

# Firewall API (Optional)
FIREWALL_API_URL=https://your-firewall-api.com
FIREWALL_API_KEY=your-api-key

# Threat Intelligence (Optional)
VIRUSTOTAL_API_KEY=your-virustotal-api-key
ALIENVAULT_API_KEY=your-alienvault-api-key

# Application Settings
SECRET_KEY=your-super-secret-key
REDIS_URL=redis://localhost:6379
```

## 🔌 Integrations

### Supported SIEM Systems
- **Splunk**: REST API integration
- **Elasticsearch/ELK**: Direct API queries
- **Custom SIEM**: Extensible integration framework

### Firewall/Security Tools
- **REST API based firewalls**
- **Palo Alto Networks**
- **Fortinet FortiGate**
- **Custom firewall APIs**

### Threat Intelligence
- **VirusTotal API**
- **AlienVault OTX**
- **Custom threat feeds**

### Automation Tools
- **Ansible playbooks**
- **Custom scripts**
- **Service orchestration**

## 📊 API Endpoints

### Detection Phase
- `GET /api/detection/alerts` - Get live alerts
- `GET /api/detection/suspicious-ips` - Analyze suspicious IPs
- `POST /api/detection/confirm-attack` - Confirm attack

### Containment Phase
- `POST /api/containment/block-ips` - Block IP addresses
- `GET /api/containment/status/{incident_id}` - Get containment status
- `POST /api/containment/containment-complete/{incident_id}` - Mark complete

### Eradication Phase
- `GET /api/eradication/incident/{incident_id}/analysis` - Log analysis
- `POST /api/eradication/search-iocs` - Search threat indicators
- `POST /api/eradication/apply-patches` - Apply security patches

### Recovery Phase
- `GET /api/recovery/services/status` - Service health status
- `POST /api/recovery/services/restart` - Restart services
- `GET /api/recovery/monitoring/dashboard/{incident_id}` - Recovery dashboard

### Post-Incident Phase
- `GET /api/post-incident/incident/{incident_id}/timeline` - Incident timeline
- `POST /api/post-incident/incident/{incident_id}/document` - Create documentation
- `GET /api/post-incident/incident/{incident_id}/report` - Generate report

## 🐳 Docker Support

The platform includes full Docker support with:
- Multi-container setup (Frontend, Backend, Database, Redis)
- Development and production configurations
- Health checks and service dependencies
- Volume persistence for data

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📈 Monitoring & Logging

- Application logs in `/logs` directory
- Performance metrics via API endpoints
- Health check endpoints for monitoring
- Structured logging for analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the integration examples
- Open an issue for bugs or feature requests

## 🔄 Roadmap

- [ ] Machine learning-based threat detection
- [ ] Mobile application for incident response
- [ ] Advanced analytics and reporting
- [ ] Multi-tenant support
- [ ] Single Sign-On (SSO) integration
- [ ] Webhook notifications
- [ ] Custom playbook editor
