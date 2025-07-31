"""
Configuration settings for solar leads scraper
"""

import os
from typing import Dict, List

# Default scraping targets and their configurations
SCRAPING_TARGETS = {
    'yellowpages': {
        'base_url': 'https://www.yellowpages.com',
        'search_terms': [
            'solar energy',
            'solar installation',
            'solar panels',
            'renewable energy',
            'solar contractors'
        ],
        'selectors': {
            'listing': 'div.result',
            'company_name': 'a.business-name',
            'phone': 'div.phones',
            'address': 'div.street-address',
            'locality': 'div.locality',
            'website': 'a.track-visit-website',
            'description': 'p.snippet'
        }
    },
    'yelp': {
        'base_url': 'https://www.yelp.com',
        'search_terms': [
            'solar installation',
            'solar energy',
            'solar panels'
        ],
        'selectors': {
            'listing': '[data-testid="serp-ia-card"]',
            'company_name': 'h3 a',
            'phone': '[data-testid="phone-number"]',
            'address': '[data-testid="address"]',
            'website': 'a[href*="biz_redir"]'
        }
    },
    'bbb': {
        'base_url': 'https://www.bbb.org',
        'search_terms': [
            'solar energy',
            'solar installation'
        ]
    },
    'angie': {
        'base_url': 'https://www.angi.com',
        'search_terms': [
            'solar panel installation',
            'solar energy systems'
        ]
    }
}

# Solar-related keywords for filtering
SOLAR_KEYWORDS = [
    'solar', 'photovoltaic', 'pv', 'renewable energy', 'solar panel',
    'solar installation', 'solar installer', 'solar energy', 'solar power',
    'solar system', 'solar contractor', 'clean energy', 'green energy',
    'solar roofing', 'solar electric', 'solar thermal', 'solar heating',
    'grid-tie', 'off-grid', 'battery storage', 'inverter', 'solar farm',
    'commercial solar', 'residential solar', 'solar maintenance',
    'solar repair', 'solar design', 'solar consultation'
]

# Business type classifications
BUSINESS_TYPES = {
    'installer': ['install', 'contractor', 'construction'],
    'manufacturer': ['manufactur', 'produc', 'factory'],
    'distributor': ['distribut', 'wholesale', 'supply'],
    'consultant': ['consult', 'design', 'engineer'],
    'maintenance': ['maintenance', 'repair', 'service'],
    'retailer': ['retail', 'store', 'shop']
}

# User agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
]

# Rate limiting settings
RATE_LIMITS = {
    'yellowpages': {'requests_per_minute': 30, 'delay_range': (1, 3)},
    'yelp': {'requests_per_minute': 20, 'delay_range': (2, 4)},
    'googlemaps': {'requests_per_minute': 10, 'delay_range': (3, 6)},
    'default': {'requests_per_minute': 30, 'delay_range': (1, 2)}
}

# Output field mappings
OUTPUT_FIELDS = [
    'company_name',
    'contact_person',
    'email',
    'phone',
    'address',
    'city',
    'state',
    'zip_code',
    'website',
    'business_type',
    'services',
    'description',
    'source_url',
    'scraped_at'
]

# Environment variables
def get_env_config():
    """Get configuration from environment variables"""
    return {
        'proxy_url': os.getenv('PROXY_URL'),
        'user_agent': os.getenv('USER_AGENT'),
        'output_dir': os.getenv('OUTPUT_DIR', './output'),
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'max_workers': int(os.getenv('MAX_WORKERS', '4')),
        'timeout': int(os.getenv('REQUEST_TIMEOUT', '30'))
    }

# State abbreviations for normalization
US_STATES = {
    'alabama': 'AL', 'alaska': 'AK', 'arizona': 'AZ', 'arkansas': 'AR',
    'california': 'CA', 'colorado': 'CO', 'connecticut': 'CT', 'delaware': 'DE',
    'florida': 'FL', 'georgia': 'GA', 'hawaii': 'HI', 'idaho': 'ID',
    'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA', 'kansas': 'KS',
    'kentucky': 'KY', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD',
    'massachusetts': 'MA', 'michigan': 'MI', 'minnesota': 'MN', 'mississippi': 'MS',
    'missouri': 'MO', 'montana': 'MT', 'nebraska': 'NE', 'nevada': 'NV',
    'new hampshire': 'NH', 'new jersey': 'NJ', 'new mexico': 'NM', 'new york': 'NY',
    'north carolina': 'NC', 'north dakota': 'ND', 'ohio': 'OH', 'oklahoma': 'OK',
    'oregon': 'OR', 'pennsylvania': 'PA', 'rhode island': 'RI', 'south carolina': 'SC',
    'south dakota': 'SD', 'tennessee': 'TN', 'texas': 'TX', 'utah': 'UT',
    'vermont': 'VT', 'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV',
    'wisconsin': 'WI', 'wyoming': 'WY'
}

# Major cities for targeted scraping
MAJOR_CITIES = [
    'New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX',
    'Phoenix, AZ', 'Philadelphia, PA', 'San Antonio, TX', 'San Diego, CA',
    'Dallas, TX', 'San Jose, CA', 'Austin, TX', 'Jacksonville, FL',
    'Fort Worth, TX', 'Columbus, OH', 'Charlotte, NC', 'San Francisco, CA',
    'Indianapolis, IN', 'Seattle, WA', 'Denver, CO', 'Washington, DC',
    'Boston, MA', 'El Paso, TX', 'Nashville, TN', 'Detroit, MI',
    'Oklahoma City, OK', 'Portland, OR', 'Las Vegas, NV', 'Memphis, TN',
    'Louisville, KY', 'Baltimore, MD', 'Milwaukee, WI', 'Albuquerque, NM',
    'Tucson, AZ', 'Fresno, CA', 'Sacramento, CA', 'Mesa, AZ',
    'Kansas City, MO', 'Atlanta, GA', 'Long Beach, CA', 'Colorado Springs, CO',
    'Raleigh, NC', 'Miami, FL', 'Virginia Beach, VA', 'Omaha, NE',
    'Oakland, CA', 'Minneapolis, MN', 'Tulsa, OK', 'Arlington, TX',
    'Tampa, FL', 'New Orleans, LA'
]
