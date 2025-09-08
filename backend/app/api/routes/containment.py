from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.integrations.firewall import FirewallIntegration
from app.models.database import Incident, BlockedIP
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class BlockIPRequest(BaseModel):
    ip_addresses: List[str]
    reason: str
    incident_id: int

class ContainmentStatus(BaseModel):
    blocked_ips: List[str]
    active_connections: int
    blocked_connections: int
    rate_limiting_active: bool

@router.get("/incident/{incident_id}/attacker-ips")
async def get_attacker_ips(incident_id: int, db: Session = Depends(get_db)):
    """Get list of attacker IPs for the incident"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Extract IPs from detection data and alerts
    attacker_ips = []
    if incident.detection_data and "suspicious_ips" in incident.detection_data:
        attacker_ips.extend(incident.detection_data["suspicious_ips"])
    
    # Get IPs from related alerts
    # This would typically query the alerts table
    
    return {
        "incident_id": incident_id,
        "attacker_ips": list(set(attacker_ips)),
        "total_count": len(set(attacker_ips))
    }

@router.post("/block-ips")
async def block_ips(request: BlockIPRequest, db: Session = Depends(get_db)):
    """Block IP addresses on firewall"""
    try:
        firewall = FirewallIntegration()
        
        blocked_ips = []
        for ip in request.ip_addresses:
            # Block on firewall
            success = await firewall.block_ip(ip, request.reason)
            
            if success:
                # Record in database
                blocked_ip = BlockedIP(
                    incident_id=request.incident_id,
                    ip_address=ip,
                    reason=request.reason,
                    is_active=True
                )
                db.add(blocked_ip)
                blocked_ips.append(ip)
        
        db.commit()
        
        return {
            "message": f"Successfully blocked {len(blocked_ips)} IP addresses",
            "blocked_ips": blocked_ips,
            "failed_ips": [ip for ip in request.ip_addresses if ip not in blocked_ips]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to block IPs: {str(e)}")

@router.get("/status/{incident_id}")
async def get_containment_status(incident_id: int, db: Session = Depends(get_db)):
    """Get containment status for incident"""
    try:
        # Get blocked IPs for this incident
        blocked_ips = db.query(BlockedIP).filter(
            BlockedIP.incident_id == incident_id,
            BlockedIP.is_active == True
        ).all()
        
        firewall = FirewallIntegration()
        connection_stats = await firewall.get_connection_stats()
        
        return {
            "incident_id": incident_id,
            "blocked_ips_count": len(blocked_ips),
            "blocked_ips": [ip.ip_address for ip in blocked_ips],
            "active_connections": connection_stats["active"],
            "blocked_connections": connection_stats["blocked"],
            "rate_limiting_active": connection_stats["rate_limiting"],
            "last_updated": datetime.utcnow()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")

@router.post("/unblock-ip/{ip_address}")
async def unblock_ip(ip_address: str, incident_id: int, db: Session = Depends(get_db)):
    """Unblock a specific IP address"""
    try:
        firewall = FirewallIntegration()
        success = await firewall.unblock_ip(ip_address)
        
        if success:
            # Update database
            blocked_ip = db.query(BlockedIP).filter(
                BlockedIP.ip_address == ip_address,
                BlockedIP.incident_id == incident_id,
                BlockedIP.is_active == True
            ).first()
            
            if blocked_ip:
                blocked_ip.is_active = False
                blocked_ip.unblocked_at = datetime.utcnow()
                db.commit()
        
        return {"message": f"IP {ip_address} unblocked successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to unblock IP: {str(e)}")

@router.post("/containment-complete/{incident_id}")
async def mark_containment_complete(incident_id: int, db: Session = Depends(get_db)):
    """Mark containment phase as complete and move to eradication"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Update incident status
    incident.current_phase = "eradication"
    incident.status = "contained"
    
    # Update containment data
    containment_data = incident.containment_data or {}
    containment_data.update({
        "completed_at": datetime.utcnow().isoformat(),
        "blocked_ips_count": db.query(BlockedIP).filter(
            BlockedIP.incident_id == incident_id,
            BlockedIP.is_active == True
        ).count()
    })
    incident.containment_data = containment_data
    
    db.commit()
    
    return {
        "message": "Containment phase completed successfully",
        "incident_id": incident_id,
        "next_phase": "eradication"
    }

@router.get("/logs/{incident_id}")
async def get_containment_logs(incident_id: int):
    """Get logs of containment actions"""
    try:
        firewall = FirewallIntegration()
        logs = await firewall.get_containment_logs(incident_id)
        
        return {
            "incident_id": incident_id,
            "logs": logs,
            "total_actions": len(logs)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get logs: {str(e)}")
