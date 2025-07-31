import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import time
import logging
from typing import List, Optional
from urllib.parse import urljoin, urlparse
import re

from models import SolarLead, ScrapingConfig
from utils import (
    clean_text, extract_email, extract_phone, is_solar_related,
    normalize_url, random_delay, validate_lead
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SolarLeadScraper:
    """Main scraper class for solar leads"""
    
    def __init__(self, config: ScrapingConfig = None):
        self.config = config or ScrapingConfig()
        self.session = requests.Session()
        self.ua = UserAgent()
        self.driver = None
        self._setup_session()
    
    def _setup_session(self):
        """Setup requests session with headers"""
        headers = {
            'User-Agent': self.config.user_agent or self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.session.headers.update(headers)
        
        if self.config.proxy:
            self.session.proxies = {'http': self.config.proxy, 'https': self.config.proxy}
    
    def _get_selenium_driver(self):
        """Initialize Selenium WebDriver"""
        if self.driver is None:
            chrome_options = Options()
            if self.config.headless:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument(f'--user-agent={self.ua.random}')
            
            self.driver = webdriver.Chrome(
                ChromeDriverManager().install(),
                options=chrome_options
            )
            self.driver.set_page_load_timeout(self.config.timeout)
        
        return self.driver
    
    def scrape_yellow_pages(self, search_term: str = "solar energy", location: str = "United States") -> List[SolarLead]:
        """Scrape Yellow Pages for solar companies"""
        leads = []
        base_url = "https://www.yellowpages.com"
        
        try:
            # Construct search URL
            search_url = f"{base_url}/search?search_terms={search_term}&geo_location_terms={location}"
            logger.info(f"Scraping Yellow Pages: {search_url}")
            
            for page in range(1, self.config.max_pages + 1):
                url = f"{search_url}&page={page}"
                response = self.session.get(url, timeout=self.config.timeout)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                listings = soup.find_all('div', class_='result')
                
                if not listings:
                    break
                
                for listing in listings:
                    lead = self._parse_yellow_pages_listing(listing, base_url)
                    if lead and validate_lead(lead):
                        leads.append(lead)
                
                random_delay(self.config.delay_between_requests)
                
        except Exception as e:
            logger.error(f"Error scraping Yellow Pages: {e}")
        
        return leads
    
    def _parse_yellow_pages_listing(self, listing, base_url: str) -> Optional[SolarLead]:
        """Parse individual Yellow Pages listing"""
        try:
            # Company name
            name_elem = listing.find('a', class_='business-name')
            if not name_elem:
                return None
            
            company_name = clean_text(name_elem.get_text())
            
            # Check if solar-related
            description = ""
            desc_elem = listing.find('p', class_='snippet')
            if desc_elem:
                description = clean_text(desc_elem.get_text())
            
            if not is_solar_related(company_name + " " + description):
                return None
            
            # Extract contact info
            phone = None
            phone_elem = listing.find('div', class_='phones')
            if phone_elem:
                phone = extract_phone(phone_elem.get_text())
            
            # Address
            address = ""
            address_elem = listing.find('div', class_='street-address')
            if address_elem:
                address = clean_text(address_elem.get_text())
            
            # City, state
            city, state = "", ""
            locality_elem = listing.find('div', class_='locality')
            if locality_elem:
                locality_text = clean_text(locality_elem.get_text())
                parts = locality_text.split(',')
                if len(parts) >= 2:
                    city = parts[0].strip()
                    state = parts[1].strip()
            
            # Website
            website = None
            website_elem = listing.find('a', class_='track-visit-website')
            if website_elem:
                website = website_elem.get('href')
                if website:
                    website = normalize_url(website)
            
            return SolarLead(
                company_name=company_name,
                phone=phone,
                address=address,
                city=city,
                state=state,
                website=website,
                description=description,
                source_url=base_url,
                business_type="solar_company"
            )
            
        except Exception as e:
            logger.error(f"Error parsing Yellow Pages listing: {e}")
            return None
    
    def scrape_solar_power_world(self) -> List[SolarLead]:
        """Scrape Solar Power World directory"""
        leads = []
        base_url = "https://www.solarpowerworldonline.com"
        
        try:
            # This would need to be adapted based on the actual site structure
            directory_url = f"{base_url}/solar-installer-directory/"
            logger.info(f"Scraping Solar Power World: {directory_url}")
            
            if self.config.use_selenium:
                driver = self._get_selenium_driver()
                driver.get(directory_url)
                time.sleep(3)
                
                # Look for company listings
                listings = driver.find_elements(By.CSS_SELECTOR, '.company-listing, .installer-listing')
                
                for listing in listings:
                    lead = self._parse_solar_world_listing(listing)
                    if lead and validate_lead(lead):
                        leads.append(lead)
            
        except Exception as e:
            logger.error(f"Error scraping Solar Power World: {e}")
        
        return leads
    
    def _parse_solar_world_listing(self, listing) -> Optional[SolarLead]:
        """Parse Solar Power World listing"""
        try:
            # This would need to be customized based on actual HTML structure
            company_name = listing.find_element(By.CSS_SELECTOR, '.company-name, h3, h4').text
            company_name = clean_text(company_name)
            
            if not company_name:
                return None
            
            # Extract other details
            description = ""
            try:
                desc_elem = listing.find_element(By.CSS_SELECTOR, '.description, p')
                description = clean_text(desc_elem.text)
            except:
                pass
            
            # Contact info
            phone = extract_phone(listing.text)
            email = extract_email(listing.text)
            
            # Website
            website = None
            try:
                website_elem = listing.find_element(By.CSS_SELECTOR, 'a[href*="http"]')
                website = normalize_url(website_elem.get_attribute('href'))
            except:
                pass
            
            return SolarLead(
                company_name=company_name,
                email=email,
                phone=phone,
                website=website,
                description=description,
                source_url="https://www.solarpowerworldonline.com",
                business_type="solar_installer"
            )
            
        except Exception as e:
            logger.error(f"Error parsing Solar Power World listing: {e}")
            return None
    
    def scrape_google_maps(self, query: str = "solar installation companies", location: str = "United States") -> List[SolarLead]:
        """Scrape Google Maps for solar companies (requires Selenium)"""
        leads = []
        
        if not self.config.use_selenium:
            logger.warning("Google Maps scraping requires Selenium. Enable use_selenium in config.")
            return leads
        
        try:
            driver = self._get_selenium_driver()
            search_url = f"https://www.google.com/maps/search/{query}+{location}"
            logger.info(f"Scraping Google Maps: {search_url}")
            
            driver.get(search_url)
            time.sleep(5)
            
            # Scroll to load more results
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Find business listings
            listings = driver.find_elements(By.CSS_SELECTOR, '[data-result-index]')
            
            for listing in listings[:20]:  # Limit to first 20 results
                try:
                    listing.click()
                    time.sleep(2)
                    
                    lead = self._parse_google_maps_listing(driver)
                    if lead and validate_lead(lead):
                        leads.append(lead)
                    
                except Exception as e:
                    logger.error(f"Error processing Google Maps listing: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error scraping Google Maps: {e}")
        
        return leads
    
    def _parse_google_maps_listing(self, driver) -> Optional[SolarLead]:
        """Parse Google Maps business listing"""
        try:
            # Company name
            name_elem = driver.find_element(By.CSS_SELECTOR, 'h1')
            company_name = clean_text(name_elem.text)
            
            if not is_solar_related(company_name):
                return None
            
            # Phone
            phone = None
            try:
                phone_elem = driver.find_element(By.CSS_SELECTOR, '[data-item-id="phone"]')
                phone = extract_phone(phone_elem.text)
            except:
                pass
            
            # Website
            website = None
            try:
                website_elem = driver.find_element(By.CSS_SELECTOR, '[data-item-id="authority"]')
                website = normalize_url(website_elem.get_attribute('href'))
            except:
                pass
            
            # Address
            address = ""
            try:
                address_elem = driver.find_element(By.CSS_SELECTOR, '[data-item-id="address"]')
                address = clean_text(address_elem.text)
            except:
                pass
            
            return SolarLead(
                company_name=company_name,
                phone=phone,
                website=website,
                address=address,
                source_url="https://maps.google.com",
                business_type="solar_company"
            )
            
        except Exception as e:
            logger.error(f"Error parsing Google Maps listing: {e}")
            return None
    
    def close(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
        self.session.close()
