from smulweb_scraper import SmulwebScraper
from generic_recep_scraper import scrape_recipes
import time

def main():
    smull_scraper = SmulwebScraper()
    smull_scraper.get_numbers()
    scrape_recipes('smulweb_receps',
                   smull_scraper.base_recipe_url,
                   smull_scraper.recipe_nums)


if __name__ == '__main__':
    start = time.time()
    main()
    print(f'runtime: {time.time() - start}s')
