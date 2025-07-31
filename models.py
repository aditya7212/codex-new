from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class SolarLead:
    """Data model for solar leads"""
    company_name: str
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    website: Optional[str] = None
    business_type: Optional[str] = None  # residential, commercial, installer, etc.
    services: Optional[List[str]] = None
    description: Optional[str] = None
    source_url: Optional[str] = None
    scraped_at: datetime = None
    
    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.now()
        if self.services is None:
            self.services = []
    
    def to_dict(self) -> dict:
        """Convert to dictionary for export"""
        return {
            'company_name': self.company_name,
            'contact_person': self.contact_person,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'website': self.website,
            'business_type': self.business_type,
            'services': ', '.join(self.services) if self.services else '',
            'description': self.description,
            'source_url': self.source_url,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else ''
        }
    
    def is_valid(self) -> bool:
        """Check if lead has minimum required information"""
        return bool(self.company_name and (self.email or self.phone or self.website))


@dataclass
class ScrapingConfig:
    """Configuration for scraping operations"""
    max_pages: int = 10
    delay_between_requests: float = 1.0
    use_selenium: bool = False
    headless: bool = True
    timeout: int = 30
    max_retries: int = 3
    output_format: str = 'csv'  # csv, json, xlsx
    output_file: str = 'solar_leads.csv'
    user_agent: Optional[str] = None
    proxy: Optional[str] = None
