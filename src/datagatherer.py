import os
from typing import Tuple

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
        heroes_df.to_feather('./data/heroes.feather')

    def get_match_data(self):

        params = {
            "mmr_descending": 60
        }

        data = self.client.get_public_match_data(**params)
        match_data = pd.DataFrame.from_records(data)
        new_match_ids = match_data["match_id"].to_list()
        match_data = match_data.set_index("match_id")
        batch_start_end = (new_match_ids[0], new_match_ids[99])
        match_ids = self.get_retrieved_match_ids()
        self.save_match_ids(batch_start_end)

        for id in new_match_ids:
            if id not in self.match_ids_set:
                pass
        pass

    @staticmethod
    def get_retrieved_match_ids() -> list[int]:
        match_ids = []
        if os.path.exists("data/match_ids.pk1"):
            with open('data/match_ids.pk1', 'rb') as f:
                while True:
                    try:
                        match_ids.append(pickle.load(f))
                    except EOFError:
                        continue
                return match_ids
        return match_ids

    @staticmethod
    def save_match_ids(match_ids: Tuple[int, int]):
        with open('data/match_ids.pk1', 'wb') as f:
            pickle.dump(match_ids, f)
