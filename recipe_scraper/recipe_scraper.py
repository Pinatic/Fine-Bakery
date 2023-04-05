from recipe_scrapers import scrape_me
import sys

def scrape_url(url, filename):
    """ function that scrapes recipe data"""

    try:
        scraper = scrape_me(url, wild_mode=True)
        with open('raw/'+filename, 'w') as f: 
            f.write(f'{scraper.title()}\n')
            f.write(f'cooking time: {scraper.total_time()}\n')
            f.write(f'number of servings: {scraper.yields()[:2]}\n')
            f.write('\nRECIPE\n')
            for i in scraper.ingredients(): f.write(i+'\n')
            f.write('\nINSTRUCTIONS\n')
            f.write(scraper.instructions()+'\n')
            f.write(f'\nimage: {scraper.image()}\n')
            f.write(f'\nsource: {scraper.host()}\n')
            f.write('\nNUTRIENTS\n')
            for k,v in scraper.nutrients().items(): f.write(f'{k}:{v}\n')  # if available
            f.write(f'\nauthor: {scraper.author()}\n')
            f.write(f'\ncanonical_url: {scraper.canonical_url()}\n')
            f.write(f'\nlanguage: {scraper.language()}\n')
            f.write(f'\nreviews: {scraper.reviews()}\n')
            f.write(f'\nsite_name: {scraper.site_name()}\n')

    except Exception:
        print(f'no information retrieved from {url}\n')

    return 0

if __name__ == '__main__':
    url = 'https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/'
    filename = 'test.txt'

    scrape_url(url=url, filename='test.txt')
