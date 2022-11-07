import os
from typing import Tuple

from pandas import DataFrame

from src.dota2api import *
import json
import pandas as pd
import pickle
import time
import pandavro as pdvro


class DataGatherer:
    def __init__(self):
        self.client = OpenDota2API()
        self.match_ids = self.get_retrieved_match_ids()
        self.match_data = []

    def get_heroes_data(self):
        data = self.client.get_heroes_list()
        heroes_df = pd.DataFrame.from_records(data)
        self.save_df(heroes_df, "heroes")

    def get_match_data(self, batch_start=9999999999) -> Optional[list[int, int]]:

        match_data = pd.DataFrame()
        batch_start_end = []
        match_ids = self.get_retrieved_match_ids()
        for _ in range(10):
            params = {"less_than_match_id": batch_start}
            data = self.client.get_public_match_data(**params)
            new_match_data = pd.DataFrame.from_records(data)
            new_match_ids = new_match_data["match_id"].to_list()
            new_match_data = new_match_data.set_index("match_id")
            new_match_ids.sort()
            batch_start_end = [
                new_match_ids[0],
                batch_start if batch_start != 9999999999 else new_match_ids[99],
            ]

            [batch_start, batch_end] = self.find_in_match_ids(
                match_ids, batch_start_end
            )
            if batch_start:
                batch_start_end[0] = batch_start
            if batch_end:
                batch_start_end[1] = batch_end
            new_match_data = new_match_data[batch_start <= new_match_data.index]
            new_match_data = new_match_data[new_match_data.index <= batch_end]
            if match_data.empty:
                match_data = new_match_data
            else:
                merge_data = [match_data, new_match_data]
                match_data = pd.concat(merge_data)
            match_ids.append(batch_start_end)
            time.sleep(1)

        match_ids = self.merge_batch_ids(match_ids)
        self.save_df(match_data, "match_data")
        self.save_match_ids(match_ids)
        return match_ids[0]

    @staticmethod
    def save_df(df: DataFrame, directory_name: str):
        now = time.strftime("_%Y_%m_%d_%H_%M_%S", time.gmtime())
        pdvro.to_avro(f"data/{directory_name}/{directory_name + now}.avro", df)

    @staticmethod
    def get_retrieved_match_ids() -> list[list[int, int]]:
        match_ids = []
        if os.path.exists("data/match_data/match_ids/match_ids.pk1"):
            with open("data/match_data/match_ids/match_ids.pk1", "rb") as f:
                try:
                    while True:
                        match_ids.extend(pickle.load(f))
                except EOFError:
                    pass
                return match_ids
        return match_ids

    @staticmethod
    def save_match_ids(match_ids: list[list[int, int]]):
        with open("data/match_data/match_ids/match_ids.pk1", "wb") as f:
            match_ids.sort(key=lambda x: x[0])
            pickle.dump(match_ids, f)

    @staticmethod
    def find_in_match_ids(
        match_ids: list[list[int, int]], new_match_id: list[int, int]
    ) -> list[int, int]:

        for match_id in reversed(match_ids):
            if match_id[1] >= new_match_id[0]:
                if match_id[0] <= new_match_id[0]:
                    return [match_id[1], new_match_id[1]]
            if match_id[0] <= new_match_id[1]:
                if match_id[1] > new_match_id[1]:
                    return [new_match_id[0], match_id[0]]
        return [new_match_id[0], new_match_id[1]]

    @staticmethod
    def merge_batch_ids(match_ids: list[list[int, int]]) -> list[list[int, int]]:

        match_ids.sort(key=lambda x: x[0])
        result = [match_ids[0]]
        for interval in match_ids[1:]:
            if interval[0] <= result[-1][1]:
                result[-1][1] = max(result[-1][1], interval[1])
            else:
                result.append(interval)
        return result
