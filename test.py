from src.dota2api import *
from src.datagatherer import *
import json
import pandas as pd

get_data = DataGatherer()
match_id = get_data.get_match_data(batch_start=9999999999)
while True:
    match_id = get_data.get_match_data(batch_start=match_id[0])
    print("======= Batch Done =========")

