from scraper_module import *

folder = '/commons/dsls/fine_bakery/scraped_recipes/ah/'

# Get recipe nr's from website
ah_receps = AlbertScraper()
# ah_receps.get_numbers(destination=folder, start_at=0)

# Setting recep store location
ah_recipe_file = folder+'ah_recep_nrs.txt'

# Scraping the recipes
ah_scraper = scrape_recipes(folder+'ah_receps/', ah_receps.base_recipe_url,
                            ah_recipe_file)
ah_scraper.create_list()
ah_scraper.fetch_receps()
