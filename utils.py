import re
import time
import random
from typing import List, Optional
from urllib.parse import urljoin, urlparse
import pandas as pd
import json
from models import SolarLead


def clean_text(text: str) -> str:
    """Clean and normalize text data"""
    if not text:
        return ""
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\-\.\,\(\)\@]', '', text)
    return text


def extract_email(text: str) -> Optional[str]:
    """Extract email address from text"""
    if not text:
        return None
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text"""
    if not text:
        return None
    # Common phone patterns
    patterns = [
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\+1[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            # Clean up the phone number
            phone = re.sub(r'[^\d]', '', match.group(0))
            if len(phone) == 10:
                return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
            elif len(phone) == 11 and phone.startswith('1'):
                return f"({phone[1:4]}) {phone[4:7]}-{phone[7:]}"
    return None


def is_solar_related(text: str) -> bool:
    """Check if text contains solar-related keywords"""
    if not text:
        return False
    
    solar_keywords = [
        'solar', 'photovoltaic', 'pv', 'renewable energy', 'solar panel',
        'solar installation', 'solar installer', 'solar energy', 'solar power',
        'solar system', 'solar contractor', 'clean energy', 'green energy'
    ]
    
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in solar_keywords)


def normalize_url(url: str, base_url: str = None) -> str:
    """Normalize and validate URL"""
    if not url:
        return ""
    
    if base_url and not url.startswith(('http://', 'https://')):
        url = urljoin(base_url, url)
    
    # Ensure URL has protocol
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return url


def random_delay(min_delay: float = 0.5, max_delay: float = 2.0):
    """Add random delay to avoid being blocked"""
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)


def save_leads(leads: List[SolarLead], filename: str, format: str = 'csv'):
    """Save leads to file in specified format"""
    if not leads:
        print("No leads to save")
        return
    
    # Convert leads to dictionaries
    leads_data = [lead.to_dict() for lead in leads]
    
    if format.lower() == 'csv':
        df = pd.DataFrame(leads_data)
        df.to_csv(filename, index=False)
        print(f"Saved {len(leads)} leads to {filename}")
    
    elif format.lower() == 'json':
        with open(filename, 'w') as f:
            json.dump(leads_data, f, indent=2, default=str)
        print(f"Saved {len(leads)} leads to {filename}")
    
    elif format.lower() == 'xlsx':
        df = pd.DataFrame(leads_data)
        df.to_excel(filename, index=False)
        print(f"Saved {len(leads)} leads to {filename}")
    
    else:
        raise ValueError(f"Unsupported format: {format}")


def deduplicate_leads(leads: List[SolarLead]) -> List[SolarLead]:
    """Remove duplicate leads based on company name and contact info"""
    seen = set()
    unique_leads = []
    
    for lead in leads:
        # Create a key based on company name and primary contact method
        key_parts = [lead.company_name.lower().strip()]
        if lead.email:
            key_parts.append(lead.email.lower())
        elif lead.phone:
            key_parts.append(re.sub(r'[^\d]', '', lead.phone))
        elif lead.website:
            key_parts.append(lead.website.lower())
        
        key = '|'.join(key_parts)
        
        if key not in seen:
            seen.add(key)
            unique_leads.append(lead)
    
    return unique_leads


def validate_lead(lead: SolarLead) -> bool:
    """Validate lead data quality"""
    if not lead.company_name or len(lead.company_name.strip()) < 2:
        return False
    
    # Must have at least one contact method
    if not any([lead.email, lead.phone, lead.website]):
        return False
    
    # Validate email format if present
    if lead.email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', lead.email):
        return False
    
    return True
