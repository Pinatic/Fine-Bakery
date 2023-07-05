import asyncio
import yaml
from recipe_scraper import RecipeScraper
import multiprocessing as mp

# First, loading the configuration file
with open('scrape_configuration.yaml', 'r') as stream:
    config = yaml.safe_load(stream)

# Lets start with all the albert heijn variables
ah_folder = config['ah_folder']
ah_base_url = config['ah_base_url']
ah_identifier_txt = config['ah_identifier_txt']

# Then the smulweb variables
smul_folder = config['smul_folder']
suml_base_url = config['smul_base_url']
smul_identifier_txt = config['smul_identifier_txt']

# Now on to the scraping
async def main():
    
    # Lets start with the albert heijn recipes
    ah_scraper = RecipeScraper(ah_folder, ah_base_url, ah_identifier_txt)
    # First we need to make a list of the txt file
    ah_recipe_list = ah_scraper.create_list()
    # Then we can start scraping
    with mp.Pool() as p:
        await p.map(ah_scraper.scrape_recipe, ah_recipe_list)
        
    # Now we can do the same for the smulweb recipes
    smul_scraper = RecipeScraper(smul_folder, suml_base_url, 
                                 smul_identifier_txt)
    smul_recipe_list = smul_scraper.create_list()
    with mp.Pool() as p:
        await p.map(smul_scraper.scrape_recipe, smul_recipe_list)
        
if __name__ == "__main__":
    asyncio.run(main())

    