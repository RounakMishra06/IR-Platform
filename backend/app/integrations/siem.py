import requests
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.core.config import settings

class SIEMIntegration:
    """Integration with SIEM systems (Splunk/ELK)"""
    
    def __init__(self):
        self.splunk_config = {
            "host": settings.SPLUNK_HOST,
            "port": settings.SPLUNK_PORT,
            "username": settings.SPLUNK_USERNAME,
            "password": settings.SPLUNK_PASSWORD,
            "token": settings.SPLUNK_TOKEN
        }
        
        self.elk_config = {
            "host": settings.ELASTICSEARCH_HOST,
            "port": settings.ELASTICSEARCH_PORT,
            "username": settings.ELASTICSEARCH_USERNAME,
            "password": settings.ELASTICSEARCH_PASSWORD
        }
    
    async def get_live_alerts(self) -> List[Dict]:
        """Fetch live alerts from SIEM"""
        alerts = []
        
        # Try Splunk first
        if self.splunk_config["host"]:
            splunk_alerts = await self._get_splunk_alerts()
            alerts.extend(splunk_alerts)
        
        # Try ELK if available
        if self.elk_config["host"]:
            elk_alerts = await self._get_elk_alerts()
            alerts.extend(elk_alerts)
        
        return alerts
    
    async def _get_splunk_alerts(self) -> List[Dict]:
        """Fetch alerts from Splunk"""
        try:
            # Splunk REST API search
            search_query = '''
            search index=security earliest=-1h latest=now 
            | where severity IN ("high", "critical", "medium")
            | stats count by source_ip, dest_ip, signature, severity, _time
            | sort -_time
            | head 100
            '''
            
            # Mock data for demonstration
            return [
                {
                    "source": "splunk",
                    "type": "malware_detected",
                    "message": "Malware signature detected in network traffic",
                    "severity": "high",
                    "source_ip": "192.168.1.100",
                    "destination_ip": "10.0.0.50",
                    "timestamp": datetime.utcnow().isoformat(),
                    "signature": "TROJAN.Win32.Generic"
                },
                {
                    "source": "splunk",
                    "type": "suspicious_login",
                    "message": "Multiple failed login attempts detected",
                    "severity": "medium",
                    "source_ip": "203.0.113.45",
                    "destination_ip": "10.0.0.10",
                    "timestamp": datetime.utcnow().isoformat(),
                    "signature": "BRUTE_FORCE_LOGIN"
                }
            ]
        except Exception as e:
            print(f"Error fetching Splunk alerts: {e}")
            return []
    
    async def _get_elk_alerts(self) -> List[Dict]:
        """Fetch alerts from ELK stack"""
        try:
            # Elasticsearch query for security alerts
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"range": {"@timestamp": {"gte": "now-1h"}}},
                            {"terms": {"severity": ["high", "critical", "medium"]}}
                        ]
                    }
                },
                "sort": [{"@timestamp": {"order": "desc"}}],
                "size": 100
            }
            
            # Mock data for demonstration
            return [
                {
                    "source": "elk",
                    "type": "port_scan",
                    "message": "Port scan activity detected",
                    "severity": "medium",
                    "source_ip": "198.51.100.25",
                    "destination_ip": "10.0.0.0/24",
                    "timestamp": datetime.utcnow().isoformat(),
                    "signature": "NMAP_SCAN"
                }
            ]
        except Exception as e:
            print(f"Error fetching ELK alerts: {e}")
            return []
    
    async def get_suspicious_ips(self) -> List[Dict]:
        """Get list of suspicious IP addresses with analysis"""
        try:
            # Mock suspicious IP analysis
            return [
                {
                    "ip": "203.0.113.45",
                    "risk_score": 8.5,
                    "country": "Unknown",
                    "asn": "AS12345",
                    "threat_types": ["brute_force", "scanning"],
                    "first_seen": datetime.utcnow() - timedelta(hours=2),
                    "last_seen": datetime.utcnow(),
                    "connection_count": 150
                },
                {
                    "ip": "198.51.100.25",
                    "risk_score": 7.2,
                    "country": "RU",
                    "asn": "AS67890",
                    "threat_types": ["port_scanning"],
                    "first_seen": datetime.utcnow() - timedelta(hours=1),
                    "last_seen": datetime.utcnow() - timedelta(minutes=5),
                    "connection_count": 75
                }
            ]
        except Exception as e:
            print(f"Error analyzing suspicious IPs: {e}")
            return []
    
    async def get_traffic_analysis(self) -> Dict:
        """Get real-time traffic analysis"""
        try:
            # Mock traffic analysis data
            current_time = datetime.utcnow()
            return {
                "current": {
                    "total_traffic_mbps": 450.2,
                    "connection_count": 1250,
                    "unique_ips": 180,
                    "timestamp": current_time.isoformat()
                },
                "baseline": {
                    "avg_traffic_mbps": 320.5,
                    "avg_connections": 980,
                    "avg_unique_ips": 150
                },
                "anomalies": [
                    {
                        "type": "traffic_spike",
                        "description": "Traffic 40% above baseline",
                        "severity": "medium",
                        "detected_at": current_time.isoformat()
                    }
                ],
                "top_talkers": [
                    {"ip": "10.0.0.100", "traffic_mb": 45.2, "connections": 89},
                    {"ip": "10.0.0.101", "traffic_mb": 38.7, "connections": 67}
                ],
                "protocols": {
                    "HTTP": 35.2,
                    "HTTPS": 45.8,
                    "DNS": 8.5,
                    "SSH": 2.1,
                    "Other": 8.4
                }
            }
        except Exception as e:
            print(f"Error getting traffic analysis: {e}")
            return {}
    
    async def search_logs(self, query: str, start_time: datetime, end_time: datetime) -> List[Dict]:
        """Search logs with custom query"""
        try:
            # Mock log search results
            return [
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "firewall",
                    "message": f"Connection blocked from suspicious IP",
                    "fields": {
                        "src_ip": "203.0.113.45",
                        "dst_ip": "10.0.0.50",
                        "port": 80,
                        "action": "block"
                    }
                }
            ]
        except Exception as e:
            print(f"Error searching logs: {e}")
            return []
