from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from app.core.database import get_db
from app.integrations.service_monitor import ServiceMonitorIntegration
from app.integrations.automation import AutomationIntegration
from app.models.database import Incident, SystemStatus
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class ServiceRestartRequest(BaseModel):
    service_names: List[str]
    incident_id: int

class LoadBalancerConfig(BaseModel):
    target_servers: List[str]
    traffic_percentage: Dict[str, int]

@router.get("/services/status")
async def get_service_status():
    """Get overall service status and uptime"""
    try:
        service_monitor = ServiceMonitorIntegration()
        services_status = await service_monitor.get_all_services_status()
        
        return {
            "timestamp": datetime.utcnow(),
            "services": services_status,
            "summary": {
                "total_services": len(services_status),
                "online": len([s for s in services_status if s["status"] == "online"]),
                "offline": len([s for s in services_status if s["status"] == "offline"]),
                "degraded": len([s for s in services_status if s["status"] == "degraded"])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get service status: {str(e)}")

@router.get("/services/{service_name}/metrics")
async def get_service_metrics(service_name: str):
    """Get detailed metrics for a specific service"""
    try:
        service_monitor = ServiceMonitorIntegration()
        metrics = await service_monitor.get_service_metrics(service_name)
        
        return {
            "service_name": service_name,
            "metrics": metrics,
            "current_status": metrics.get("status"),
            "response_time": metrics.get("response_time"),
            "uptime": metrics.get("uptime"),
            "error_rate": metrics.get("error_rate"),
            "throughput": metrics.get("throughput")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get service metrics: {str(e)}")

@router.post("/services/restart")
async def restart_services(request: ServiceRestartRequest, db: Session = Depends(get_db)):
    """Restart specified services"""
    try:
        automation = AutomationIntegration()
        
        restart_results = []
        for service in request.service_names:
            result = await automation.restart_service(service)
            restart_results.append({
                "service": service,
                "success": result["success"],
                "message": result["message"],
                "restart_time": result.get("restart_time")
            })
        
        # Update incident recovery data
        incident = db.query(Incident).filter(Incident.id == request.incident_id).first()
        if incident:
            recovery_data = incident.recovery_data or {}
            recovery_data.update({
                "service_restarts": restart_results,
                "restart_timestamp": datetime.utcnow().isoformat()
            })
            incident.recovery_data = recovery_data
            db.commit()
        
        successful_restarts = [r for r in restart_results if r["success"]]
        
        return {
            "message": f"Restarted {len(successful_restarts)} services successfully",
            "results": restart_results,
            "success_count": len(successful_restarts),
            "failure_count": len(restart_results) - len(successful_restarts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to restart services: {str(e)}")

@router.get("/load-balancer/status")
async def get_load_balancer_status():
    """Get load balancer configuration and traffic distribution"""
    try:
        service_monitor = ServiceMonitorIntegration()
        lb_status = await service_monitor.get_load_balancer_status()
        
        return {
            "status": lb_status["status"],
            "active_servers": lb_status["active_servers"],
            "traffic_distribution": lb_status["traffic_distribution"],
            "health_checks": lb_status["health_checks"],
            "total_requests": lb_status["total_requests"],
            "error_rate": lb_status["error_rate"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get load balancer status: {str(e)}")

@router.post("/load-balancer/configure")
async def configure_load_balancer(config: LoadBalancerConfig):
    """Configure load balancer traffic distribution"""
    try:
        automation = AutomationIntegration()
        
        result = await automation.configure_load_balancer(
            target_servers=config.target_servers,
            traffic_percentage=config.traffic_percentage
        )
        
        return {
            "message": "Load balancer configured successfully",
            "configuration": result["configuration"],
            "applied_at": result["applied_at"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to configure load balancer: {str(e)}")

@router.get("/traffic/patterns")
async def get_traffic_patterns():
    """Get traffic patterns and normal baseline"""
    try:
        service_monitor = ServiceMonitorIntegration()
        traffic_data = await service_monitor.get_traffic_patterns()
        
        return {
            "current_traffic": traffic_data["current"],
            "baseline": traffic_data["baseline"],
            "patterns": traffic_data["patterns"],
            "anomalies": traffic_data["anomalies"],
            "peak_hours": traffic_data["peak_hours"],
            "trends": traffic_data["trends"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get traffic patterns: {str(e)}")

@router.get("/monitoring/dashboard/{incident_id}")
async def get_monitoring_dashboard(incident_id: int):
    """Get comprehensive monitoring dashboard for recovery phase"""
    try:
        service_monitor = ServiceMonitorIntegration()
        dashboard_data = await service_monitor.get_recovery_dashboard(incident_id)
        
        return {
            "incident_id": incident_id,
            "system_health": dashboard_data["system_health"],
            "performance_metrics": dashboard_data["performance"],
            "security_status": dashboard_data["security"],
            "network_status": dashboard_data["network"],
            "alerts": dashboard_data["alerts"],
            "recommendations": dashboard_data["recommendations"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get monitoring dashboard: {str(e)}")

@router.post("/recovery-complete/{incident_id}")
async def mark_recovery_complete(incident_id: int, db: Session = Depends(get_db)):
    """Mark recovery phase as complete and move to post-incident"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Verify system health before marking complete
    service_monitor = ServiceMonitorIntegration()
    system_health = await service_monitor.verify_system_health()
    
    if not system_health["healthy"]:
        raise HTTPException(
            status_code=400, 
            detail=f"System not fully recovered: {system_health['issues']}"
        )
    
    # Update incident status
    incident.current_phase = "post_incident"
    incident.status = "recovered"
    
    # Update recovery data
    recovery_data = incident.recovery_data or {}
    recovery_data.update({
        "completed_at": datetime.utcnow().isoformat(),
        "system_health_verified": True,
        "services_restored": system_health["restored_services"]
    })
    incident.recovery_data = recovery_data
    
    db.commit()
    
    return {
        "message": "Recovery phase completed successfully",
        "incident_id": incident_id,
        "next_phase": "post_incident",
        "system_status": "fully_recovered"
    }

@router.get("/automation/logs/{incident_id}")
async def get_automation_logs(incident_id: int):
    """Get automation logs for recovery actions"""
    try:
        automation = AutomationIntegration()
        logs = await automation.get_recovery_logs(incident_id)
        
        return {
            "incident_id": incident_id,
            "logs": logs,
            "total_actions": len(logs),
            "successful_actions": len([log for log in logs if log["success"]]),
            "failed_actions": len([log for log in logs if not log["success"]])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get automation logs: {str(e)}")

@router.post("/run-health-check")
async def run_comprehensive_health_check():
    """Run comprehensive system health check"""
    try:
        service_monitor = ServiceMonitorIntegration()
        health_report = await service_monitor.run_health_check()
        
        return {
            "timestamp": datetime.utcnow(),
            "overall_health": health_report["overall"],
            "detailed_results": health_report["details"],
            "recommendations": health_report["recommendations"],
            "critical_issues": health_report["critical_issues"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run health check: {str(e)}")
