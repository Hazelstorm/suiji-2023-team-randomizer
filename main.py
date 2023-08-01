import get_players
import random

from config import SEED, USE_OSU_API
from models import Tournament

if __name__ == "__main__":
    random.seed(SEED)

    print("fetching users...")
    players = get_players.from_osu() if USE_OSU_API else get_players.from_tsc_2023_sheet()

    tournament = Tournament(players)
    tournament.balance_tournament()
    tournament.export_teams()
