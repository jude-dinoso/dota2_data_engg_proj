from src.dota2api import *
import json
import pandas as pd


class DataGatherer:

    def __init__(self):
        self.client = OpenDota2API()

    def get_heroes_data(self):
        data = self.client.get_heroes_list()
        heroes_df = pd.DataFrame.from_records(data)
        heroes_df.to_csv('./data/heroes.csv')
