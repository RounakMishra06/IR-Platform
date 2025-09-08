import requests
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.core.config import settings

class ThreatIntelIntegration:
    """Integration with Threat Intelligence feeds"""
    
    def __init__(self):
        self.virustotal_api_key = settings.VIRUSTOTAL_API_KEY
        self.alienvault_api_key = settings.ALIENVAULT_API_KEY
        self.threat_feeds = []
    
    async def search_indicator(self, indicator: str) -> Optional[Dict]:
        """Search for an indicator in threat intelligence feeds"""
        try:
            # Try different sources
            vt_result = await self._search_virustotal(indicator)
            if vt_result:
                return vt_result
                
            av_result = await self._search_alienvault(indicator)
            if av_result:
                return av_result
                
            # Mock result if no API keys configured
            if not self.virustotal_api_key and not self.alienvault_api_key:
                return self._mock_threat_intel_result(indicator)
                
            return None
            
        except Exception as e:
            print(f"Error searching indicator {indicator}: {e}")
            return None
    
    async def _search_virustotal(self, indicator: str) -> Optional[Dict]:
        """Search VirusTotal for indicator"""
        if not self.virustotal_api_key:
            return None
            
        try:
            headers = {"x-apikey": self.virustotal_api_key}
            
            # Determine indicator type
            if self._is_ip(indicator):
                url = f"https://www.virustotal.com/api/v3/ip_addresses/{indicator}"
            elif self._is_domain(indicator):
                url = f"https://www.virustotal.com/api/v3/domains/{indicator}"
            elif self._is_hash(indicator):
                url = f"https://www.virustotal.com/api/v3/files/{indicator}"
            else:
                return None
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                
                return {
                    "type": self._get_indicator_type(indicator),
                    "source": "virustotal",
                    "malicious": stats.get("malicious", 0) > 0,
                    "score": min(stats.get("malicious", 0) * 2, 10),  # Scale to 0-10
                    "engines_detected": stats.get("malicious", 0),
                    "total_engines": sum(stats.values()),
                    "first_seen": data.get("data", {}).get("attributes", {}).get("first_submission_date"),
                    "last_seen": data.get("data", {}).get("attributes", {}).get("last_modification_date"),
                    "sources": ["virustotal"]
                }
            
            return None
            
        except Exception as e:
            print(f"Error searching VirusTotal: {e}")
            return None
    
    async def _search_alienvault(self, indicator: str) -> Optional[Dict]:
        """Search AlienVault OTX for indicator"""
        if not self.alienvault_api_key:
            return None
            
        try:
            headers = {"X-OTX-API-KEY": self.alienvault_api_key}
            
            # Determine API endpoint based on indicator type
            if self._is_ip(indicator):
                url = f"https://otx.alienvault.com/api/v1/indicators/IPv4/{indicator}/general"
            elif self._is_domain(indicator):
                url = f"https://otx.alienvault.com/api/v1/indicators/domain/{indicator}/general"
            elif self._is_hash(indicator):
                url = f"https://otx.alienvault.com/api/v1/indicators/file/{indicator}/general"
            else:
                return None
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                pulse_count = data.get("pulse_info", {}).get("count", 0)
                
                return {
                    "type": self._get_indicator_type(indicator),
                    "source": "alienvault",
                    "malicious": pulse_count > 0,
                    "score": min(pulse_count, 10),  # Scale to 0-10
                    "pulse_count": pulse_count,
                    "first_seen": data.get("base_indicator", {}).get("first_seen"),
                    "last_seen": data.get("base_indicator", {}).get("last_seen"),
                    "sources": ["alienvault"]
                }
            
            return None
            
        except Exception as e:
            print(f"Error searching AlienVault: {e}")
            return None
    
    def _mock_threat_intel_result(self, indicator: str) -> Dict:
        """Generate mock threat intelligence result for demo"""
        import random
        
        malicious_probability = 0.3  # 30% chance of being malicious
        is_malicious = random.random() < malicious_probability
        
        return {
            "type": self._get_indicator_type(indicator),
            "source": "mock_threat_feed",
            "malicious": is_malicious,
            "score": random.randint(7, 10) if is_malicious else random.randint(0, 3),
            "confidence": random.randint(7, 10) if is_malicious else random.randint(3, 6),
            "first_seen": (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat(),
            "last_seen": (datetime.utcnow() - timedelta(hours=random.randint(1, 24))).isoformat(),
            "sources": ["mock_feed_1", "mock_feed_2"],
            "tags": ["malware", "trojan"] if is_malicious else ["benign", "legitimate"]
        }
    
    async def get_latest_feed(self) -> Dict:
        """Get latest threat intelligence feed updates"""
        try:
            # Mock threat feed data
            return {
                "last_updated": datetime.utcnow().isoformat(),
                "new_indicators": 245,
                "total_indicators": 15420,
                "top_threats": [
                    {
                        "name": "Emotet Banking Trojan",
                        "type": "malware",
                        "severity": "high",
                        "iocs": ["192.0.2.100", "example-malware.com", "abc123def456"]
                    },
                    {
                        "name": "APT28 Campaign",
                        "type": "apt_group",
                        "severity": "critical",
                        "iocs": ["203.0.113.200", "fake-update.net", "def456ghi789"]
                    }
                ],
                "trending_malware": [
                    {"name": "Emotet", "growth": 25},
                    {"name": "TrickBot", "growth": 18},
                    {"name": "Ryuk", "growth": 12}
                ],
                "feed_stats": {
                    "ips": 8950,
                    "domains": 4200,
                    "hashes": 2270,
                    "urls": 1500
                }
            }
        except Exception as e:
            print(f"Error getting threat feed: {e}")
            return {}
    
    async def bulk_search_indicators(self, indicators: List[str]) -> List[Dict]:
        """Search multiple indicators in batch"""
        results = []
        
        for indicator in indicators:
            result = await self.search_indicator(indicator)
            if result:
                results.append({
                    "indicator": indicator,
                    "data": result
                })
        
        return results
    
    async def get_ioc_context(self, indicator: str) -> Dict:
        """Get additional context for an IOC"""
        try:
            # Mock IOC context
            return {
                "indicator": indicator,
                "type": self._get_indicator_type(indicator),
                "associated_campaigns": [
                    {
                        "name": "APT28 Phishing Campaign",
                        "first_seen": "2024-01-10",
                        "target_sectors": ["Government", "Defense"]
                    }
                ],
                "related_indicators": [
                    "198.51.100.30",
                    "malware-c2.example.com",
                    "fedcba098765"
                ],
                "attack_techniques": [
                    {
                        "technique": "T1566.001",
                        "name": "Spearphishing Attachment",
                        "tactic": "Initial Access"
                    }
                ],
                "geographic_distribution": {
                    "US": 45,
                    "EU": 30,
                    "APAC": 25
                }
            }
        except Exception as e:
            print(f"Error getting IOC context: {e}")
            return {}
    
    def _is_ip(self, indicator: str) -> bool:
        """Check if indicator is an IP address"""
        import ipaddress
        try:
            ipaddress.ip_address(indicator)
            return True
        except ValueError:
            return False
    
    def _is_domain(self, indicator: str) -> bool:
        """Check if indicator is a domain"""
        import re
        domain_pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        return re.match(domain_pattern, indicator) is not None
    
    def _is_hash(self, indicator: str) -> bool:
        """Check if indicator is a file hash"""
        hash_lengths = [32, 40, 64, 128]  # MD5, SHA1, SHA256, SHA512
        return len(indicator) in hash_lengths and all(c in '0123456789abcdefABCDEF' for c in indicator)
    
    def _get_indicator_type(self, indicator: str) -> str:
        """Determine the type of indicator"""
        if self._is_ip(indicator):
            return "ip"
        elif self._is_domain(indicator):
            return "domain"
        elif self._is_hash(indicator):
            return "hash"
        else:
            return "unknown"
