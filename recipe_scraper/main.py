from albert_scraper import AlbertScraper
import time

def main():
    ah_scraper = AlbertScraper()
    ah_scraper.get_numbers()
    ah_scraper.scrape_recipes()
    ah_scraper.recipes_to_csv('first_page.csv')

if __name__ == '__main__':
    start = time.time()
    main()
    print(f'runtime: {time.time() - start}s')
