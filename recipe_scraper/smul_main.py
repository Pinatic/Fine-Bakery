from scraper_module import *

folder = '/commons/dsls/fine_bakery/scraped_recipes/smul/'

# Get recipe nr's from website
smul_receps = SmulwebScraper()
# smul_receps.get_numbers(destination=folder, start_at=1)

# Setting recep store location
smul_recipe_file = folder+'smulweb_recep_nrs.txt'

# Scraping the recipes
smul_scraper = scrape_recipes(folder+'smul_receps/', 
                              smul_receps.base_recipe_url,
                              smul_recipe_file)
smul_scraper.create_list()
smul_scraper.fetch_receps()
