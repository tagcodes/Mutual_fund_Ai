import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from markdownify import markdownify as md

# URLs to scrape
HDFC_FUNDS = {
    "HDFC Mid Cap Fund": "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
    "HDFC Equity Fund": "https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth",
    "HDFC Focused Fund": "https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth",
    "HDFC ELSS Tax Saver Fund": "https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth",
    "HDFC Large Cap Fund": "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth"
}

# Output directory for Phase 1 Ingestion
OUTPUT_DIR = "src/phase_1_ingestion/data"

def scrape_fund(name, url):
    print(f"Scraping {name} from {url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Groww fund pages often have the main content in specific containers
        # We target common containers or the whole body if specific ones fail
        content_container = soup.find('div', {'class': 'mf_details_container'}) or soup.find('body')
        
        if not content_container:
            print(f"Warning: Could not find content container for {name}")
            return
            
        # Convert to Markdown
        markdown_content = md(str(content_container), heading_style="ATX")
        
        # Add Metadata header
        header = f"---\nscheme_name: {name}\nsource_url: {url}\nlast_updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n---\n\n"
        final_content = header + markdown_content
        
        # Save to file
        filename = f"{name.replace(' ', '_').lower()}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_content)
        
        print(f"Successfully saved {name} to {filepath}")
        
    except Exception as e:
        print(f"Error scraping {name}: {e}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    for name, url in HDFC_FUNDS.items():
        scrape_fund(name, url)

if __name__ == "__main__":
    main()
