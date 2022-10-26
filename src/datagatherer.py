import os

from src.dota2api import *
import json
import pandas as pd
import pickle


class DataGatherer:

    def __init__(self):
        self.client = OpenDota2API()
        self.match_ids_set = set(self.get_retrieved_match_ids())
        self.match_data = []

    def get_heroes_data(self):
        data = self.client.get_heroes_list()
        heroes_df = pd.DataFrame.from_records(data)
        heroes_df.to_csv('./data/heroes.csv')

    def get_match_data(self):

        params = {
            "mmr_descending": 60
        }
        data = self.client.get_public_match_data(**params)
        match_data = pd.DataFrame.from_records(data)
        match_data = match_data.set_index("match_id")
        new_match_ids = match_data["match_id"].to_list()

        for id in new_match_ids:
            if id not in self.match_ids_set:
                pass
        pass

    @staticmethod
    def get_retrieved_match_ids() -> list[int]:
        if os.path.exists("data/match_ids.txt"):
            with open('data/match_ids.txt') as f:
                match_ids = pickle.load(f)
                return match_ids
        return []

    @staticmethod
    def save_match_ids(match_ids:list[str]):
        with open('data/match_ids.txt', 'wb') as f:
            pickle.dump(match_ids, f)
