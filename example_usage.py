#!/usr/bin/env python3
"""
Example usage of the Solar Leads Scraper
"""

from models import SolarLead, ScrapingConfig
from solar_scraper import SolarLeadScraper
from utils import save_leads, deduplicate_leads
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def basic_scraping_example():
    """Basic example of scraping solar leads"""
    print("=== Basic Solar Leads Scraping Example ===")
    
    # Create configuration
    config = ScrapingConfig(
        max_pages=3,
        delay_between_requests=1.5,
        use_selenium=False,
        output_format='csv',
        output_file='basic_solar_leads.csv'
    )
    
    # Initialize scraper
    scraper = SolarLeadScraper(config)
    
    try:
        # Scrape from Yellow Pages
        print("Scraping Yellow Pages...")
        leads = scraper.scrape_yellow_pages(
            search_term="solar installation",
            location="California"
        )
        
        print(f"Found {len(leads)} leads")
        
        # Save leads
        if leads:
            save_leads(leads, 'basic_example_leads.csv', 'csv')
            
            # Print first few leads
            print("\nFirst 3 leads:")
            for i, lead in enumerate(leads[:3]):
                print(f"\n{i+1}. {lead.company_name}")
                print(f"   Phone: {lead.phone}")
                print(f"   Location: {lead.city}, {lead.state}")
                print(f"   Website: {lead.website}")
    
    finally:
        scraper.close()


def advanced_scraping_example():
    """Advanced example with multiple sources and Selenium"""
    print("\n=== Advanced Solar Leads Scraping Example ===")
    
    # Create configuration for Selenium-based scraping
    config = ScrapingConfig(
        max_pages=2,
        delay_between_requests=2.0,
        use_selenium=True,
        headless=True,
        output_format='xlsx',
        output_file='advanced_solar_leads.xlsx'
    )
    
    # Initialize scraper
    scraper = SolarLeadScraper(config)
    all_leads = []
    
    try:
        # Scrape from multiple sources
        sources = [
            ("Yellow Pages", lambda: scraper.scrape_yellow_pages("solar energy", "Texas")),
            ("Google Maps", lambda: scraper.scrape_google_maps("solar companies", "Texas"))
        ]
        
        for source_name, scrape_func in sources:
            print(f"\nScraping from {source_name}...")
            try:
                leads = scrape_func()
                print(f"Found {len(leads)} leads from {source_name}")
                all_leads.extend(leads)
            except Exception as e:
                print(f"Error scraping {source_name}: {e}")
        
        # Process all leads
        print(f"\nTotal leads collected: {len(all_leads)}")
        
        # Remove duplicates
        unique_leads = deduplicate_leads(all_leads)
        print(f"Unique leads after deduplication: {len(unique_leads)}")
        
        # Save to Excel
        if unique_leads:
            save_leads(unique_leads, 'advanced_example_leads.xlsx', 'xlsx')
            
            # Analyze results
            analyze_leads(unique_leads)
    
    finally:
        scraper.close()


def custom_filtering_example():
    """Example of custom filtering and data processing"""
    print("\n=== Custom Filtering Example ===")
    
    config = ScrapingConfig(max_pages=2)
    scraper = SolarLeadScraper(config)
    
    try:
        # Scrape leads
        leads = scraper.scrape_yellow_pages("renewable energy", "Florida")
        
        # Custom filtering
        filtered_leads = []
        for lead in leads:
            # Only include leads with contact information
            if lead.email or lead.phone:
                # Only include leads with specific keywords
                text_to_check = f"{lead.company_name} {lead.description}".lower()
                if any(keyword in text_to_check for keyword in ['solar', 'photovoltaic', 'renewable']):
                    filtered_leads.append(lead)
        
        print(f"Original leads: {len(leads)}")
        print(f"Filtered leads: {len(filtered_leads)}")
        
        # Save filtered results
        if filtered_leads:
            save_leads(filtered_leads, 'filtered_solar_leads.csv', 'csv')
    
    finally:
        scraper.close()


def analyze_leads(leads):
    """Analyze scraped leads and print statistics"""
    print("\n=== Lead Analysis ===")
    
    # Basic stats
    total_leads = len(leads)
    with_email = sum(1 for lead in leads if lead.email)
    with_phone = sum(1 for lead in leads if lead.phone)
    with_website = sum(1 for lead in leads if lead.website)
    
    print(f"Total leads: {total_leads}")
    print(f"Leads with email: {with_email} ({with_email/total_leads*100:.1f}%)")
    print(f"Leads with phone: {with_phone} ({with_phone/total_leads*100:.1f}%)")
    print(f"Leads with website: {with_website} ({with_website/total_leads*100:.1f}%)")
    
    # Geographic distribution
    states = {}
    for lead in leads:
        state = lead.state or 'Unknown'
        states[state] = states.get(state, 0) + 1
    
    print(f"\nGeographic distribution:")
    for state, count in sorted(states.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {state}: {count}")
    
    # Business types
    business_types = {}
    for lead in leads:
        btype = lead.business_type or 'Unknown'
        business_types[btype] = business_types.get(btype, 0) + 1
    
    print(f"\nBusiness types:")
    for btype, count in business_types.items():
        print(f"  {btype}: {count}")


def create_sample_lead():
    """Create a sample lead for testing"""
    return SolarLead(
        company_name="Sunshine Solar Solutions",
        contact_person="John Smith",
        email="john@sunshinesolar.com",
        phone="(555) 123-4567",
        address="123 Solar Street",
        city="San Diego",
        state="CA",
        zip_code="92101",
        website="https://www.sunshinesolar.com",
        business_type="solar_installer",
        services=["residential solar", "commercial solar", "battery storage"],
        description="Full-service solar installation company serving San Diego County",
        source_url="https://example.com"
    )


def test_data_models():
    """Test the data models and utilities"""
    print("\n=== Testing Data Models ===")
    
    # Create sample lead
    lead = create_sample_lead()
    print(f"Created sample lead: {lead.company_name}")
    
    # Test validation
    print(f"Lead is valid: {lead.is_valid()}")
    
    # Test dictionary conversion
    lead_dict = lead.to_dict()
    print(f"Lead as dictionary has {len(lead_dict)} fields")
    
    # Test saving single lead
    save_leads([lead], 'sample_lead.json', 'json')
    print("Saved sample lead to JSON")


if __name__ == "__main__":
    print("Solar Leads Scraper - Example Usage")
    print("=" * 50)
    
    # Run examples
    try:
        # Test data models first
        test_data_models()
        
        # Run basic example
        basic_scraping_example()
        
        # Run custom filtering example
        custom_filtering_example()
        
        # Uncomment to run advanced example (requires more time)
        # advanced_scraping_example()
        
        print("\n" + "=" * 50)
        print("Examples completed successfully!")
        print("Check the generated files for results.")
        
    except Exception as e:
        logger.error(f"Error running examples: {e}")
        print(f"Error: {e}")
