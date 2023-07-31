import csv
import json
import random

from ossapi import Ossapi
from config import SEED, CLIENT_ID, CLIENT_SECRET
from models import Tournament, Player
from more_itertools import batched

if __name__ == "__main__":
    random.seed(SEED)

    # # Load csv
    # with open("player_ids.csv") as file:
    #     reader = csv.reader(file)
    #     rows = [row for row in reader]

    # # Load players
    # # The osu!api returns up to 50 results at a time, so we need to batch our requests
    # print("Fetching users...")
    # api = Ossapi(CLIENT_ID, CLIENT_SECRET)
    # players = []
    # for batch in batched(rows, 50):
    #     players += [Player(user) for user in api.users([row[0] for row in batch])]

    # Load static players

    try:
        with open("players.json") as file:
            players = [Player(player) for player in json.load(file)]
    except FileNotFoundError:
        raise FileNotFoundError(
            "players.json file is missing! ensure that generate_players_json.py has been run, for example through 'pipenv run json'")

    tournament = Tournament(players)
    tournament.balance_tournament()
    tournament.export_teams()
