import requests
from recipe_scrapers import scrape_me
from datetime import datetime
from bs4 import BeautifulSoup


class LekkerSimpelScraper:
    """
    Scrapes all the recipes of lekkersimpel.com
    """

    def __init__(self) -> None:
        self.recipes = None
        self.output_path = f"lkkr_smpl_{datetime.today().strftime('%Y-%m-%d')}.csv"

    def get_recipes(self):
        """
        Goes through all the pages of all the food categories and stores the
        recipes in a list. Any duplicates are removed from this list and then
        it gets saved as a object variable.
        """
        tags = ['ontbijtrecepten', 'lunchrecepten', 'tussendoortjes',
                'voorgerecht', 'hoofdgerechten', 'bijgerechten',
                'nagerechten', 'salades', 'bakken']

        recipes = []

        for tag in tags[:2]:
            print(f'working on {tag}')
            page_num = 1
            page_url = f'https://www.lekkerensimpel.com/{tag}/page/{page_num}/'

            while page_num < 2:
                print(f'page number: {page_num}')
                html = requests.get(page_url)

                if 'class="cell large-6 medium-6 small-12"' in html.text:

                    soup = BeautifulSoup(html.text, 'html.parser')

                    [recipes.append(a['href'].split('/')[-2]) for a in
                     (soup.find_all('a', attrs={"class": "post-item__anchor"}))]

                    page_num += 1

                else:
                    break

        self.recipes = list(set(recipes))

    def scrape_recipes(self):
        """
        Scrapes all the recipes found in the get_recipes functions and
        stores them in a CSV
        """

        # writing the header
        with open(self.output_path, 'w') as output:  # !! Change to append !!
            output.write("title,ingredients,directions,linksource,NER\n")

            # Setting up a counter so we can track progress
            n = 1

            for recp in self.recipes[:4]:
                scraper = scrape_me(f'https://www.lekkerensimpel.com/{recp}')
                
                title = scraper.title()
                ingredients = scraper.ingredients()
                instructions = scraper.instructions_list()
                url = scraper.url

                output.write(f'{title},"{ingredients}","{instructions}",{url}\,\n')

                print(f'{n} recipes scraped')
                n += 1
