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

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

#### Frontend Setup  
```bash
cd frontend
npm install
npm start
```

### Option 3: Docker Setup
```bash
docker-compose up --build
```

## 🌐 Access Points

Once running, access the platform at:

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000  
- **API Documentation**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc

## 🔌 Integrations

### SIEM Systems
- **Splunk**: REST API integration for log analysis
- **ELK Stack**: Elasticsearch queries for threat hunting
- **QRadar**: Custom API connectors for incident correlation

### Firewall & Network
- **pfSense**: Automated rule management
- **Cisco ASA**: Policy enforcement APIs  
- **FortiGate**: Threat blocking integration

### Threat Intelligence
- **VirusTotal**: File and URL reputation checks
- **AlienVault OTX**: IOC validation and enrichment
- **MISP**: Threat intelligence sharing

## 📊 Dashboard Features

### Real-time Monitoring
- Live threat level indicators
- Active incident counters  
- System health metrics
- Performance dashboards

### Incident Workflow
- Phase-based navigation tabs
- Progress tracking across phases
- Automated phase transitions
- Workflow status indicators

### Analytics & Reporting
- Incident timeline visualization
- Attack vector analysis
- Response time metrics
- Comprehensive PDF reports

## 🛡️ Security Features

### Authentication & Authorization
- Multi-factor authentication support
- Role-based access control
- Session management
- Audit logging

### Data Protection
- Encrypted data storage
- Secure API communications
- PII data handling
- Compliance reporting

## 🔧 Configuration

### Environment Variables
```bash
# Backend Configuration
DATABASE_URL=postgresql://user:pass@localhost/irplatform
SIEM_API_KEY=your_siem_api_key
FIREWALL_API_ENDPOINT=https://your-firewall/api

# Frontend Configuration  
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

### Database Setup
```bash
# PostgreSQL setup
createdb irplatform
python -c "from app.models.database import create_tables; create_tables()"
```

## 📱 API Documentation

### Detection Phase Endpoints
- `GET /api/detection/alerts` - Retrieve live alerts
- `POST /api/detection/confirm-attack` - Confirm security incident
- `GET /api/detection/suspicious-ips` - Get suspicious IP addresses

### Containment Phase Endpoints  
- `POST /api/containment/block-ip` - Block malicious IP addresses
- `GET /api/containment/status` - Get containment status
- `POST /api/containment/firewall-rule` - Create firewall rules

### Eradication Phase Endpoints
- `GET /api/eradication/analysis` - Get log analysis results
- `POST /api/eradication/search-iocs` - Search threat intelligence
- `POST /api/eradication/patch-vulnerabilities` - Apply security patches

### Recovery Phase Endpoints
- `GET /api/recovery/system-health` - Monitor system health
- `POST /api/recovery/start-recovery` - Initiate recovery procedures
- `GET /api/recovery/performance-metrics` - Get performance data

### Post-Incident Phase Endpoints
- `GET /api/post-incident/timeline` - Get incident timeline
- `POST /api/post-incident/generate-report` - Generate incident report
- `POST /api/post-incident/lessons-learned` - Document lessons learned

## 🐳 Docker Deployment

### Development Environment
```bash
docker-compose -f docker-compose.dev.yml up
```

### Production Environment  
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment-specific Configurations
- **Development**: Hot reload, debug logging, development database
- **Production**: Optimized builds, production database, security headers

## 🧪 Testing

### Backend Testing
```bash
cd backend  
pytest tests/ -v --coverage
```

### Frontend Testing
```bash
cd frontend
npm test -- --coverage --watchAll=false
```

### Integration Testing
```bash
python -m pytest tests/integration/ -v
```

## 📈 Performance Optimization

### Backend Optimization
- Asynchronous request handling
- Database query optimization
- Caching strategies
- API rate limiting

### Frontend Optimization  
- Component lazy loading
- Bundle size optimization
- Service worker caching
- Image optimization

## 🔍 Monitoring & Logging

### Application Monitoring
- Health check endpoints
- Performance metrics collection
- Error tracking and alerting
- User activity logging

### Infrastructure Monitoring
- Server resource usage
- Database performance metrics
- Network latency monitoring
- Security event logging

## 🚨 Incident Response Workflow

### 1. Detection Phase
1. Monitor live alerts from integrated systems
2. Analyze suspicious activities and traffic patterns  
3. Confirm genuine security incidents
4. Initialize incident response process

### 2. Containment Phase
1. Block malicious IP addresses automatically
2. Isolate affected systems from network
3. Implement emergency firewall rules
4. Monitor containment effectiveness

### 3. Eradication Phase  
1. Perform comprehensive log analysis
2. Search threat intelligence databases
3. Identify and patch vulnerabilities
4. Remove malware and malicious artifacts

### 4. Recovery Phase
1. Restore systems to normal operation
2. Monitor system health and performance
3. Implement additional security measures
4. Verify complete system recovery

### 5. Post-Incident Phase
1. Document complete incident timeline
2. Generate comprehensive reports
3. Conduct lessons learned analysis  
4. Update security procedures and policies

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality  
5. Submit a pull request

### Code Standards
- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript/TypeScript
- Write comprehensive tests
- Document all functions and APIs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React team for the powerful frontend library
- Material-UI for beautiful UI components
- All contributors to the open source security tools integrated

## 📞 Support & Contact

- **GitHub Issues**: For bug reports and feature requests
- **Documentation**: Comprehensive guides and API references
- **Community**: Join our security community discussions

## 🗓️ Roadmap

### Phase 1 (Current)
- [x] Core platform architecture
- [x] Five-phase incident response workflow
- [x] Basic SIEM integrations
- [x] Web-based dashboard

### Phase 2 (Next)
- [ ] Advanced threat intelligence
- [ ] Machine learning-based detection
- [ ] Mobile application
- [ ] Multi-tenant support

### Phase 3 (Future)
- [ ] AI-powered response automation
- [ ] Advanced analytics and reporting
- [ ] Compliance framework integration
- [ ] Custom playbook editor

---

**Built with ❤️ for cybersecurity professionals worldwide**

## 👨‍💻 Author

**Rounak Mishra** - [LinkedIn](https://linkedin.com/in/rounakmishra)
