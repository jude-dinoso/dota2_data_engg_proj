from src.dota2api import *
from src.datagatherer import *
import json
import pandas as pd

get_data = DataGatherer()
get_data.get_heroes_data()

print("======= DONE =========")
