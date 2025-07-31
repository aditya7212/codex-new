#!/usr/bin/env python3
"""
Solar Leads Scraper - Main execution script
"""

import argparse
import logging
from typing import List
import sys
import os

from models import SolarLead, ScrapingConfig
from solar_scraper import SolarLeadScraper
from utils import save_leads, deduplicate_leads, validate_lead

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function to run the solar leads scraper"""
    parser = argparse.ArgumentParser(description='Scrape solar leads from various sources')
    parser.add_argument('--sources', nargs='+', 
                       choices=['yellowpages', 'solarpowerworld', 'googlemaps', 'all'],
                       default=['yellowpages'],
                       help='Sources to scrape from')
    parser.add_argument('--location', type=str, default='United States',
                       help='Location to search for leads')
    parser.add_argument('--max-pages', type=int, default=5,
                       help='Maximum pages to scrape per source')
    parser.add_argument('--output', type=str, default='solar_leads.csv',
                       help='Output file name')
    parser.add_argument('--format', choices=['csv', 'json', 'xlsx'], default='csv',
                       help='Output format')
    parser.add_argument('--use-selenium', action='store_true',
                       help='Use Selenium for JavaScript-heavy sites')
    parser.add_argument('--headless', action='store_true', default=True,
                       help='Run browser in headless mode')
    parser.add_argument('--delay', type=float, default=1.0,
                       help='Delay between requests in seconds')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create scraping configuration
    config = ScrapingConfig(
        max_pages=args.max_pages,
        delay_between_requests=args.delay,
        use_selenium=args.use_selenium,
        headless=args.headless,
        output_format=args.format,
        output_file=args.output
    )
    
    logger.info(f"Starting solar leads scraping with config: {config}")
    logger.info(f"Sources: {args.sources}")
    logger.info(f"Location: {args.location}")
    
    # Initialize scraper
    scraper = SolarLeadScraper(config)
    all_leads = []
    
    try:
        # Determine which sources to scrape
        sources_to_scrape = args.sources
        if 'all' in sources_to_scrape:
            sources_to_scrape = ['yellowpages', 'solarpowerworld', 'googlemaps']
        
        # Scrape from each source
        for source in sources_to_scrape:
            logger.info(f"Scraping from {source}...")
            
            if source == 'yellowpages':
                leads = scraper.scrape_yellow_pages(
                    search_term="solar energy companies",
                    location=args.location
                )
                logger.info(f"Found {len(leads)} leads from Yellow Pages")
                all_leads.extend(leads)
            
            elif source == 'solarpowerworld':
                leads = scraper.scrape_solar_power_world()
                logger.info(f"Found {len(leads)} leads from Solar Power World")
                all_leads.extend(leads)
            
            elif source == 'googlemaps':
                if not config.use_selenium:
                    logger.warning("Google Maps requires Selenium. Use --use-selenium flag.")
                    continue
                leads = scraper.scrape_google_maps(
                    query="solar installation companies",
                    location=args.location
                )
                logger.info(f"Found {len(leads)} leads from Google Maps")
                all_leads.extend(leads)
        
        # Process and save leads
        logger.info(f"Total leads found: {len(all_leads)}")
        
        # Validate leads
        valid_leads = [lead for lead in all_leads if validate_lead(lead)]
        logger.info(f"Valid leads: {len(valid_leads)}")
        
        # Remove duplicates
        unique_leads = deduplicate_leads(valid_leads)
        logger.info(f"Unique leads after deduplication: {len(unique_leads)}")
        
        # Save to file
        if unique_leads:
            save_leads(unique_leads, args.output, args.format)
            logger.info(f"Successfully saved {len(unique_leads)} leads to {args.output}")
            
            # Print summary
            print_summary(unique_leads)
        else:
            logger.warning("No valid leads found to save")
    
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        sys.exit(1)
    finally:
        scraper.close()


def print_summary(leads: List[SolarLead]):
    """Print summary of scraped leads"""
    print("\n" + "="*50)
    print("SOLAR LEADS SCRAPING SUMMARY")
    print("="*50)
    print(f"Total leads found: {len(leads)}")
    
    # Count by business type
    business_types = {}
    for lead in leads:
        btype = lead.business_type or 'unknown'
        business_types[btype] = business_types.get(btype, 0) + 1
    
    print("\nBy business type:")
    for btype, count in business_types.items():
        print(f"  {btype}: {count}")
    
    # Count by state
    states = {}
    for lead in leads:
        state = lead.state or 'unknown'
        states[state] = states.get(state, 0) + 1
    
    print(f"\nTop 5 states:")
    sorted_states = sorted(states.items(), key=lambda x: x[1], reverse=True)
    for state, count in sorted_states[:5]:
        print(f"  {state}: {count}")
    
    # Contact info availability
    with_email = sum(1 for lead in leads if lead.email)
    with_phone = sum(1 for lead in leads if lead.phone)
    with_website = sum(1 for lead in leads if lead.website)
    
    print(f"\nContact information:")
    print(f"  With email: {with_email} ({with_email/len(leads)*100:.1f}%)")
    print(f"  With phone: {with_phone} ({with_phone/len(leads)*100:.1f}%)")
    print(f"  With website: {with_website} ({with_website/len(leads)*100:.1f}%)")
    
    print("\n" + "="*50)


if __name__ == "__main__":
    main()
