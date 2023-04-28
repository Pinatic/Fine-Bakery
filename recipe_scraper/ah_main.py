from albert_scraperV3 import AlbertScraper
from generic_recep_scraper import scrape_recipes
import time

def main():
    print('Scraping Albert Hein')
    ah_scraper = AlbertScraper()
    ah_scraper.get_numbers()
    scrape_recipes('recipe_scraper/ah_receps',
                   ah_scraper.base_recipe_url,
                   ah_scraper.recipe_nums)

if __name__ == '__main__':
    start = time.time()
    main()
    print(f'runtime: {time.time() - start}s')
