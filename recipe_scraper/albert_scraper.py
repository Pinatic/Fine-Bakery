import requests
import re
from recipe_scrapers import scrape_me
import pandas as pd


class AlbertScraper:

    def __init__(self) -> None:
        self.base_url = 'https://www.ah.nl/allerhande/recepten-zoeken?page='
        self.recipe_nums = None
        self.recipe_df = pd.DataFrame()

    def get_numbers(self):
        """
        Retrives all the recipe numbers from a range of AH recipe pages
        """

        pattern = 'R-R(\d{6,7})'
        numbers = []

        for num in range(0, 1):  # Change this to 0, 284 to get all the recipe numbers
            print(f'Page {num}')
            r = requests.get(f'{self.base_url}{num}')
            numbers += set(re.findall(pattern=pattern, string=r.text))

        self.recipe_nums = numbers

    def scrape_recipes(self):
        """
        Scrapes all the recipes found in the get_numbers functions and
        stores them in a DataFrame
        """
        for recp_num in self.recipe_nums[:10]:
            scraper = scrape_me(f'https://www.ah.nl/allerhande/recept/R-R{recp_num}')

            recipe = {'title': scraper.title(),
                      'ingredients': scraper.ingredients(),
                      'directions': scraper.instructions().split('\n'),
                      'linksource': scraper.url,
                      'NER': 'NaN'}  # Extend here if needed (I think yes.)

            self.recipe_df = pd.concat([self.recipe_df, pd.DataFrame([recipe])
                                        ], ignore_index=True)

    def recipes_to_csv(self, pathname):
        """
        Writes the recipe_df to a csv file.
        """
        self.recipe_df.to_csv(path_or_buf=pathname)