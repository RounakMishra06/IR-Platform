import requests
import json
from typing import List, Dict, Optional
from datetime import datetime
from app.core.config import settings

class FirewallIntegration:
    """Integration with Firewall/IPS systems for containment actions"""
    
    def __init__(self):
        self.api_url = settings.FIREWALL_API_URL
        self.api_key = settings.FIREWALL_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def block_ip(self, ip_address: str, reason: str) -> bool:
        """Block an IP address on the firewall"""
        try:
            if not self.api_url:
                # Mock successful blocking for demo
                print(f"Mock: Blocking IP {ip_address} - Reason: {reason}")
                return True
            
            payload = {
                "ip_address": ip_address,
                "action": "block",
                "reason": reason,
                "duration": "permanent",  # or specify time-based blocking
                "timestamp": datetime.utcnow().isoformat()
            }
            
            response = requests.post(
                f"{self.api_url}/api/firewall/block",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Error blocking IP {ip_address}: {e}")
            return False
    
    async def unblock_ip(self, ip_address: str) -> bool:
        """Unblock an IP address"""
        try:
            if not self.api_url:
                # Mock successful unblocking for demo
                print(f"Mock: Unblocking IP {ip_address}")
                return True
            
            payload = {
                "ip_address": ip_address,
                "action": "unblock",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            response = requests.post(
                f"{self.api_url}/api/firewall/unblock",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Error unblocking IP {ip_address}: {e}")
            return False
    
    async def get_connection_stats(self) -> Dict:
        """Get current connection statistics"""
        try:
            if not self.api_url:
                # Mock connection stats
                return {
                    "active": 1250,
                    "blocked": 45,
                    "rate_limiting": True,
                    "total_rules": 128,
                    "last_updated": datetime.utcnow().isoformat()
                }
            
            response = requests.get(
                f"{self.api_url}/api/firewall/stats",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
                
        except Exception as e:
            print(f"Error getting connection stats: {e}")
            return {}
    
    async def get_blocked_ips(self) -> List[Dict]:
        """Get list of currently blocked IPs"""
        try:
            if not self.api_url:
                # Mock blocked IPs list
                return [
                    {
                        "ip": "203.0.113.45",
                        "blocked_at": "2024-01-15T10:30:00Z",
                        "reason": "Brute force attack",
                        "rule_id": "fw-001"
                    },
                    {
                        "ip": "198.51.100.25", 
                        "blocked_at": "2024-01-15T11:45:00Z",
                        "reason": "Port scanning",
                        "rule_id": "fw-002"
                    }
                ]
            
            response = requests.get(
                f"{self.api_url}/api/firewall/blocked-ips",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("blocked_ips", [])
            else:
                return []
                
        except Exception as e:
            print(f"Error getting blocked IPs: {e}")
            return []
    
    async def create_firewall_rule(self, rule_config: Dict) -> Dict:
        """Create a new firewall rule"""
        try:
            if not self.api_url:
                # Mock rule creation
                return {
                    "success": True,
                    "rule_id": f"fw-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                    "message": "Rule created successfully"
                }
            
            response = requests.post(
                f"{self.api_url}/api/firewall/rules",
                json=rule_config,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 201:
                return {
                    "success": True,
                    "rule_id": response.json().get("rule_id"),
                    "message": "Rule created successfully"
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to create rule: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error creating rule: {e}"
            }
    
    async def enable_rate_limiting(self, config: Dict) -> bool:
        """Enable rate limiting"""
        try:
            if not self.api_url:
                # Mock rate limiting enable
                print(f"Mock: Enabling rate limiting with config: {config}")
                return True
            
            response = requests.post(
                f"{self.api_url}/api/firewall/rate-limiting",
                json=config,
                headers=self.headers,
                timeout=30
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Error enabling rate limiting: {e}")
            return False
    
    async def get_containment_logs(self, incident_id: int) -> List[Dict]:
        """Get logs of containment actions for specific incident"""
        try:
            # Mock containment logs
            return [
                {
                    "timestamp": "2024-01-15T10:30:00Z",
                    "action": "block_ip",
                    "target": "203.0.113.45",
                    "result": "success",
                    "details": "IP blocked due to brute force attack",
                    "user": "system"
                },
                {
                    "timestamp": "2024-01-15T10:31:15Z",
                    "action": "enable_rate_limiting",
                    "target": "login_endpoint",
                    "result": "success", 
                    "details": "Rate limiting enabled: 5 requests per minute",
                    "user": "admin"
                },
                {
                    "timestamp": "2024-01-15T10:32:30Z",
                    "action": "block_ip",
                    "target": "198.51.100.25",
                    "result": "success",
                    "details": "IP blocked due to port scanning",
                    "user": "system"
                }
            ]
            
        except Exception as e:
            print(f"Error getting containment logs: {e}")
            return []
    
    async def get_traffic_rules(self) -> List[Dict]:
        """Get current traffic filtering rules"""
        try:
            if not self.api_url:
                # Mock traffic rules
                return [
                    {
                        "rule_id": "fw-001",
                        "type": "block",
                        "source": "203.0.113.45",
                        "destination": "any",
                        "port": "any",
                        "protocol": "any",
                        "created_at": "2024-01-15T10:30:00Z",
                        "status": "active"
                    },
                    {
                        "rule_id": "fw-002",
                        "type": "rate_limit",
                        "source": "any",
                        "destination": "10.0.0.10:80",
                        "limit": "100/minute",
                        "protocol": "HTTP",
                        "created_at": "2024-01-15T10:31:00Z",
                        "status": "active"
                    }
                ]
            
            response = requests.get(
                f"{self.api_url}/api/firewall/rules",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("rules", [])
            else:
                return []
                
        except Exception as e:
            print(f"Error getting traffic rules: {e}")
            return []
    
    async def bulk_block_ips(self, ip_list: List[str], reason: str) -> Dict:
        """Block multiple IPs in bulk"""
        results = []
        successful_blocks = 0
        
        for ip in ip_list:
            success = await self.block_ip(ip, reason)
            results.append({
                "ip": ip,
                "success": success,
                "timestamp": datetime.utcnow().isoformat()
            })
            if success:
                successful_blocks += 1
        
        return {
            "total_ips": len(ip_list),
            "successful_blocks": successful_blocks,
            "failed_blocks": len(ip_list) - successful_blocks,
            "results": results
        }
