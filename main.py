import get_players
import random

from config import SEED, PLAYER_DATA_SOURCE
from models import Tournament

if __name__ == "__main__":
    random.seed(SEED)

    print("Fetching users...")
    if PLAYER_DATA_SOURCE == "TSC2023":
        players = get_players.from_tsc_2023_sheet()
    elif PLAYER_DATA_SOURCE == "live":
        players = get_players.from_osu()
    elif PLAYER_DATA_SOURCE == "locked":
        players = get_players.from_locked()
    else:
        raise ValueError(
            f"PLAYER_DATA_SOURCE parameter is invalid. Received: \"{PLAYER_DATA_SOURCE}\". Expected: \"TSC2023\", \"live\" or \"locked\""
        )

    tournament = Tournament(players)
    tournament.balance_tournament()
    tournament.export_teams()
