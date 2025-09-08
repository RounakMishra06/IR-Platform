from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from app.core.database import get_db
from app.models.database import Incident
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

class TimelineEvent(BaseModel):
    timestamp: datetime
    phase: str
    action: str
    description: str
    user: Optional[str] = None

class IncidentDocumentation(BaseModel):
    incident_id: int
    summary: str
    root_cause: str
    impact_assessment: str
    lessons_learned: str
    iocs: List[str]
    mitigation_steps: List[str]

class TabletopExercise(BaseModel):
    title: str
    description: str
    scenario: str
    participants: List[str]
    scheduled_date: datetime

@router.get("/incident/{incident_id}/timeline")
async def get_incident_timeline(incident_id: int, db: Session = Depends(get_db)):
    """Generate incident timeline from all phases"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    timeline = []
    
    # Detection phase events
    if incident.detection_data:
        timeline.append({
            "timestamp": incident.created_at,
            "phase": "Detection",
            "action": "Incident Created",
            "description": f"Incident '{incident.title}' detected and created",
            "severity": incident.severity
        })
        
        if "confirmed_at" in incident.detection_data:
            timeline.append({
                "timestamp": incident.detection_data["confirmed_at"],
                "phase": "Detection",
                "action": "Attack Confirmed",
                "description": "Attack confirmed, moving to containment phase"
            })
    
    # Containment phase events
    if incident.containment_data:
        if "completed_at" in incident.containment_data:
            timeline.append({
                "timestamp": incident.containment_data["completed_at"],
                "phase": "Containment",
                "action": "Containment Complete",
                "description": f"Blocked {incident.containment_data.get('blocked_ips_count', 0)} IP addresses"
            })
    
    # Eradication phase events
    if incident.eradication_data:
        if "patch_timestamp" in incident.eradication_data:
            timeline.append({
                "timestamp": incident.eradication_data["patch_timestamp"],
                "phase": "Eradication",
                "action": "Patches Applied",
                "description": "Vulnerability patches applied"
            })
        
        if "completed_at" in incident.eradication_data:
            timeline.append({
                "timestamp": incident.eradication_data["completed_at"],
                "phase": "Eradication",
                "action": "Eradication Complete",
                "description": "Threats removed and vulnerabilities patched"
            })
    
    # Recovery phase events
    if incident.recovery_data:
        if "restart_timestamp" in incident.recovery_data:
            timeline.append({
                "timestamp": incident.recovery_data["restart_timestamp"],
                "phase": "Recovery",
                "action": "Services Restarted",
                "description": "System services restarted"
            })
        
        if "completed_at" in incident.recovery_data:
            timeline.append({
                "timestamp": incident.recovery_data["completed_at"],
                "phase": "Recovery",
                "action": "Recovery Complete",
                "description": "System fully recovered and operational"
            })
    
    # Sort timeline by timestamp
    timeline.sort(key=lambda x: x["timestamp"])
    
    return {
        "incident_id": incident_id,
        "timeline": timeline,
        "total_events": len(timeline),
        "duration": (timeline[-1]["timestamp"] - timeline[0]["timestamp"]).total_seconds() / 3600 if timeline else 0
    }

@router.post("/incident/{incident_id}/document")
async def create_incident_documentation(
    incident_id: int, 
    documentation: IncidentDocumentation, 
    db: Session = Depends(get_db)
):
    """Create comprehensive incident documentation"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Update post-incident data
    post_incident_data = incident.post_incident_data or {}
    post_incident_data.update({
        "documentation": {
            "summary": documentation.summary,
            "root_cause": documentation.root_cause,
            "impact_assessment": documentation.impact_assessment,
            "lessons_learned": documentation.lessons_learned,
            "iocs": documentation.iocs,
            "mitigation_steps": documentation.mitigation_steps,
            "documented_at": datetime.utcnow().isoformat()
        }
    })
    incident.post_incident_data = post_incident_data
    
    db.commit()
    
    return {
        "message": "Incident documentation created successfully",
        "incident_id": incident_id,
        "documentation_id": str(uuid.uuid4())
    }

