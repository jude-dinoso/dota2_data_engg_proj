from src.dota2api import *
from src.datagatherer import *
import json
import pandas as pd

get_data = DataGatherer()
match_id = get_data.get_match_data(batch_start=9999999999)
while True:
    print("======= Batch Done =========")
    match_id = get_data.get_match_data(batch_start=match_id[0])


