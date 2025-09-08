from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./incident_response.db"
    
    # SIEM Integration
    SPLUNK_HOST: Optional[str] = None
    SPLUNK_PORT: int = 8089
    SPLUNK_USERNAME: Optional[str] = None
    SPLUNK_PASSWORD: Optional[str] = None
    SPLUNK_TOKEN: Optional[str] = None
    
    # ELK Integration
    ELASTICSEARCH_HOST: Optional[str] = "localhost"
    ELASTICSEARCH_PORT: int = 9200
    ELASTICSEARCH_USERNAME: Optional[str] = None
    ELASTICSEARCH_PASSWORD: Optional[str] = None
    
    # Firewall API
    FIREWALL_API_URL: Optional[str] = None
    FIREWALL_API_KEY: Optional[str] = None
    
    # Threat Intelligence
    VIRUSTOTAL_API_KEY: Optional[str] = None
    ALIENVAULT_API_KEY: Optional[str] = None
    
    # Automation
    ANSIBLE_PLAYBOOK_PATH: str = "/opt/ansible/playbooks"
    
    # Application
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis (for background tasks)
    REDIS_URL: str = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"

settings = Settings()