@router.get("/incident/{incident_id}/report")
async def generate_incident_report(incident_id: int, format: str = "json", db: Session = Depends(get_db)):
    """Generate comprehensive incident report"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Get timeline
    timeline_response = await get_incident_timeline(incident_id, db)
    
    report_data = {
        "incident_summary": {
            "id": incident.id,
            "title": incident.title,
            "description": incident.description,
            "severity": incident.severity,
            "status": incident.status,
            "created_at": incident.created_at,
            "closed_at": incident.closed_at,
            "assigned_to": incident.assigned_to
        },
        "timeline": timeline_response["timeline"],
        "phases": {
            "detection": incident.detection_data,
            "containment": incident.containment_data,
            "eradication": incident.eradication_data,
            "recovery": incident.recovery_data,
            "post_incident": incident.post_incident_data
        },
        "metrics": {
            "total_duration_hours": timeline_response["duration"],
            "time_to_containment": None,  # Calculate based on timeline
            "time_to_eradication": None,  # Calculate based on timeline
            "time_to_recovery": None     # Calculate based on timeline
        }
    }
    
    # Calculate phase durations
    detection_time = incident.created_at
    if incident.containment_data and "completed_at" in incident.containment_data:
        containment_time = datetime.fromisoformat(incident.containment_data["completed_at"])
        report_data["metrics"]["time_to_containment"] = (containment_time - detection_time).total_seconds() / 3600
    
    return {
        "report": report_data,
        "generated_at": datetime.utcnow(),
        "format": format
    }

@router.post("/tabletop-exercise")
async def schedule_tabletop_exercise(exercise: TabletopExercise):
    """Schedule a tabletop exercise based on incident lessons learned"""
    exercise_id = str(uuid.uuid4())
    
    # In a real implementation, this would integrate with a scheduling system
    scheduled_exercise = {
        "id": exercise_id,
        "title": exercise.title,
        "description": exercise.description,
        "scenario": exercise.scenario,
        "participants": exercise.participants,
        "scheduled_date": exercise.scheduled_date,
        "status": "scheduled",
        "created_at": datetime.utcnow()
    }
    
    return {
        "message": "Tabletop exercise scheduled successfully",
        "exercise_id": exercise_id,
        "exercise": scheduled_exercise
    }

@router.get("/exercises")
async def get_scheduled_exercises():
    """Get list of scheduled tabletop exercises"""
    # In a real implementation, this would fetch from database
    exercises = [
        {
            "id": "ex-001",
            "title": "Ransomware Response Exercise",
            "scenario": "Large-scale ransomware attack simulation",
            "scheduled_date": "2024-02-15T10:00:00Z",
            "status": "scheduled"
        },
        {
            "id": "ex-002", 
            "title": "Data Breach Response",
            "scenario": "Customer data exfiltration scenario",
            "scheduled_date": "2024-03-01T14:00:00Z",
            "status": "scheduled"
        }
    ]
    
    return {
        "exercises": exercises,
        "total_count": len(exercises)
    }

@router.post("/incident/{incident_id}/close")
async def close_incident(incident_id: int, db: Session = Depends(get_db)):
    """Close the incident and finalize documentation"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Verify all phases are complete
    required_phases = ["detection", "containment", "eradication", "recovery"]
    for phase in required_phases:
        phase_data = getattr(incident, f"{phase}_data", {})
        if not phase_data or "completed_at" not in phase_data:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot close incident: {phase} phase not completed"
            )
    
    # Close the incident
    incident.status = "closed"
    incident.current_phase = "closed"
    incident.closed_at = datetime.utcnow()
    
    # Update post-incident data
    post_incident_data = incident.post_incident_data or {}
    post_incident_data.update({
        "closed_at": datetime.utcnow().isoformat(),
        "closure_confirmed": True
    })
    incident.post_incident_data = post_incident_data
    
    db.commit()
    
    return {
        "message": "Incident closed successfully",
        "incident_id": incident_id,
        "final_status": "closed",
        "closed_at": incident.closed_at
    }

@router.get("/metrics/summary")
async def get_incident_metrics_summary(db: Session = Depends(get_db)):
    """Get summary metrics for all incidents"""
    incidents = db.query(Incident).all()
    
    metrics = {
        "total_incidents": len(incidents),
        "by_severity": {
            "critical": len([i for i in incidents if i.severity == "critical"]),
            "high": len([i for i in incidents if i.severity == "high"]),
            "medium": len([i for i in incidents if i.severity == "medium"]),
            "low": len([i for i in incidents if i.severity == "low"])
        },
        "by_status": {
            "active": len([i for i in incidents if i.status != "closed"]),
            "closed": len([i for i in incidents if i.status == "closed"])
        },
        "average_resolution_time": 0,  # Calculate from closed incidents
        "most_common_attack_types": []  # Analyze from incident data
    }
    
    # Calculate average resolution time for closed incidents
    closed_incidents = [i for i in incidents if i.status == "closed" and i.closed_at]
    if closed_incidents:
        total_time = sum((i.closed_at - i.created_at).total_seconds() for i in closed_incidents)
        metrics["average_resolution_time"] = (total_time / len(closed_incidents)) / 3600  # in hours
    
    return metrics

@router.get("/lessons-learned")
async def get_lessons_learned(db: Session = Depends(get_db)):
    """Get aggregated lessons learned from all incidents"""
    incidents = db.query(Incident).filter(Incident.post_incident_data.isnot(None)).all()
    
    lessons = []
    for incident in incidents:
        post_data = incident.post_incident_data or {}
        doc_data = post_data.get("documentation", {})
        if "lessons_learned" in doc_data:
            lessons.append({
                "incident_id": incident.id,
                "incident_title": incident.title,
                "severity": incident.severity,
                "lessons": doc_data["lessons_learned"],
                "documented_at": doc_data.get("documented_at")
            })
    
    return {
        "total_incidents": len(lessons),
        "lessons_learned": lessons
    }
