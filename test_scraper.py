#!/usr/bin/env python3
"""
Test script for Solar Leads Scraper
"""

import sys
import logging
from models import SolarLead, ScrapingConfig
from utils import clean_text, extract_email, extract_phone, is_solar_related, validate_lead
from solar_scraper import SolarLeadScraper

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_utilities():
    """Test utility functions"""
    print("Testing utility functions...")
    
    # Test text cleaning
    dirty_text = "  Solar   Installation\n\nCompany  "
    clean = clean_text(dirty_text)
    assert clean == "Solar Installation Company", f"Expected 'Solar Installation Company', got '{clean}'"
    
    # Test email extraction
    text_with_email = "Contact us at info@solarpanel.com for more info"
    email = extract_email(text_with_email)
    assert email == "info@solarpanel.com", f"Expected 'info@solarpanel.com', got '{email}'"
    
    # Test phone extraction
    text_with_phone = "Call us at (555) 123-4567 today"
    phone = extract_phone(text_with_phone)
    assert phone == "(555) 123-4567", f"Expected '(555) 123-4567', got '{phone}'"
    
    # Test solar keyword detection
    solar_text = "We install solar panels and renewable energy systems"
    non_solar_text = "We sell cars and automotive parts"
    assert is_solar_related(solar_text), "Should detect solar-related text"
    assert not is_solar_related(non_solar_text), "Should not detect non-solar text"
    
    print("✓ All utility tests passed!")


def test_data_models():
    """Test data models"""
    print("Testing data models...")
    
    # Create a valid lead
    lead = SolarLead(
        company_name="Test Solar Company",
        email="test@solar.com",
        phone="(555) 123-4567",
        city="Test City",
        state="CA"
    )
    
    # Test validation
    assert lead.is_valid(), "Valid lead should pass validation"
    
    # Test invalid lead
    invalid_lead = SolarLead(company_name="")
    assert not invalid_lead.is_valid(), "Invalid lead should fail validation"
    
    # Test dictionary conversion
    lead_dict = lead.to_dict()
    assert lead_dict['company_name'] == "Test Solar Company"
    assert lead_dict['email'] == "test@solar.com"
    
    print("✓ All data model tests passed!")


def test_scraper_initialization():
    """Test scraper initialization"""
    print("Testing scraper initialization...")
    
    # Test with default config
    config = ScrapingConfig()
    scraper = SolarLeadScraper(config)
    
    assert scraper.config.max_pages == 10, "Default max_pages should be 10"
    assert scraper.session is not None, "Session should be initialized"
    
    scraper.close()
    print("✓ Scraper initialization test passed!")


def test_basic_scraping():
    """Test basic scraping functionality (without making actual requests)"""
    print("Testing basic scraping setup...")
    
    config = ScrapingConfig(max_pages=1, delay_between_requests=0.5)
    scraper = SolarLeadScraper(config)
    
    # Test that scraper methods exist and are callable
    assert hasattr(scraper, 'scrape_yellow_pages'), "Should have scrape_yellow_pages method"
    assert hasattr(scraper, 'scrape_google_maps'), "Should have scrape_google_maps method"
    assert hasattr(scraper, '_parse_yellow_pages_listing'), "Should have parsing method"
    
    scraper.close()
    print("✓ Basic scraping setup test passed!")


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("Running Solar Leads Scraper Tests")
    print("=" * 50)
    
    try:
        test_utilities()
        test_data_models()
        test_scraper_initialization()
        test_basic_scraping()
        
        print("\n" + "=" * 50)
        print("✓ ALL TESTS PASSED!")
        print("The scraper is ready to use.")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        logger.error(f"Test error: {e}")
        return False


def check_dependencies():
    """Check if all required dependencies are installed"""
    print("Checking dependencies...")
    
    required_modules = [
        ('requests', 'requests'),
        ('beautifulsoup4', 'bs4'),
        ('selenium', 'selenium'),
        ('pandas', 'pandas'),
        ('lxml', 'lxml'),
        ('fake-useragent', 'fake_useragent'),
        ('webdriver-manager', 'webdriver_manager')
    ]

    missing_modules = []

    for package_name, import_name in required_modules:
        try:
            __import__(import_name)
            print(f"✓ {package_name}")
        except ImportError:
            missing_modules.append(package_name)
            print(f"❌ {package_name}")
    
    if missing_modules:
        print(f"\nMissing dependencies: {', '.join(missing_modules)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    else:
        print("✓ All dependencies are installed!")
        return True


if __name__ == "__main__":
    print("Solar Leads Scraper - Test Suite")
    
    # Check dependencies first
    if not check_dependencies():
        sys.exit(1)
    
    # Run tests
    if run_all_tests():
        print("\nYou can now run the scraper with:")
        print("python main.py --sources yellowpages --location 'California' --max-pages 2")
        print("\nOr try the examples:")
        print("python example_usage.py")
        sys.exit(0)
    else:
        sys.exit(1)
