import yaml
import sys
from bokeh.io import export_png
from bokeh.plotting import figure
from panel.template import FastListTemplate
from datetime import date
from datetime import datetime
import json
import hvplot.pandas
import pandas as pd
import panel as pn
import param
import holoviews as hv
hv.extension('bokeh')
pn.extension('tabulator')
PALETTE = ["#ff6f69", "#ffcc5c", "#88d8b0", ]
with open('config.yaml', 'r') as stream:
    config = yaml.safe_load(stream)
    ingredient_names = config['ingredient_names']

ingredients = open(ingredient_names)
ingredients = ingredients.readlines()[0]
ingredients = ingredients.replace('"', '').replace('[', '')
ingredients = ingredients.replace(']', '').replace(' ', '').split(',')


class Page2:
    def __init__(self):
        self.content = pn.widgets.AutocompleteInput(name="Ingredient search",
                                                    options=ingredients,
                                                    case_sensitive=False)

    def get_replacement(self, n_predictions=10):
        """
        Returns a dataframe of the n most likely replacements for the given 
        ingredient, with their similarity score and function

        Args:
            ingredient (str): ingredient to replace
            n_predictions (int, optional): number of candidates. Defaults to 10.

        Returns:
            pd.DataFrame: Table of replacement candidates and their score and function
        """
        ingredient = self.content.value

    def view(self):
        # autocomplete = pn.widgets.AutocompleteInput(name="Ingredient search", options=["Cheese", "Egg", "Onion"])
        # self.content = pn.Row(pn.WidgetBox(autocomplete))
        return self.content


if __name__ == "__main__":
    pass
