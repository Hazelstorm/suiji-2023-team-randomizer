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


def from_tsc_2023_sheet() -> list[Player]:
    SHEET_ID = "1cAMcCkwm_pxeTusb-Tddm1xXUpk7ZFu_I1DVtm7Qx5Y"
    SHEET_NAME = "Player List"

    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    response = requests.get(url)

    # Checks if the response was successful
    response.raise_for_status()

    eligible_players = filter(
        lambda row: row[1] and row[2] and row[3],
        csv.reader(response.text.split("\n")[1:])
    )
    players = [Player({"username": player[1], "pp": float(player[2])})
               for player in eligible_players]

    return players


def from_locked() -> list[Player]:
    try:
        with open("players.json", "r") as file:
            players = [Player(player) for player in json.load(file)]
    except FileNotFoundError:
        raise FileNotFoundError(
            "Locked players data file could not be found. Run \"pipenv run lock\" to lock the pp of all players in \"player_ids.csv\""
        )
    return players
