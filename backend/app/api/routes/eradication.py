from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from app.core.database import get_db
from app.integrations.threat_intel import ThreatIntelIntegration
from app.integrations.log_analysis import LogAnalysisIntegration
from app.integrations.vulnerability import VulnerabilityIntegration
from app.models.database import Incident, ThreatIndicator
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class IOCSearchRequest(BaseModel):
    indicators: List[str]
    incident_id: int

class PatchRequest(BaseModel):
    vulnerability_ids: List[str]
    incident_id: int

@router.get("/incident/{incident_id}/analysis")
async def get_log_analysis(incident_id: int, db: Session = Depends(get_db)):
    """Get log analysis dashboard for the incident"""
    try:
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        
        log_analyzer = LogAnalysisIntegration()
        
        # Get relevant time range from incident
        start_time = incident.created_at
        end_time = datetime.utcnow()
        
        # Analyze logs for attack patterns
        analysis_results = await log_analyzer.analyze_incident_logs(
            incident_id=incident_id,
            start_time=start_time,
            end_time=end_time
        )
        
        return {
            "incident_id": incident_id,
            "analysis": analysis_results,
            "summary": {
                "total_events": analysis_results.get("total_events", 0),
                "malicious_events": analysis_results.get("malicious_events", 0),
                "attack_vectors": analysis_results.get("attack_vectors", []),
                "affected_systems": analysis_results.get("affected_systems", [])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze logs: {str(e)}")

@router.post("/search-iocs")
async def search_threat_indicators(request: IOCSearchRequest, db: Session = Depends(get_db)):
    """Search threat intelligence for indicators of compromise"""
    try:
        threat_intel = ThreatIntelIntegration()
        
        ioc_results = []
        for indicator in request.indicators:
            # Search in threat intelligence feeds
            intel_data = await threat_intel.search_indicator(indicator)
            
            if intel_data and intel_data.get("malicious", False):
                # Store in database
                threat_indicator = ThreatIndicator(
                    incident_id=request.incident_id,
                    indicator_type=intel_data["type"],
                    value=indicator,
                    source=intel_data["source"],
                    threat_score=intel_data.get("score", 0),
                    indicator_metadata=intel_data
                )
                db.add(threat_indicator)
                ioc_results.append({
                    "indicator": indicator,
                    "malicious": True,
                    "sources": intel_data.get("sources", []),
                    "threat_score": intel_data.get("score", 0),
                    "first_seen": intel_data.get("first_seen"),
                    "last_seen": intel_data.get("last_seen")
                })
        
        db.commit()
        
        return {
            "incident_id": request.incident_id,
            "searched_indicators": len(request.indicators),
            "malicious_indicators": len(ioc_results),
            "results": ioc_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search IOCs: {str(e)}")

@router.get("/vulnerabilities/{incident_id}")
async def get_vulnerability_status(incident_id: int):
    """Get vulnerability and patch status"""
    try:
        vuln_scanner = VulnerabilityIntegration()
        
        # Get incident-related vulnerabilities
        vulnerabilities = await vuln_scanner.get_incident_vulnerabilities(incident_id)
        
        # Get patch status
        patch_status = await vuln_scanner.get_patch_status()
        
        return {
            "incident_id": incident_id,
            "vulnerabilities": {
                "critical": [v for v in vulnerabilities if v["severity"] == "critical"],
                "high": [v for v in vulnerabilities if v["severity"] == "high"],
                "medium": [v for v in vulnerabilities if v["severity"] == "medium"],
                "low": [v for v in vulnerabilities if v["severity"] == "low"]
            },
            "patch_status": patch_status,
            "summary": {
                "total_vulnerabilities": len(vulnerabilities),
                "patched": len([v for v in vulnerabilities if v.get("patched", False)]),
                "pending_patches": len([v for v in vulnerabilities if not v.get("patched", False)])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get vulnerability status: {str(e)}")

@router.post("/apply-patches")
async def apply_patches(request: PatchRequest, db: Session = Depends(get_db)):
    """Apply patches for vulnerabilities"""
    try:
        vuln_scanner = VulnerabilityIntegration()
        
        patch_results = []
        for vuln_id in request.vulnerability_ids:
            result = await vuln_scanner.apply_patch(vuln_id)
            patch_results.append({
                "vulnerability_id": vuln_id,
                "success": result["success"],
                "message": result["message"]
            })
        
        # Update incident data
        incident = db.query(Incident).filter(Incident.id == request.incident_id).first()
        if incident:
            eradication_data = incident.eradication_data or {}
            eradication_data.update({
                "patches_applied": patch_results,
                "patch_timestamp": datetime.utcnow().isoformat()
            })
            incident.eradication_data = eradication_data
            db.commit()
        
        successful_patches = [r for r in patch_results if r["success"]]
        
        return {
            "message": f"Applied {len(successful_patches)} patches successfully",
            "results": patch_results,
            "success_count": len(successful_patches),
            "failure_count": len(patch_results) - len(successful_patches)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to apply patches: {str(e)}")

@router.get("/malware-analysis/{incident_id}")
async def get_malware_analysis(incident_id: int):
    """Get malware analysis results"""
    try:
        log_analyzer = LogAnalysisIntegration()
        malware_analysis = await log_analyzer.analyze_malware(incident_id)
        
        return {
            "incident_id": incident_id,
            "malware_detected": malware_analysis.get("detected", False),
            "malware_families": malware_analysis.get("families", []),
            "file_hashes": malware_analysis.get("hashes", []),
            "persistence_mechanisms": malware_analysis.get("persistence", []),
            "network_communications": malware_analysis.get("network", []),
            "recommended_actions": malware_analysis.get("recommendations", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze malware: {str(e)}")

@router.post("/eradication-complete/{incident_id}")
async def mark_eradication_complete(incident_id: int, db: Session = Depends(get_db)):
    """Mark eradication phase as complete and move to recovery"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Update incident status
    incident.current_phase = "recovery"
    incident.status = "eradicated"
    
    # Update eradication data
    eradication_data = incident.eradication_data or {}
    eradication_data.update({
        "completed_at": datetime.utcnow().isoformat(),
        "threats_removed": True,
        "vulnerabilities_patched": True
    })
    incident.eradication_data = eradication_data
    
    db.commit()
    
    return {
        "message": "Eradication phase completed successfully",
        "incident_id": incident_id,
        "next_phase": "recovery"
    }

@router.get("/threat-feed")
async def get_threat_intelligence_feed():
    """Get latest threat intelligence feed"""
    try:
        threat_intel = ThreatIntelIntegration()
        feed_data = await threat_intel.get_latest_feed()
        
        return {
            "feed_updated": feed_data.get("last_updated"),
            "new_indicators": feed_data.get("new_indicators", 0),
            "total_indicators": feed_data.get("total_indicators", 0),
            "top_threats": feed_data.get("top_threats", []),
            "trending_malware": feed_data.get("trending_malware", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get threat feed: {str(e)}")
