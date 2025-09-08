from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    severity = Column(String, default="medium")  # low, medium, high, critical
    status = Column(String, default="detected")  # detected, contained, eradicated, recovered, closed
    current_phase = Column(String, default="detection")
    assigned_to = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    closed_at = Column(DateTime(timezone=True))
    
    # Phase-specific data
    detection_data = Column(JSON)
    containment_data = Column(JSON)
    eradication_data = Column(JSON)
    recovery_data = Column(JSON)
    post_incident_data = Column(JSON)

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, index=True)
    source = Column(String)  # siem, ids, firewall, etc.
    alert_type = Column(String)
    message = Column(Text)
    severity = Column(String)
    source_ip = Column(String)
    destination_ip = Column(String)
    raw_data = Column(JSON)
    acknowledged = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BlockedIP(Base):
    __tablename__ = "blocked_ips"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, index=True)
    ip_address = Column(String, index=True)
    reason = Column(String)
    blocked_at = Column(DateTime(timezone=True), server_default=func.now())
    unblocked_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)

class ThreatIndicator(Base):
    __tablename__ = "threat_indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, index=True)
    indicator_type = Column(String)  # ip, domain, hash, etc.
    value = Column(String, index=True)
    source = Column(String)  # virustotal, alienvault, etc.
    threat_score = Column(Integer)
    indicator_metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SystemStatus(Base):
    __tablename__ = "system_status"
    
    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, index=True)
    status = Column(String)  # online, offline, degraded
    response_time = Column(Integer)  # in milliseconds
    last_check = Column(DateTime(timezone=True), server_default=func.now())
    status_metadata = Column(JSON)
