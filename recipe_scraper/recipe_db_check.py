"""
Cecks the scraped recipes and turns it into a database
"""

import json
import glob
import multiprocessing as mp


class RecipeFolderToDB:
    """Turns a folder of recipe files into a database. 
    """

    def __init__(self, recipe_folder) -> None:
        self.recipe_folder = recipe_folder
        self.recipe_list = glob.glob(self.recipe_folder+'*.json')
        self.empty_recipes = []

    def check_empty_recep(self, recep_nr):
        try:
            with open(recep_nr, 'r') as json_file:
                recipe = json.load(json_file)

            if recipe['ingredients'] is None:
                self.empty_recipes.append(recipe)

            else:
                self.empty_recipes.append('.')

        except Exception as e:
            print(f'\n{recep_nr} could not be parsed')
            print(e)

    def empty_recipes_to_file(self, out_path='empty_recipes.txt'):
        """
        Dumps the paths of the empty recipe into a txt file.

        Args:
            out_path (str, optional): Filepath where the .txt file will be stored. 
            Defaults to 'empty_recipes.txt'.
        """
        with open(out_path, 'w') as out:
            out.write(str(self.empty_recipes))

    def create_database(self, out_path, datatype='csv'):
        """Turns all the loose json recipe files into a database

        Args:
            datatype (str): The kind of database you want. Defaults to '.csv'
            out_path (str): Where the database should be stored.
                            Defaults to 'recipe_database.{datatype}'
        """
        pass


def main():
    smul_path = '/commons/dsls/fine_bakery/scraped_recipes/smul/smul_receps/'
    f_out = '/commons/dsls/fine_bakery/scraped_recipes/smul/empty_recipes.txt'
    smul_checker = RecipeFolderToDB(smul_path)

    with mp.Pool() as p:
        print('checking recipes')
        p.map(smul_checker.check_empty_recep, smul_checker.recipe_list)

    print('writing empty recipes to file')
    smul_checker.empty_recipes_to_file(f_out)


if __name__ == '__main__':
    main()
