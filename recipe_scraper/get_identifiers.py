"""
In this script we will get all the identifiers from the websites and store them
in a txt file
"""
import asyncio
import yaml
from recipe_identifier_fetchers import SmulwebScraper, AlbertScraper

# First, loading the configuration file
with open('scrape_configuration.yaml', 'r') as stream:
    config = yaml.safe_load(stream)

# Lets start with all the albert heijn variables
ah_folder = config['ah_folder']
ah_base_url = config['ah_base_url']
ah_identifier_output = config['ah_identifier_output']
ah_identifier_txt = config['ah_identifier_txt']

# Then the smulweb variables
smul_folder = config['smul_folder']
suml_base_url = config['smul_base_url']
smul_identifier_output = config['smul_identifier_output']
smul_identifier_txt = config['smul_identifier_txt']

async def main():
    """
    This script first fetches all the recipe names from the website and stores 
    them in a text file. Then scrapes all the recipes found in the text file 
    and stores each recipe in a seperate json file.
    """
    
    # Depending on the amount of pages the website has this might take a long time
    ah_ident_scraper = AlbertScraper()
    await ah_ident_scraper.get_numbers(ah_identifier_output)     

    smul_ident_scraper = SmulwebScraper()
    await smul_ident_scraper.get_numbers(smul_identifier_output)
    
if __name__ == '__main__':
    asyncio.run(main())