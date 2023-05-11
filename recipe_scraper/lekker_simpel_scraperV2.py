import requests
from bs4 import BeautifulSoup


class LekkerSimpelScraper:
    """
    Scrapes all the recipes of lekkersimpel.com
    """

    def __init__(self) -> None:
        self.recipes = None
        self.base_recep_url = 'https://www.lekkerensimpel.com/'


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

        for tag in tags:
            print(f'working on {tag}')
            page_num = 1
            page_url = f'https://www.lekkerensimpel.com/{tag}/page/{page_num}/'

            while True:
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