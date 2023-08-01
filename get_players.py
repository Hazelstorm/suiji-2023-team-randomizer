import csv
import json
import requests

from config import CLIENT_ID, CLIENT_SECRET
from ossapi import Ossapi
from models import Player
from more_itertools import batched


def from_osu() -> list[Player]:
    # Load csv
    with open("player_ids.csv") as file:
        reader = csv.reader(file)
        rows = [row for row in reader]

    # Load players
    # The osu!api returns up to 50 results at a time, so we need to batch our requests
    api = Ossapi(CLIENT_ID, CLIENT_SECRET)
    players = []
    for batch in batched(rows, 50):
        players += [Player(user)
                    for user in api.users([row[0] for row in batch])]

    return players


def from_tsc_2023_sheet():
    SHEET_ID = "1cAMcCkwm_pxeTusb-Tddm1xXUpk7ZFu_I1DVtm7Qx5Y"
    SHEET_NAME = "Player List"

    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

    # get sheet data and remove first row
    data = requests.get(url).text.split("\n")[1:]

    players = [Player({"username": row[1], "pp": float(row[2])})
               for row in filter(lambda row: row[1] and row[2] and row[3], csv.reader(data))]

    return players
