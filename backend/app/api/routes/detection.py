from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.integrations.siem import SIEMIntegration
from app.integrations.ids import IDSIntegration
from app.models.database import Alert, Incident
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class AlertResponse(BaseModel):
    id: int
    source: str
    alert_type: str
    message: str
    severity: str
    source_ip: str
    destination_ip: str
    created_at: datetime
    acknowledged: bool

class ConfirmAttackRequest(BaseModel):
    alert_ids: List[int]
    incident_title: str
    incident_description: str
    severity: str

@router.get("/alerts", response_model=List[AlertResponse])
async def get_live_alerts(db: Session = Depends(get_db)):
    """Get live alerts from SIEM and IDS systems"""
    try:
        # Fetch from SIEM
        siem = SIEMIntegration()
        siem_alerts = await siem.get_live_alerts()
        
        # Fetch from IDS
        ids = IDSIntegration()
        ids_alerts = await ids.get_live_alerts()
        
        # Store alerts in database
        all_alerts = []
        for alert_data in siem_alerts + ids_alerts:
            alert = Alert(
                source=alert_data["source"],
                alert_type=alert_data["type"],
                message=alert_data["message"],
                severity=alert_data["severity"],
                source_ip=alert_data.get("source_ip", ""),
                destination_ip=alert_data.get("destination_ip", ""),
                raw_data=alert_data
            )
            db.add(alert)
            all_alerts.append(alert)
        
        db.commit()
        
        # Return recent unacknowledged alerts
        recent_alerts = db.query(Alert).filter(
            Alert.acknowledged == False
        ).order_by(Alert.created_at.desc()).limit(50).all()
        
        return recent_alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch alerts: {str(e)}")

@router.get("/suspicious-ips")
async def get_suspicious_ips():
    """Get list of suspicious IP addresses with traffic analysis"""
    try:
        siem = SIEMIntegration()
        suspicious_ips = await siem.get_suspicious_ips()
        
        return {
            "suspicious_ips": suspicious_ips,
            "analysis": {
                "total_count": len(suspicious_ips),
                "high_risk_count": len([ip for ip in suspicious_ips if ip["risk_score"] > 7]),
                "countries": list(set([ip.get("country", "Unknown") for ip in suspicious_ips]))
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze IPs: {str(e)}")

@router.post("/confirm-attack")
async def confirm_attack(request: ConfirmAttackRequest, db: Session = Depends(get_db)):
    """Confirm attack and create incident, move to containment phase"""
    try:
        # Create new incident
        incident = Incident(
            title=request.incident_title,
            description=request.incident_description,
            severity=request.severity,
            status="confirmed",
            current_phase="containment",
            detection_data={
                "confirmed_alerts": request.alert_ids,
                "confirmed_at": datetime.utcnow().isoformat()
            }
        )
        
        db.add(incident)
        db.commit()
        db.refresh(incident)
        
        # Mark alerts as acknowledged
        db.query(Alert).filter(Alert.id.in_(request.alert_ids)).update({
            "acknowledged": True,
            "incident_id": incident.id
        })
        db.commit()
        
        return {
            "message": "Attack confirmed successfully",
            "incident_id": incident.id,
            "next_phase": "containment"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to confirm attack: {str(e)}")

@router.get("/traffic-analysis")
async def get_traffic_analysis():
    """Get real-time traffic analysis and patterns"""
    try:
        siem = SIEMIntegration()
        traffic_data = await siem.get_traffic_analysis()
        
        return {
            "current_traffic": traffic_data["current"],
            "baseline": traffic_data["baseline"],
            "anomalies": traffic_data["anomalies"],
            "top_talkers": traffic_data["top_talkers"],
            "protocols": traffic_data["protocols"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get traffic analysis: {str(e)}")

@router.post("/acknowledge-alert/{alert_id}")
async def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    """Acknowledge a specific alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.acknowledged = True
    db.commit()
    
    return {"message": "Alert acknowledged successfully"}
