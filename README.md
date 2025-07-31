# Solar Leads Scraper

A comprehensive Python tool for scraping solar industry leads from various online sources including Yellow Pages, Google Maps, and industry-specific directories.

## Features

- **Multiple Data Sources**: Scrape from Yellow Pages, Google Maps, Solar Power World, and more
- **Smart Filtering**: Automatically identifies solar-related businesses using keyword matching
- **Data Validation**: Validates and cleans scraped data for quality assurance
- **Multiple Output Formats**: Export to CSV, JSON, or Excel formats
- **Duplicate Removal**: Intelligent deduplication based on company name and contact info
- **Rate Limiting**: Built-in delays and rate limiting to avoid being blocked
- **Selenium Support**: JavaScript-heavy sites supported with Selenium WebDriver
- **Configurable**: Extensive configuration options for different scraping scenarios

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd solar-leads-scraper
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. For Selenium support, Chrome/Chromium browser is required (automatically managed by webdriver-manager)

## Quick Start

### Basic Usage

```python
from models import ScrapingConfig
from solar_scraper import SolarLeadScraper
from utils import save_leads

# Create configuration
config = ScrapingConfig(
    max_pages=5,
    delay_between_requests=1.5,
    output_format='csv'
)

# Initialize scraper
scraper = SolarLeadScraper(config)

# Scrape leads
leads = scraper.scrape_yellow_pages("solar installation", "California")

# Save results
save_leads(leads, 'solar_leads.csv', 'csv')
scraper.close()
```

### Command Line Usage

```bash
# Basic scraping from Yellow Pages
python main.py --sources yellowpages --location "Texas" --max-pages 3

# Scrape from multiple sources with Selenium
python main.py --sources yellowpages googlemaps --use-selenium --location "California"

# Export to Excel format
python main.py --sources all --format xlsx --output solar_leads.xlsx

# Verbose output
python main.py --sources yellowpages --location "Florida" --verbose
```

## Command Line Options

- `--sources`: Choose sources to scrape from (yellowpages, solarpowerworld, googlemaps, all)
- `--location`: Geographic location to search (default: "United States")
- `--max-pages`: Maximum pages to scrape per source (default: 5)
- `--output`: Output file name (default: solar_leads.csv)
- `--format`: Output format - csv, json, or xlsx (default: csv)
- `--use-selenium`: Enable Selenium for JavaScript-heavy sites
- `--headless`: Run browser in headless mode (default: true)
- `--delay`: Delay between requests in seconds (default: 1.0)
- `--verbose`: Enable verbose logging

## Data Structure

Each lead contains the following information:
- Company name
- Contact person (when available)
- Email address
- Phone number
- Physical address (street, city, state, zip)
- Website URL
- Business type (installer, manufacturer, etc.)
- Services offered
- Description
- Source URL
- Timestamp when scraped

## Configuration

The scraper can be configured through the `ScrapingConfig` class:

```python
config = ScrapingConfig(
    max_pages=10,                    # Pages to scrape per source
    delay_between_requests=2.0,      # Delay between requests
    use_selenium=True,               # Use Selenium for JS sites
    headless=True,                   # Headless browser mode
    timeout=30,                      # Request timeout
    max_retries=3,                   # Retry failed requests
    output_format='xlsx',            # Output format
    output_file='leads.xlsx'         # Output filename
)
```

## Supported Sources

1. **Yellow Pages** - Business directory with solar companies
2. **Google Maps** - Local business listings (requires Selenium)
3. **Solar Power World** - Industry-specific directory
4. **Yelp** - Business reviews and listings (configurable)
5. **Better Business Bureau** - Accredited businesses (configurable)

## Examples

See `example_usage.py` for comprehensive examples including:
- Basic scraping
- Advanced multi-source scraping
- Custom filtering
- Data analysis
- Testing data models

Run examples:
```bash
python example_usage.py
```

## Legal and Ethical Considerations

- **Respect robots.txt**: Always check and respect website robots.txt files
- **Rate Limiting**: Built-in delays prevent overwhelming target servers
- **Terms of Service**: Ensure compliance with website terms of service
- **Data Usage**: Use scraped data responsibly and in compliance with applicable laws
- **Privacy**: Respect privacy and only collect publicly available information

## Troubleshooting

### Common Issues

1. **Selenium WebDriver Issues**:
   - Ensure Chrome/Chromium is installed
   - Check internet connection
   - Try running with `--headless` flag

2. **Rate Limiting**:
   - Increase delay between requests
   - Use proxy rotation if needed
   - Reduce max_pages setting

3. **No Results Found**:
   - Check search terms and location
   - Verify website structure hasn't changed
   - Enable verbose logging for debugging

### Debugging

Enable verbose logging:
```bash
python main.py --verbose
```

Or in code:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and research purposes. Users are responsible for ensuring compliance with website terms of service and applicable laws. The authors are not responsible for any misuse of this software.